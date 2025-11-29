# Classification Guide

## Overview

The Classification Service uses **Together AI LLM** to analyze pattern detection results and classify clusters as **misinformation**, **legitimate**, or **uncertain**.

## Recommended LLM Model

### **Meta-Llama-3.1-8B-Instruct-Turbo** (Default)

**Why this model?**
- ✅ **Fast**: 8B parameters = quick responses
- ✅ **Good for classification**: Instruction-tuned for structured tasks
- ✅ **Cost-effective**: Lower cost per token
- ✅ **Reliable**: Stable outputs for classification
- ✅ **Supports JSON**: Can return structured responses

**Model Name**: `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`

### Alternative Models

If you need better reasoning (but slower):

1. **Meta-Llama-3.1-70B-Instruct-Turbo** (Balanced)
   - Better reasoning capabilities
   - Slower but more accurate
   - Model: `meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo`

2. **Mixtral-8x7B-Instruct** (Best Reasoning)
   - Best for complex analysis
   - Slower and more expensive
   - Model: `mistralai/Mixtral-8x7B-Instruct-v0.1`

## Configuration

Set the model in your `.env` file:

```bash
# Together AI Configuration
TOGETHER_API_KEY=your_api_key_here
TOGETHER_LLM_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
```

Or use the default (8B model).

## Classification Prompt Design

The classification prompt is designed to:

1. **Analyze Pattern Detection Results**: All 4 factors (growth, credibility, contradictions, evolution)
2. **Provide Binary Classification**: Misinformation vs Legitimate
3. **Assign Confidence Score**: 0.0-1.0 with clear guidelines
4. **Build Evidence Chain**: Transparent reasoning with weighted evidence
5. **Identify Key Indicators**: What led to the classification

### Prompt Structure

```
1. Cluster Information (ID, size, risk score)
2. Pattern Detection Results (all 4 factors)
3. Red Flags Summary
4. Sample Article Titles
5. Classification Task
6. Classification Criteria
7. Output Format (JSON)
8. Confidence Scoring Guidelines
9. Evidence Chain Instructions
```

### Key Features

- **Conservative Approach**: When uncertain, classify as "uncertain"
- **Context Awareness**: Considers legitimate scenarios (breaking news, debates)
- **Structured Output**: JSON format for easy parsing
- **Transparency**: Evidence chain shows reasoning

## Confidence Scoring Guidelines

The prompt instructs the LLM to use these confidence levels:

| Confidence Range | Meaning | Use Case |
|-----------------|---------|----------|
| **0.9-1.0** | Very High | Clear misinformation or clearly legitimate |
| **0.7-0.9** | High | Strong evidence one way or the other |
| **0.5-0.7** | Moderate | Mixed signals, some uncertainty |
| **0.3-0.5** | Low | Uncertain, needs human review |
| **0.0-0.3** | Very Low | Insufficient data |

## Evidence Chain Structure

Each evidence step includes:

```json
{
    "step": 1,
    "evidence": "Description of evidence",
    "weight": 0.0-1.0,
    "indicator": "rapid_growth" | "low_credibility" | "contradictions" | "evolution" | "other"
}
```

The evidence chain:
- Starts with strongest evidence
- Each step builds on previous steps
- Weighted by importance (0.0-1.0)
- Linked to specific indicators

## API Endpoints

### POST `/classification/cluster/{cluster_id}`

Classify a specific cluster.

**Example:**
```bash
curl -X POST "http://localhost:2024/classification/cluster/cluster_0"
```

**Response:**
```json
{
  "status": "success",
  "cluster_id": "cluster_0",
  "classification": {
    "is_misinformation": true,
    "confidence": 0.85,
    "classification": "misinformation",
    "evidence_chain": [...],
    "key_indicators": [
      "Rapid growth detected (3.5x in 6 hours)",
      "Multiple contradictions found (5 pairs)",
      "Low credible source ratio (0.3)"
    ],
    "reasoning": "Detailed explanation...",
    "supporting_evidence": [...],
    "contradictory_evidence": [...]
  },
  "pattern_analysis": {...}
}
```

### POST `/classification/analyze-all`

Classify all clusters.

**Example:**
```bash
curl -X POST "http://localhost:2024/classification/analyze-all?hours=168&min_cluster_size=2"
```

**Response:**
```json
{
  "status": "success",
  "summary": {
    "total_clusters_classified": 5,
    "misinformation": 2,
    "legitimate": 2,
    "uncertain": 1,
    "average_confidence": 0.72
  },
  "classifications": {...}
}
```

### GET `/classification/misinformation-clusters`

Get all high-confidence misinformation clusters.

**Example:**
```bash
curl "http://localhost:2024/classification/misinformation-clusters?min_confidence=0.7"
```

**Response:**
```json
{
  "status": "success",
  "misinformation_clusters": [
    {
      "cluster_id": "cluster_0",
      "confidence": 0.85,
      "classification": "misinformation",
      "key_indicators": [...],
      "reasoning": "...",
      "risk_score": 0.75,
      "datapoint_count": 18
    }
  ],
  "count": 1,
  "min_confidence": 0.7
}
```

## Testing

### Test Script

```bash
uv run python scripts/test_classification.py
```

This will:
1. Find clusters in the database
2. Run pattern detection
3. Classify using LLM
4. Display results

### Manual Testing

```bash
# 1. Classify a specific cluster
curl -X POST "http://localhost:2024/classification/cluster/cluster_0"

# 2. Classify all clusters
curl -X POST "http://localhost:2024/classification/analyze-all?hours=8760"

# 3. Get misinformation clusters
curl "http://localhost:2024/classification/misinformation-clusters?min_confidence=0.7"
```

## Integration with Pattern Detection

The classification service automatically:

1. **Receives Pattern Analysis**: From `PatternDetectionService.analyze_cluster()`
2. **Builds Comprehensive Prompt**: Includes all pattern detection results
3. **Calls LLM**: Uses Together AI to analyze
4. **Parses Response**: Extracts JSON classification result
5. **Returns Structured Result**: `ClassificationResult` with all fields

## Error Handling

- **JSON Parse Failure**: Falls back to text extraction
- **LLM Error**: Returns "uncertain" classification with error details
- **Missing Data**: Handles gracefully with default values

## Next Steps

After classification:

1. **Verification**: Cross-reference with fact-checking databases
2. **Public Updates**: Generate user-friendly summaries
3. **Alerting**: Notify when high-confidence misinformation detected
4. **Human Review**: Queue uncertain classifications for review

## Troubleshooting

### LLM Not Responding

- Check `TOGETHER_API_KEY` is set
- Verify model name is correct
- Check API quota/limits

### Low Confidence Scores

- Ensure pattern detection has enough data
- Check if clusters have sufficient datapoints
- Verify pattern detection is working correctly

### JSON Parse Errors

- The service falls back to text extraction
- Check LLM response format
- Consider using a model with better JSON support

