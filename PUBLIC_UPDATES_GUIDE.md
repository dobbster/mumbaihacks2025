# Public Updates Guide

## Overview

The Public Updates Service generates user-friendly, JSON-formatted reports about misinformation detection. These updates are designed for public consumption and provide:

- Easy-to-understand summaries
- Key findings in plain language
- Actionable recommendations
- Evidence summaries
- Source links

## JSON Output Format

All endpoints return JSON with the following structure:

```json
{
  "status": "success",
  "update": {
    "update_id": "update_cluster_0_1234567890",
    "cluster_id": "cluster_0",
    "timestamp": "2025-11-29T04:30:00",
    "title": "⚠️ False Information Detected",
    "summary": "Fact-checking sources have verified that claims in this cluster are false. Confidence: 80%.",
    "status": "misinformation",
    "severity": "high",
    "explanation": "Our analysis has identified this cluster as containing misinformation. Key indicators include: rapid growth, contradictions, low credibility. We found 2 fact-checking source(s) that have analyzed these claims. 2 of these sources have verified the claims as false.",
    "key_findings": [
      "Identified as misinformation with high confidence",
      "Found 2 fact-checking source(s)",
      "Detected conflicting claims within the cluster"
    ],
    "recommendations": [
      "Do not share or amplify this information",
      "Verify information through official sources before believing",
      "Check fact-checking sources for detailed analysis"
    ],
    "credible_sources": ["BBC News", "Reuters", "AP News"],
    "fact_check_sources": [
      {
        "source": "AP News",
        "title": "Fact-checkers debunk viral claim...",
        "url": "https://apnews.com/...",
        "verdict": "false"
      }
    ],
    "evidence_summary": "2 fact-checking source(s) analyzed these claims. Cross-referenced with 3 credible source(s).",
    "confidence": 0.85,
    "risk_score": 0.75,
    "datapoint_count": 18,
    "sources": ["https://apnews.com/...", "https://bbc.com/..."],
    "related_clusters": []
  }
}
```

## API Endpoints

### GET `/public-updates/cluster/{cluster_id}`

Get a user-friendly update for a specific cluster.

**Parameters:**
- `use_llm` (bool, default: true): Use LLM for natural language generation

**Example:**
```bash
curl "http://localhost:2024/public-updates/cluster/cluster_0?use_llm=true"
```

**Response:** JSON-formatted update (see format above)

### GET `/public-updates/all`

Get updates for all clusters.

**Parameters:**
- `hours` (int, default: 168): Look back this many hours
- `min_cluster_size` (int, default: 2): Minimum cluster size
- `use_llm` (bool, default: false): Use LLM (slower but better quality)

**Example:**
```bash
curl "http://localhost:2024/public-updates/all?hours=168&use_llm=false"
```

**Response:**
```json
{
  "status": "success",
  "total_updates": 5,
  "updates": [
    {...},
    {...}
  ]
}
```

### GET `/public-updates/alerts`

Get alerts for high-confidence misinformation.

**Parameters:**
- `hours` (int, default: 168): Look back this many hours
- `min_confidence` (float, default: 0.7): Minimum confidence for alerts

**Example:**
```bash
curl "http://localhost:2024/public-updates/alerts?min_confidence=0.7"
```

**Response:**
```json
{
  "status": "success",
  "total_alerts": 3,
  "high_severity": 2,
  "medium_severity": 1,
  "low_severity": 0,
  "alerts": [
    {
      "title": "⚠️ False Information Detected",
      "summary": "...",
      "severity": "high",
      "confidence": 0.85,
      ...
    }
  ]
}
```

### GET `/public-updates/summary`

Get a high-level summary of all detected misinformation.

**Parameters:**
- `hours` (int, default: 168): Look back this many hours
- `min_cluster_size` (int, default: 2): Minimum cluster size

**Example:**
```bash
curl "http://localhost:2024/public-updates/summary?hours=168"
```

**Response:**
```json
{
  "status": "success",
  "summary": {
    "total_clusters_analyzed": 10,
    "misinformation_detected": 3,
    "legitimate_news": 5,
    "uncertain": 2,
    "severity_breakdown": {
      "high": 2,
      "medium": 1,
      "low": 0
    },
    "average_confidence": 0.72,
    "average_risk_score": 0.58
  },
  "top_alerts": [...],
  "timestamp": "2025-11-29T04:30:00"
}
```

### GET `/public-updates/feed`

Get a public feed of updates (RSS-like format).

**Parameters:**
- `hours` (int, default: 24): Look back this many hours
- `limit` (int, default: 10): Maximum number of updates
- `severity` (string, optional): Filter by "high", "medium", or "low"
- `status` (string, optional): Filter by "misinformation", "legitimate", or "uncertain"

**Example:**
```bash
# Get high-severity misinformation alerts
curl "http://localhost:2024/public-updates/feed?severity=high&status=misinformation&limit=5"
```

**Response:**
```json
{
  "status": "success",
  "feed": {
    "title": "Misinformation Detection Updates",
    "description": "Real-time updates on detected misinformation",
    "last_updated": "2025-11-29T04:30:00",
    "total_items": 5,
    "items": [
      {
        "title": "⚠️ False Information Detected",
        "summary": "...",
        "timestamp": "2025-11-29T04:30:00",
        ...
      }
    ]
  }
}
```

## Update Statuses

| Status | Meaning | When Used |
|--------|---------|-----------|
| **misinformation** | False information detected | Verification = false OR Classification = misinformation |
| **legitimate** | Verified legitimate news | Verification = verified OR Classification = legitimate |
| **uncertain** | Requires review | Classification = uncertain |
| **verified** | Information verified | Verification = verified |

## Severity Levels

| Severity | Meaning | Criteria |
|----------|---------|----------|
| **high** | Critical misinformation | High confidence (≥0.8) OR high risk score (≥0.7) |
| **medium** | Moderate concern | Medium confidence (0.5-0.8) OR medium risk (0.4-0.7) |
| **low** | Low concern | Low confidence (<0.5) OR low risk (<0.4) |

## LLM vs Template-Based Generation

### LLM Generation (`use_llm=true`)
- **Pros**: More natural language, better explanations
- **Cons**: Slower, requires API calls
- **Use When**: Need high-quality summaries for public consumption

### Template-Based (`use_llm=false`)
- **Pros**: Fast, consistent, no API calls
- **Cons**: Less natural, more structured
- **Use When**: Need quick updates, bulk generation

## Integration with Full Pipeline

The public update service integrates all previous steps:

```
1. Pattern Detection → 2. Classification → 3. Verification → 4. Public Update
```

It uses results from:
- **Pattern Detection**: Risk scores, flags, credibility analysis
- **Classification**: Misinformation status, confidence, key indicators
- **Verification**: Fact-check sources, cross-references, evidence

## Use Cases

### 1. Public Dashboard
```bash
# Get summary for dashboard
curl "http://localhost:2024/public-updates/summary"

# Get recent alerts
curl "http://localhost:2024/public-updates/alerts?hours=24"
```

### 2. RSS Feed
```bash
# Get feed for RSS readers
curl "http://localhost:2024/public-updates/feed?hours=24&limit=20"
```

### 3. Mobile App
```bash
# Get updates for mobile app
curl "http://localhost:2024/public-updates/all?hours=168&use_llm=false"
```

### 4. Alert System
```bash
# Get high-severity alerts
curl "http://localhost:2024/public-updates/alerts?min_confidence=0.8"
```

## Testing

### Test Script
```bash
uv run python scripts/test_public_updates.py
```

### Manual Testing
```bash
# 1. Get update for a cluster
curl "http://localhost:2024/public-updates/cluster/cluster_0"

# 2. Get all updates
curl "http://localhost:2024/public-updates/all?hours=8760"

# 3. Get alerts
curl "http://localhost:2024/public-updates/alerts?min_confidence=0.7"

# 4. Get summary
curl "http://localhost:2024/public-updates/summary"

# 5. Get feed
curl "http://localhost:2024/public-updates/feed?hours=24&limit=10"
```

## JSON Schema

The update JSON follows this schema:

```json
{
  "update_id": "string",
  "cluster_id": "string",
  "timestamp": "ISO datetime string",
  "title": "string (max 100 chars)",
  "summary": "string (1-2 sentences)",
  "status": "misinformation | legitimate | uncertain | verified",
  "severity": "high | medium | low",
  "explanation": "string (2-3 paragraphs)",
  "key_findings": ["string", ...],
  "recommendations": ["string", ...],
  "credible_sources": ["string", ...],
  "fact_check_sources": [
    {
      "source": "string",
      "title": "string",
      "url": "string",
      "verdict": "false | verified | disputed | unverified"
    }
  ],
  "evidence_summary": "string",
  "confidence": 0.0-1.0,
  "risk_score": 0.0-1.0,
  "datapoint_count": "integer",
  "sources": ["url", ...],
  "related_clusters": ["cluster_id", ...]
}
```

## Best Practices

1. **Use LLM for Public-Facing**: Use `use_llm=true` for public consumption
2. **Use Templates for Bulk**: Use `use_llm=false` for bulk generation
3. **Filter by Severity**: Use severity filters for alerts
4. **Check Confidence**: Only show high-confidence results to public
5. **Include Sources**: Always include source URLs for transparency

## Next Steps

After public updates:

1. ✅ **Public Updates** - DONE
2. ⏭️ **LangGraph Integration** - Orchestrate full workflow
3. ⏭️ **Frontend Dashboard** - Visualize updates
4. ⏭️ **Notification System** - Real-time alerts

