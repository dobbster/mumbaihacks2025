# Pattern Detection Guide

## Overview

The Pattern Detection Service analyzes clusters of news articles to identify potential misinformation patterns. It detects:

1. **Rapid Growth**: Sudden spikes in article volume (misinformation spreads faster)
2. **Source Credibility**: Ratio of credible vs. questionable sources
3. **Contradictions**: Conflicting claims within the same cluster
4. **Narrative Evolution**: How stories change over time

## Quick Start

### 1. Ensure Clusters Exist

First, make sure you have clustered datapoints:

```bash
# Cluster recent datapoints
curl -X POST "http://localhost:2024/clustering/cluster?hours=8760&eps=0.30&min_cluster_size=2"
```

### 2. Analyze a Specific Cluster

```bash
# Get comprehensive analysis for a cluster
curl "http://localhost:2024/pattern-detection/cluster/cluster_0"
```

### 3. Analyze All Clusters

```bash
# Analyze all clusters and get summary
curl -X POST "http://localhost:2024/pattern-detection/analyze-all?hours=8760&min_cluster_size=2"
```

### 4. Get High-Risk Clusters

```bash
# Get all clusters with risk score >= 0.6
curl "http://localhost:2024/pattern-detection/high-risk-clusters?hours=8760&risk_threshold=0.6"
```

## API Endpoints

### GET `/pattern-detection/cluster/{cluster_id}`

Comprehensive analysis of a specific cluster.

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "cluster_id": "cluster_0",
    "datapoint_count": 5,
    "overall_risk_score": 0.65,
    "risk_level": "medium",
    "flags": {
      "rapid_growth": true,
      "low_credibility": false,
      "has_contradictions": true,
      "narrative_evolution": false
    },
    "flag_count": 2,
    "growth_analysis": {...},
    "credibility_analysis": {...},
    "contradiction_analysis": {...},
    "evolution_analysis": {...},
    "recommendation": "MEDIUM RISK: Review recommended..."
  }
}
```

### GET `/pattern-detection/cluster/{cluster_id}/rapid-growth`

Detect rapid growth in a cluster.

**Parameters:**
- `time_window_hours` (int, default: 6): Time window for growth analysis

**Response:**
```json
{
  "status": "success",
  "cluster_id": "cluster_0",
  "rapid_growth_analysis": {
    "is_rapid_growth": true,
    "growth_rate": 3.5,
    "current_size": 7,
    "previous_size": 2,
    "datapoints_per_hour": 1.2,
    "risk_score": 0.75
  }
}
```

### GET `/pattern-detection/cluster/{cluster_id}/credibility`

Analyze source credibility within a cluster.

**Response:**
```json
{
  "status": "success",
  "cluster_id": "cluster_0",
  "credibility_analysis": {
    "credible_ratio": 0.6,
    "credible_count": 3,
    "questionable_count": 2,
    "source_diversity": 5,
    "risk_score": 0.4,
    "credible_sources": ["BBC News", "Reuters", "AP News"],
    "questionable_sources": ["Unknown Blog", "Social Media"]
  }
}
```

### GET `/pattern-detection/cluster/{cluster_id}/contradictions`

Detect contradictory claims within a cluster.

**Parameters:**
- `similarity_threshold` (float, default: 0.7): Minimum similarity for contradiction detection

**Response:**
```json
{
  "status": "success",
  "cluster_id": "cluster_0",
  "contradiction_analysis": {
    "has_contradictions": true,
    "contradiction_count": 2,
    "contradiction_pairs": [...],
    "risk_score": 0.5
  }
}
```

### GET `/pattern-detection/cluster/{cluster_id}/evolution`

Track narrative evolution over time.

**Response:**
```json
{
  "status": "success",
  "cluster_id": "cluster_0",
  "evolution_analysis": {
    "has_evolution": true,
    "evolution_stages": [...],
    "key_changes": [...],
    "risk_score": 0.6
  }
}
```

### POST `/pattern-detection/analyze-all`

Analyze all clusters found in recent datapoints.

**Parameters:**
- `hours` (int, default: 168): Look back this many hours
- `min_cluster_size` (int, default: 2): Minimum cluster size to analyze

**Response:**
```json
{
  "status": "success",
  "summary": {
    "total_clusters_analyzed": 10,
    "high_risk_clusters": 2,
    "medium_risk_clusters": 3,
    "low_risk_clusters": 5,
    "average_risk_score": 0.45,
    "high_risk_cluster_ids": ["cluster_0", "cluster_5"]
  },
  "analyses": {...}
}
```

### GET `/pattern-detection/high-risk-clusters`

Get all high-risk clusters (potential misinformation).

**Parameters:**
- `hours` (int, default: 168): Look back this many hours
- `min_cluster_size` (int, default: 2): Minimum cluster size
- `risk_threshold` (float, default: 0.6): Minimum risk score

**Response:**
```json
{
  "status": "success",
  "high_risk_clusters": [
    {
      "cluster_id": "cluster_0",
      "risk_score": 0.75,
      "risk_level": "high",
      "flags": {...},
      "datapoint_count": 8,
      "recommendation": "HIGH RISK: Immediate review recommended..."
    }
  ],
  "count": 1,
  "risk_threshold": 0.6
}
```

## Risk Scoring

The system calculates an overall risk score (0.0-1.0) based on:

1. **Rapid Growth** (40% weight): High growth rate = higher risk
2. **Source Credibility** (30% weight): Low credible sources = higher risk
3. **Contradictions** (20% weight): More contradictions = higher risk
4. **Narrative Evolution** (10% weight): Significant changes = higher risk

### Risk Levels

- **High Risk** (≥0.7): Immediate review recommended
- **Medium Risk** (0.4-0.7): Review recommended
- **Low Risk** (<0.4): Appears legitimate

## Source Credibility Database

The system maintains a database of source credibility scores:

### High Credibility (0.9-1.0)
- BBC News, Reuters, AP News, CNN, The Guardian, etc.

### Medium Credibility (0.6-0.8)
- Firstpost, India Today, The Hindu, etc.

### Low Credibility (0.3-0.5)
- Unknown sources, social media, blogs

You can extend this database in `app/core/pattern_detection.py` (see `CREDIBLE_SOURCES` dictionary).

## Testing

### Run Test Script

```bash
uv run python scripts/test_pattern_detection.py
```

This will:
1. Find all clusters in the database
2. Analyze the first cluster comprehensively
3. Analyze all clusters and show summary
4. Display high-risk clusters

### Manual Testing

```bash
# 1. Get cluster IDs
curl "http://localhost:2024/clustering/stats?hours=8760"

# 2. Analyze a specific cluster
curl "http://localhost:2024/pattern-detection/cluster/cluster_0"

# 3. Check for rapid growth
curl "http://localhost:2024/pattern-detection/cluster/cluster_0/rapid-growth?time_window_hours=6"

# 4. Check source credibility
curl "http://localhost:2024/pattern-detection/cluster/cluster_0/credibility"

# 5. Find contradictions
curl "http://localhost:2024/pattern-detection/cluster/cluster_0/contradictions"

# 6. Track evolution
curl "http://localhost:2024/pattern-detection/cluster/cluster_0/evolution"

# 7. Get all high-risk clusters
curl "http://localhost:2024/pattern-detection/high-risk-clusters?risk_threshold=0.6"
```

## Integration with LangGraph

The pattern detection service is ready to be integrated into a LangGraph workflow:

```python
from app.core.pattern_detection import PatternDetectionService
from app.dependencies import get_pattern_detection_service

def pattern_detection_node(state: AgentState) -> AgentState:
    """LangGraph node for pattern detection."""
    pattern_service = get_pattern_detection_service()
    
    # Analyze cluster from state
    cluster_id = state.get("cluster_id")
    analysis = pattern_service.analyze_cluster(cluster_id)
    
    # Add to state
    state["pattern_analysis"] = analysis
    state["risk_score"] = analysis["overall_risk_score"]
    
    return state
```

## Next Steps

1. **Fact-Checking**: External fact-checking organizations verify claims (already integrated)
2. **Classification**: Use pattern detection and fact-check results to classify misinformation (already integrated)
3. **Alerting**: Set up alerts for clusters with risk score > 0.7 (future enhancement)

## Troubleshooting

### No clusters found

Ensure you've run clustering first:
```bash
curl -X POST "http://localhost:2024/clustering/cluster?hours=8760"
```

### Low risk scores

- Check if datapoints have valid timestamps
- Verify source names are correctly stored
- Ensure clusters have enough datapoints (minimum 2)

### High false positives

- Adjust `rapid_growth_threshold` in `PatternDetectionService`
- Update `CREDIBLE_SOURCES` database with your sources
- Tune `similarity_threshold` for contradiction detection

