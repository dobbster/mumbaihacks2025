#!/bin/bash
# Script to ingest all topic-specific datapoint files for clustering testing

BASE_URL="http://localhost:2024/ingestion/datapoints"

echo "Ingesting datapoints for clustering testing..."
echo "=============================================="

# Health/Virus topic (4 datapoints)
echo -e "\n1. Ingesting Health/Virus topic (4 datapoints)..."
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_health_virus.json
echo -e "\n"

# Vaccines topic (4 datapoints)
echo "2. Ingesting Vaccines topic (4 datapoints)..."
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_vaccines.json
echo -e "\n"

# Emergency/Disaster topic (4 datapoints)
echo "3. Ingesting Emergency/Disaster topic (4 datapoints)..."
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_emergency_disaster.json
echo -e "\n"

# Health Guidelines topic (4 datapoints)
echo "4. Ingesting Health Guidelines topic (4 datapoints)..."
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_health_guidelines.json
echo -e "\n"

# Misinformation topic (4 datapoints)
echo "5. Ingesting Misinformation topic (4 datapoints)..."
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d @examples/datapoints_misinformation.json
echo -e "\n"

echo "=============================================="
echo "✅ All topics ingested!"
echo ""
echo "Total expected: 20 datapoints (4 per topic × 5 topics)"
echo ""
echo "Now test clustering:"
echo "  curl -X POST \"http://localhost:2024/clustering/cluster?hours=168&eps=0.4\""
echo "  uv run python scripts/test_clustering.py"

