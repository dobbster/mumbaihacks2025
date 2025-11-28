# Verification Guide

## Overview

The Verification Service provides fact-checking and cross-referencing capabilities to verify claims and clusters. It:

1. **Finds Fact-Checking Sources**: Searches for fact-checking articles in the cluster
2. **Cross-References**: Compares with credible sources
3. **Analyzes Evidence**: Identifies supporting and contradicting evidence
4. **Provides Verification Status**: Returns verified/false/partially_true/unverified/disputed
5. **Builds Evidence Chains**: Creates transparent verification reasoning

## How It Works

### 1. Fact-Checking Source Detection

The service identifies fact-checking sources by:
- **Source Name**: Checks if source is a known fact-checker (Snopes, PolitiFact, etc.)
- **Keywords**: Looks for fact-check keywords ("fact check", "debunked", "verified", etc.)
- **Categories**: Checks for "fact_check" category in datapoints

### 2. Verdict Extraction

Extracts verdicts from fact-check articles:
- **"false"**: Claim is false/misinformation
- **"verified"**: Claim is verified as true
- **"disputed"**: Claim is disputed/unclear
- **"unverified"**: No clear verdict

### 3. Cross-Referencing

Cross-references with credible sources (credibility ≥ 0.7):
- Groups articles by credible source
- Analyzes consistency across sources
- Identifies supporting/contradicting evidence

### 4. Evidence Analysis

Analyzes evidence for and against claims:
- Counts fact-check verdicts
- Checks for false/verified indicators in titles
- Compares evidence for vs. against

### 5. Verification Status

Determines verification status based on:
- Fact-check verdicts (highest weight)
- Credible source cross-references (medium weight)
- Classification results (lower weight)

## Verification Statuses

| Status | Meaning | Confidence Range |
|--------|---------|------------------|
| **verified** | Claim is verified as true | 0.7-0.9 |
| **false** | Claim is false/misinformation | 0.7-0.9 |
| **partially_true** | Claim is partially true | 0.6-0.8 |
| **disputed** | Claim is disputed/unclear | 0.5-0.7 |
| **unverified** | Cannot verify claim | 0.3-0.5 |

## API Endpoints

### POST `/verification/cluster/{cluster_id}`

Verify a specific cluster.

**Parameters:**
- `include_classification` (bool, default: true): Include classification results

**Example:**
```bash
curl -X POST "http://localhost:2024/verification/cluster/cluster_0?include_classification=true"
```

**Response:**
```json
{
  "status": "success",
  "cluster_id": "cluster_0",
  "verification": {
    "is_verified": false,
    "verification_status": "false",
    "confidence": 0.8,
    "fact_check_sources": [
      {
        "source": "AP News",
        "title": "Fact-checkers debunk viral claim...",
        "url": "https://apnews.com/fact-check...",
        "verdict": "false",
        "relevance": "high"
      }
    ],
    "cross_references": [
      {
        "source": "BBC News",
        "count": 2,
        "credibility": 0.95,
        "articles": [...]
      }
    ],
    "evidence_for": [...],
    "evidence_against": [
      "2 fact-checking source(s) indicate the claim is false"
    ],
    "verification_summary": "Verification Status: FALSE. Found 2 fact-checking source(s)...",
    "sources": ["https://apnews.com/...", "https://bbc.com/..."]
  },
  "evidence_chain": [...],
  "classification": {...}
}
```

### POST `/verification/claim`

Verify a specific claim.

**Parameters:**
- `claim` (string, required): The claim to verify
- `context` (string, optional): Context about the claim

**Example:**
```bash
curl -X POST "http://localhost:2024/verification/claim?claim=Vaccines%20cause%20autism&context=Health%20misinformation"
```

**Response:**
```json
{
  "status": "success",
  "claim": "Vaccines cause autism",
  "verification": {
    "is_verified": false,
    "verification_status": "false",
    "confidence": 0.7,
    "verification_summary": "..."
  }
}
```

### POST `/verification/verify-all`

Verify all clusters.

**Parameters:**
- `hours` (int, default: 168): Look back this many hours
- `min_cluster_size` (int, default: 2): Minimum cluster size
- `include_classification` (bool, default: true): Include classification

**Example:**
```bash
curl -X POST "http://localhost:2024/verification/verify-all?hours=168&min_cluster_size=2"
```

**Response:**
```json
{
  "status": "success",
  "summary": {
    "total_clusters_verified": 5,
    "verified": 1,
    "false": 2,
    "unverified": 2,
    "average_confidence": 0.65
  },
  "verifications": {...}
}
```

### GET `/verification/verified-clusters`

Get all clusters with high-confidence verification.

**Parameters:**
- `hours` (int, default: 168): Look back this many hours
- `min_confidence` (float, default: 0.7): Minimum confidence score

**Example:**
```bash
curl "http://localhost:2024/verification/verified-clusters?min_confidence=0.7"
```

**Response:**
```json
{
  "status": "success",
  "verified_clusters": [
    {
      "cluster_id": "cluster_0",
      "verification_status": "false",
      "confidence": 0.8,
      "is_verified": false,
      "summary": "...",
      "fact_check_count": 2,
      "cross_reference_count": 3
    }
  ],
  "count": 1,
  "min_confidence": 0.7
}
```

## Fact-Checking Sources

The system recognizes these fact-checking organizations:
- Snopes
- PolitiFact
- FactCheck.org
- AFP Fact Check
- Reuters Fact Check
- AP Fact Check

## Cross-Referencing

Credible sources (credibility ≥ 0.7) are used for cross-referencing:
- BBC News (0.95)
- Reuters (0.95)
- AP News (0.95)
- CNN (0.90)
- The Guardian (0.90)
- And more...

## Integration with Classification

The verification service can use classification results to:
- Enhance verification confidence
- Provide additional context
- Cross-validate findings

Set `include_classification=true` to enable this.

## Evidence Chain

The evidence chain shows:
1. **Fact-Check Sources** (weight: 0.4)
2. **Cross-References** (weight: 0.3)
3. **Evidence Analysis** (weight: 0.3)

Each step includes:
- Description
- Sources
- Weight (importance)

## Future Enhancements

### Web Search Integration

Currently, the service analyzes existing datapoints. Future enhancements could include:

1. **Tavily Search Integration**: Search for fact-checking articles in real-time
2. **Google Fact Check API**: Integrate with Google's fact-check database
3. **Custom Fact-Check Database**: Build a database of verified claims

### Example Integration:

```python
# Future: Integrate with Tavily search
def _search_fact_check_articles(self, claim_text: str):
    """Search for fact-checking articles using Tavily."""
    from tavily import TavilyClient
    
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(
        query=f"fact check {claim_text}",
        search_depth="advanced",
        include_domains=["snopes.com", "politifact.com", "factcheck.org"]
    )
    return results
```

## Testing

### Test Script

```bash
uv run python scripts/test_verification.py
```

### Manual Testing

```bash
# 1. Verify a specific cluster
curl -X POST "http://localhost:2024/verification/cluster/cluster_0"

# 2. Verify a claim
curl -X POST "http://localhost:2024/verification/claim?claim=Vaccines%20are%20safe"

# 3. Verify all clusters
curl -X POST "http://localhost:2024/verification/verify-all?hours=8760"

# 4. Get verified clusters
curl "http://localhost:2024/verification/verified-clusters?min_confidence=0.7"
```

## Workflow Integration

The verification service integrates with the full pipeline:

```
1. Ingestion → 2. Clustering → 3. Pattern Detection → 4. Classification → 5. Verification
```

Verification uses results from:
- **Pattern Detection**: Source credibility, contradictions
- **Classification**: Misinformation classification, confidence
- **Storage**: All datapoints in cluster

## Best Practices

1. **Use Classification**: Include classification results for better verification
2. **Check Fact-Check Sources**: Prioritize clusters with fact-checking sources
3. **Cross-Reference**: Verify against multiple credible sources
4. **Review Evidence Chain**: Check the evidence chain for transparency
5. **Confidence Thresholds**: Use min_confidence=0.7 for high-confidence results

## Troubleshooting

### No Fact-Check Sources Found

- Ensure datapoints include fact-checking articles
- Check if sources are recognized (see FACT_CHECK_SOURCES)
- Verify categories include "fact_check"

### Low Confidence Scores

- Check if cluster has enough datapoints
- Verify credible sources are present
- Consider including classification results

### Unverified Status

- May indicate insufficient evidence
- Check if fact-check sources are present
- Review evidence_for vs evidence_against

