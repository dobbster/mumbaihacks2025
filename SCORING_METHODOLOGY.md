# Scoring Methodology for Pattern Detection

This document explains how each factor is scored in the pattern detection system.

## Overview

Each pattern detection method calculates a **risk score** (0.0 to 1.0), where:
- **0.0** = No risk (legitimate news)
- **1.0** = Maximum risk (likely misinformation)

The overall risk score is the **average** of all four individual risk scores.

---

## 1. Contradiction Detection Score

**Location**: `app/core/pattern_detection.py`, line 452

### Formula

```python
risk_score = min(1.0, contradiction_count / total_datapoints)
```

### How It Works

1. **Find Contradictions**: 
   - Uses embedding similarity to find similar claims (similarity ≥ 0.7)
   - Checks for contradiction keywords: "false", "debunked", "unfounded", "rumors", "misinformation", etc.
   - Compares titles for topic similarity

2. **Count Unique Pairs**: 
   - Removes duplicate contradiction pairs
   - Each pair represents two conflicting claims about the same topic

3. **Calculate Risk**:
   - **Risk = (Number of Contradiction Pairs) / (Total Datapoints in Cluster)**
   - Capped at 1.0 (100% risk)

### Example

- **Cluster with 18 datapoints**
- **5 contradiction pairs found**
- **Risk Score = 5 / 18 = 0.278** (27.8% risk)

### Why This Formula?

- **Proportional Risk**: More contradictions relative to cluster size = higher risk
- **Normalized**: Always between 0.0 and 1.0
- **Simple**: Easy to understand and interpret

### Current Issue

This formula can be **too lenient** for large clusters. For example:
- 5 contradictions in 100 datapoints = 0.05 risk (very low)
- But 5 contradictions might still indicate misinformation

**Potential Improvement**: Use logarithmic scaling or minimum threshold:
```python
risk_score = min(1.0, (contradiction_count / total_datapoints) * 2.0)  # Amplify
# OR
risk_score = min(1.0, max(0.3, contradiction_count / total_datapoints))  # Minimum threshold
```

---

## 2. Rapid Growth Detection Score

**Location**: `app/core/pattern_detection.py`, lines 201-205

### Formula

```python
risk_score = min(1.0, (
    (min(growth_rate, 10) / 10) * 0.4 +           # Growth rate (40%)
    (min(datapoints_per_hour, 10) / 10) * 0.3 +  # Velocity (30%)
    (min(cluster_size, 50) / 50) * 0.3            # Size (30%)
))
```

### Components

1. **Growth Rate** (40% weight):
   - `growth_rate = current_window_size / previous_window_size`
   - Example: 7 articles in last 6 hours vs 2 in previous 6 hours = 3.5x growth
   - Capped at 10x (anything above = 100% of this component)

2. **Velocity** (30% weight):
   - `datapoints_per_hour = total_datapoints / time_span_hours`
   - Example: 18 datapoints over 10 hours = 1.8 per hour
   - Capped at 10 per hour

3. **Cluster Size** (30% weight):
   - Larger clusters = higher risk (more spread)
   - Capped at 50 datapoints (clusters larger than 50 = 100% of this component)

### Example

- **Growth Rate**: 3.5x → `(3.5/10) * 0.4 = 0.14`
- **Velocity**: 1.8/hour → `(1.8/10) * 0.3 = 0.054`
- **Size**: 18 datapoints → `(18/50) * 0.3 = 0.108`
- **Total Risk Score = 0.14 + 0.054 + 0.108 = 0.302** (30.2% risk)

### Why This Formula?

- **Multi-factor**: Considers growth, speed, and size
- **Weighted**: Growth rate is most important (40%)
- **Capped**: Prevents extreme values from skewing results

---

## 3. Source Credibility Score

**Location**: `app/core/pattern_detection.py`, lines 287-291

### Formula

```python
risk_score = (
    (1 - credible_ratio) * 0.5 +                                    # Low credibility (50%)
    (min(questionable_count / total_sources, 1.0)) * 0.3 +          # Questionable sources (30%)
    (1 - min(source_diversity / 10, 1.0)) * 0.2                     # Low diversity (20%)
)
```

### Components

1. **Credible Ratio** (50% weight):
   - `credible_ratio = credible_count / total_datapoints`
   - Sources with credibility ≥ 0.7 are "credible"
   - **Lower credible ratio = Higher risk**
   - Example: 10 credible out of 18 total = 0.556 ratio → `(1 - 0.556) * 0.5 = 0.222`

2. **Questionable Sources** (30% weight):
   - Sources with credibility < 0.5 are "questionable"
   - **More questionable sources = Higher risk**
   - Example: 0 questionable out of 18 = `(0/18) * 0.3 = 0.0`

3. **Source Diversity** (20% weight):
   - `source_diversity = number of unique sources`
   - **Lower diversity = Higher risk** (echo chamber effect)
   - Example: 5 unique sources → `(1 - 5/10) * 0.2 = 0.1`

### Example

- **Credible Ratio**: 0.556 → `(1 - 0.556) * 0.5 = 0.222`
- **Questionable Count**: 0 → `(0/18) * 0.3 = 0.0`
- **Source Diversity**: 5 → `(1 - 5/10) * 0.2 = 0.1`
- **Total Risk Score = 0.222 + 0.0 + 0.1 = 0.322** (32.2% risk)

### Source Credibility Database

Sources are scored in `CREDIBLE_SOURCES` dictionary:
- **High (0.9-1.0)**: BBC News (0.95), Reuters (0.95), AP News (0.95)
- **Medium (0.6-0.8)**: Firstpost (0.70), India Today (0.75)
- **Low (0.3-0.5)**: Unknown (0.50), Social Media (0.30), Blog (0.40)

---

## 4. Narrative Evolution Score

**Location**: `app/core/pattern_detection.py`, lines 576-580

### Formula

```python
risk_score = min(1.0, (
    (len(key_changes) / max(len(time_windows), 1)) * 0.5 +           # Change frequency (50%)
    (min(len(evolution_stages), 5) / 5) * 0.3 +                     # Number of stages (30%)
    (1 if has_evolution else 0) * 0.2                                # Has evolution (20%)
))
```

### Components

1. **Change Frequency** (50% weight):
   - Groups datapoints into 6-hour time windows
   - Compares keywords between windows
   - **More changes = Higher risk**
   - Example: 3 changes across 4 windows → `(3/4) * 0.5 = 0.375`

2. **Number of Stages** (30% weight):
   - Counts distinct time windows with different narratives
   - **More stages = Higher risk**
   - Capped at 5 stages (anything above = 100% of this component)
   - Example: 4 stages → `(4/5) * 0.3 = 0.24`

3. **Has Evolution** (20% weight):
   - Binary: 1.0 if any evolution detected, 0.0 otherwise
   - Example: Has evolution → `1.0 * 0.2 = 0.2`

### Example

- **Change Frequency**: 3 changes / 4 windows → `(3/4) * 0.5 = 0.375`
- **Stages**: 4 stages → `(4/5) * 0.3 = 0.24`
- **Has Evolution**: Yes → `1.0 * 0.2 = 0.2`
- **Total Risk Score = 0.375 + 0.24 + 0.2 = 0.815** (81.5% risk)

### How Evolution is Detected

1. **Time Windows**: Groups datapoints into 6-hour windows
2. **Keyword Extraction**: Extracts top 5 keywords from titles in each window
3. **Change Detection**: Compares keywords between consecutive windows
4. **New Keywords**: If new keywords appear, it's a narrative shift

---

## Overall Risk Score

**Location**: `app/core/pattern_detection.py`, line 630

### Formula

```python
overall_risk_score = mean([
    growth_risk_score,
    credibility_risk_score,
    contradiction_risk_score,
    evolution_risk_score
])
```

### Risk Levels

- **High Risk** (≥0.7): Immediate review recommended
- **Medium Risk** (0.4-0.7): Review recommended
- **Low Risk** (<0.4): Appears legitimate

### Example from Your Data

From your cluster_0 analysis:
- **Growth Risk**: 0.508
- **Credibility Risk**: 0.322
- **Contradiction Risk**: 0.278
- **Evolution Risk**: 0.815

**Overall = (0.508 + 0.322 + 0.278 + 0.815) / 4 = 0.481** → **Medium Risk**

---

## Potential Improvements

### 1. Contradiction Detection

**Current**: `risk_score = contradiction_count / total_datapoints`

**Issue**: Too lenient for large clusters

**Suggestion**:
```python
# Option 1: Amplify
risk_score = min(1.0, (contradiction_count / total_datapoints) * 2.0)

# Option 2: Minimum threshold
risk_score = min(1.0, max(0.3, contradiction_count / total_datapoints))

# Option 3: Logarithmic
risk_score = min(1.0, math.log(1 + contradiction_count) / math.log(1 + total_datapoints))
```

### 2. Weighted Overall Score

**Current**: Simple average (all factors equal weight)

**Suggestion**: Weight by importance:
```python
overall_risk_score = (
    growth_risk * 0.3 +        # Growth is important
    credibility_risk * 0.3 +    # Credibility is important
    contradiction_risk * 0.25 + # Contradictions are strong signals
    evolution_risk * 0.15       # Evolution is less critical
)
```

### 3. Contradiction Quality

**Current**: Counts all contradiction pairs equally

**Suggestion**: Weight by contradiction type:
- `fact_check_vs_claim` = 1.0 (strong signal)
- `conflicting_claims` = 0.7 (moderate signal)
- `rumor_vs_fact` = 0.9 (strong signal)

---

## Summary

| Factor | Weight in Overall Score | Key Metric | Current Formula |
|--------|------------------------|------------|-----------------|
| **Rapid Growth** | 25% (equal weight) | Growth rate, velocity, size | Weighted sum (40%+30%+30%) |
| **Source Credibility** | 25% (equal weight) | Credible ratio, questionable count, diversity | Weighted sum (50%+30%+20%) |
| **Contradictions** | 25% (equal weight) | Contradiction pairs / total datapoints | Simple ratio |
| **Narrative Evolution** | 25% (equal weight) | Change frequency, stages, has evolution | Weighted sum (50%+30%+20%) |

**Overall Risk = Average of all 4 scores**

