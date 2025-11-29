"""Public update service for generating user-friendly summaries and reports."""

import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.storage import StorageService
from app.core.pattern_detection import PatternDetectionService
from app.core.classification import ClassificationService
from app.core.verification import VerificationService, VerificationResult

logger = logging.getLogger(__name__)


class PublicUpdate(BaseModel):
    """Public-facing update about misinformation detection."""
    update_id: str = Field(description="Unique identifier for this update")
    cluster_id: str = Field(description="Cluster ID this update is about")
    timestamp: str = Field(description="ISO timestamp of update generation")
    
    # Summary
    title: str = Field(description="User-friendly title")
    summary: str = Field(description="Brief summary (1-2 sentences)")
    status: str = Field(description="'misinformation', 'legitimate', 'uncertain', or 'verified'")
    severity: str = Field(description="'high', 'medium', or 'low'")
    
    # Details
    explanation: str = Field(description="Easy-to-understand explanation")
    key_findings: List[str] = Field(description="Key findings in plain language")
    recommendations: List[str] = Field(description="Actionable recommendations for users")
    
    # Evidence
    credible_sources: List[str] = Field(description="List of credible sources")
    fact_check_sources: List[Dict[str, Any]] = Field(description="Fact-checking sources if available")
    evidence_summary: str = Field(description="Summary of evidence")
    
    # Metadata
    confidence: float = Field(description="Confidence score (0.0-1.0)")
    risk_score: float = Field(description="Risk score from pattern detection")
    datapoint_count: int = Field(description="Number of articles analyzed")
    
    # Links
    sources: List[str] = Field(description="URLs to source articles")
    related_clusters: List[str] = Field(description="Related cluster IDs")


class PublicUpdateService:
    """
    Service for generating user-friendly public updates about misinformation.
    
    Creates easy-to-understand summaries from:
    - Pattern detection results
    - Classification results
    - Verification results
    """
    
    def __init__(
        self,
        storage_service: StorageService,
        pattern_service: PatternDetectionService,
        classification_service: ClassificationService,
        verification_service: Optional[VerificationService] = None
    ):
        """
        Initialize public update service.
        
        Args:
            storage_service: Storage service
            pattern_service: Pattern detection service
            classification_service: Classification service
            verification_service: Optional verification service (if None, returns dummy verification results)
        """
        self.storage_service = storage_service
        self.pattern_service = pattern_service
        self.classification_service = classification_service
        self.verification_service = verification_service
    
    def _get_dummy_verification_result(self) -> VerificationResult:
        """Return a dummy verification result when verification service is not available."""
        return VerificationResult(
            is_verified=False,
            verification_status="unverified",
            confidence=0.0,
            fact_check_sources=[],
            cross_references=[],
            evidence_for=[],
            evidence_against=[],
            verification_summary="Verification not performed (service disabled)",
            sources=[]
        )
    
    def generate_update(
        self,
        cluster_id: str,
        use_llm: bool = True
    ) -> PublicUpdate:
        """
        Generate a public-facing update for a cluster.
        
        Args:
            cluster_id: Cluster to generate update for
            use_llm: Whether to use LLM for generating summaries (default: True)
            
        Returns:
            PublicUpdate with user-friendly information
        """
        logger.info(f"Generating public update for cluster {cluster_id}")
        
        # Get all analysis results
        pattern_analysis = self.pattern_service.analyze_cluster(cluster_id)
        cluster_datapoints = self.storage_service.get_datapoints_by_cluster(cluster_id)
        
        # Get classification
        classification_result = self.classification_service.classify_cluster(
            cluster_id,
            pattern_analysis,
            cluster_datapoints
        )
        
        # Get verification (or use dummy if service not available)
        if self.verification_service:
            verification_result = self.verification_service.verify_cluster(
                cluster_id,
                classification_result.model_dump()
            )
        else:
            verification_result = self._get_dummy_verification_result()
        
        # Generate update
        if use_llm:
            update = self._generate_update_with_llm(
                cluster_id,
                pattern_analysis,
                classification_result,
                verification_result,
                cluster_datapoints
            )
        else:
            update = self._generate_update_simple(
                cluster_id,
                pattern_analysis,
                classification_result,
                verification_result,
                cluster_datapoints
            )
        
        return update
    
    def _generate_update_with_llm(
        self,
        cluster_id: str,
        pattern_analysis: Dict[str, Any],
        classification_result: Any,
        verification_result: Any,
        cluster_datapoints: List[Dict[str, Any]]
    ) -> PublicUpdate:
        """Generate update using LLM for natural language generation."""
        # Build prompt for LLM
        prompt = self._build_update_prompt(
            cluster_id,
            pattern_analysis,
            classification_result,
            verification_result,
            cluster_datapoints
        )
        
        # Call LLM (reuse classification service's LLM)
        try:
            # Access LLM from classification service
            llm = self.classification_service.llm
            response = llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Parse LLM response
            update_data = self._parse_llm_update_response(content)
            
            # Merge with structured data
            return self._merge_update_data(
                cluster_id,
                pattern_analysis,
                classification_result,
                verification_result,
                cluster_datapoints,
                update_data
            )
        except Exception as e:
            logger.warning(f"LLM update generation failed, using simple method: {e}")
            return self._generate_update_simple(
                cluster_id,
                pattern_analysis,
                classification_result,
                verification_result,
                cluster_datapoints
            )
    
    def _generate_update_simple(
        self,
        cluster_id: str,
        pattern_analysis: Dict[str, Any],
        classification_result: Any,
        verification_result: Any,
        cluster_datapoints: List[Dict[str, Any]]
    ) -> PublicUpdate:
        """Generate update without LLM (structured template-based)."""
        # Determine status and severity
        status, severity = self._determine_status_severity(
            classification_result,
            verification_result,
            pattern_analysis
        )
        
        # Generate title
        title = self._generate_title(
            classification_result,
            verification_result,
            cluster_datapoints
        )
        
        # Generate summary
        summary = self._generate_summary(
            classification_result,
            verification_result,
            pattern_analysis
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            pattern_analysis,
            classification_result,
            verification_result
        )
        
        # Extract key findings
        key_findings = self._extract_key_findings(
            pattern_analysis,
            classification_result,
            verification_result
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            status,
            severity,
            verification_result
        )
        
        # Extract sources
        credible_sources = pattern_analysis.get("credibility_analysis", {}).get("credible_sources", [])
        fact_check_sources = verification_result.fact_check_sources
        sources = verification_result.sources
        
        # Evidence summary
        evidence_summary = self._generate_evidence_summary(
            verification_result,
            pattern_analysis
        )
        
        # Related clusters (find similar clusters)
        related_clusters = self._find_related_clusters(cluster_id)
        
        return PublicUpdate(
            update_id=f"update_{cluster_id}_{int(datetime.utcnow().timestamp())}",
            cluster_id=cluster_id,
            timestamp=datetime.utcnow().isoformat(),
            title=title,
            summary=summary,
            status=status,
            severity=severity,
            explanation=explanation,
            key_findings=key_findings,
            recommendations=recommendations,
            credible_sources=credible_sources,
            fact_check_sources=fact_check_sources[:5],  # Limit to top 5
            evidence_summary=evidence_summary,
            confidence=classification_result.confidence,
            risk_score=pattern_analysis.get("overall_risk_score", 0.0),
            datapoint_count=len(cluster_datapoints),
            sources=sources[:10],  # Limit to top 10
            related_clusters=related_clusters
        )
    
    def _build_update_prompt(
        self,
        cluster_id: str,
        pattern_analysis: Dict[str, Any],
        classification_result: Any,
        verification_result: Any,
        cluster_datapoints: List[Dict[str, Any]]
    ) -> str:
        """Build prompt for LLM to generate user-friendly update."""
        # Sample titles
        sample_titles = [dp.get("title", "")[:80] for dp in cluster_datapoints[:5]]
        
        prompt = f"""You are a public information officer creating a user-friendly update about misinformation detection.

## Cluster Analysis Results

**Cluster ID**: {cluster_id}
**Number of Articles**: {len(cluster_datapoints)}

**Classification**: {classification_result.classification}
**Confidence**: {classification_result.confidence:.2f}
**Is Misinformation**: {classification_result.is_misinformation}

**Verification Status**: {verification_result.verification_status}
**Verification Confidence**: {verification_result.confidence:.2f}

**Risk Score**: {pattern_analysis.get('overall_risk_score', 0.0):.2f}
**Risk Level**: {pattern_analysis.get('risk_level', 'unknown')}

**Key Indicators**:
{chr(10).join(f"- {ind}" for ind in classification_result.key_indicators[:5])}

**Sample Article Titles**:
{chr(10).join(f"- {title}" for title in sample_titles)}

**Fact-Check Sources**: {len(verification_result.fact_check_sources)}
**Credible Sources**: {len(pattern_analysis.get('credibility_analysis', {}).get('credible_sources', []))}

## Your Task

Create a user-friendly public update in JSON format. The update should:
1. Be easy to understand (avoid technical jargon)
2. Clearly explain what was found
3. Provide actionable recommendations
4. Be concise but informative

## Output Format

Respond with a JSON object:

```json
{{
    "title": "User-friendly title (max 100 chars)",
    "summary": "Brief 1-2 sentence summary",
    "explanation": "Detailed but easy-to-understand explanation (2-3 paragraphs)",
    "key_findings": [
        "Finding 1 in plain language",
        "Finding 2 in plain language"
    ],
    "recommendations": [
        "Actionable recommendation 1",
        "Actionable recommendation 2"
    ],
    "evidence_summary": "Summary of evidence in plain language"
}}
```

## Guidelines

- **Title**: Should be clear and attention-grabbing
- **Summary**: One sentence that captures the essence
- **Explanation**: Explain what was found and why it matters
- **Key Findings**: 3-5 bullet points of important findings
- **Recommendations**: 2-4 actionable steps users can take
- **Evidence Summary**: Brief summary of supporting evidence

**Tone**: Professional but accessible, informative but not alarmist.

Now generate the public update in JSON format.
"""
        return prompt
    
    def _parse_llm_update_response(self, content: str) -> Dict[str, Any]:
        """Parse LLM response for update data."""
        import json
        import re
        
        # Try to extract JSON
        json_str = None
        
        # Strategy 1: Extract from markdown code blocks
        code_block_pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
        match = re.search(code_block_pattern, content, re.DOTALL)
        if match:
            potential_json = match.group(1).strip()
            # Find JSON object
            brace_count = 0
            start_idx = -1
            for i, char in enumerate(potential_json):
                if char == '{':
                    if start_idx == -1:
                        start_idx = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_idx != -1:
                        json_str = potential_json[start_idx:i+1]
                        break
        
        # Strategy 2: Find JSON object in content
        if not json_str:
            brace_count = 0
            start_idx = -1
            for i, char in enumerate(content):
                if char == '{':
                    if start_idx == -1:
                        start_idx = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_idx != -1:
                        json_str = content[start_idx:i+1]
                        break
        
        if json_str:
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Fallback: return empty dict
        return {}
    
    def _merge_update_data(
        self,
        cluster_id: str,
        pattern_analysis: Dict[str, Any],
        classification_result: Any,
        verification_result: Any,
        cluster_datapoints: List[Dict[str, Any]],
        llm_data: Dict[str, Any]
    ) -> PublicUpdate:
        """Merge LLM-generated data with structured data."""
        # Determine status and severity
        status, severity = self._determine_status_severity(
            classification_result,
            verification_result,
            pattern_analysis
        )
        
        # Use LLM data if available, otherwise use defaults
        title = llm_data.get("title") or self._generate_title(
            classification_result, verification_result, cluster_datapoints
        )
        summary = llm_data.get("summary") or self._generate_summary(
            classification_result, verification_result, pattern_analysis
        )
        explanation = llm_data.get("explanation") or self._generate_explanation(
            pattern_analysis, classification_result, verification_result
        )
        key_findings = llm_data.get("key_findings") or self._extract_key_findings(
            pattern_analysis, classification_result, verification_result
        )
        recommendations = llm_data.get("recommendations") or self._generate_recommendations(
            status, severity, verification_result
        )
        evidence_summary = llm_data.get("evidence_summary") or self._generate_evidence_summary(
            verification_result, pattern_analysis
        )
        
        # Extract sources
        credible_sources = pattern_analysis.get("credibility_analysis", {}).get("credible_sources", [])
        fact_check_sources = verification_result.fact_check_sources
        sources = verification_result.sources
        related_clusters = self._find_related_clusters(cluster_id)
        
        return PublicUpdate(
            update_id=f"update_{cluster_id}_{int(datetime.utcnow().timestamp())}",
            cluster_id=cluster_id,
            timestamp=datetime.utcnow().isoformat(),
            title=title,
            summary=summary,
            status=status,
            severity=severity,
            explanation=explanation,
            key_findings=key_findings,
            recommendations=recommendations,
            credible_sources=credible_sources,
            fact_check_sources=fact_check_sources[:5],
            evidence_summary=evidence_summary,
            confidence=classification_result.confidence,
            risk_score=pattern_analysis.get("overall_risk_score", 0.0),
            datapoint_count=len(cluster_datapoints),
            sources=sources[:10],
            related_clusters=related_clusters
        )
    
    def _determine_status_severity(
        self,
        classification_result: Any,
        verification_result: Any,
        pattern_analysis: Dict[str, Any]
    ) -> Tuple[str, str]:
        """Determine status and severity."""
        # Priority: verification > classification > pattern analysis
        if verification_result.verification_status == "false":
            status = "misinformation"
            severity = "high" if verification_result.confidence >= 0.8 else "medium"
        elif verification_result.verification_status == "verified":
            status = "legitimate"
            severity = "low"
        elif classification_result.is_misinformation:
            status = "misinformation"
            severity = "high" if classification_result.confidence >= 0.7 else "medium"
        elif classification_result.classification == "uncertain":
            status = "uncertain"
            severity = "medium"
        else:
            status = "legitimate"
            severity = "low"
        
        # Adjust severity based on risk score
        risk_score = pattern_analysis.get("overall_risk_score", 0.0)
        if risk_score >= 0.7 and severity != "high":
            severity = "high"
        elif risk_score < 0.4 and severity == "high":
            severity = "medium"
        
        return status, severity
    
    def _generate_title(
        self,
        classification_result: Any,
        verification_result: Any,
        cluster_datapoints: List[Dict[str, Any]]
    ) -> str:
        """Generate user-friendly title."""
        if verification_result.verification_status == "false":
            return "⚠️ False Information Detected"
        elif verification_result.verification_status == "verified":
            return "✅ Information Verified"
        elif classification_result.is_misinformation:
            return "⚠️ Potential Misinformation Detected"
        elif classification_result.classification == "uncertain":
            return "❓ Information Requires Review"
        else:
            return "📰 News Cluster Analysis"
    
    def _generate_summary(
        self,
        classification_result: Any,
        verification_result: Any,
        pattern_analysis: Dict[str, Any]
    ) -> str:
        """Generate brief summary."""
        if verification_result.verification_status == "false":
            return f"Fact-checking sources have verified that claims in this cluster are false. Confidence: {verification_result.confidence*100:.0f}%."
        elif verification_result.verification_status == "verified":
            return f"Information in this cluster has been verified by credible sources. Confidence: {verification_result.confidence*100:.0f}%."
        elif classification_result.is_misinformation:
            return f"Our analysis indicates this cluster contains misinformation. Confidence: {classification_result.confidence*100:.0f}%."
        else:
            return f"Analysis of {pattern_analysis.get('datapoint_count', 0)} articles shows this appears to be legitimate news coverage."
    
    def _generate_explanation(
        self,
        pattern_analysis: Dict[str, Any],
        classification_result: Any,
        verification_result: Any
    ) -> str:
        """Generate detailed explanation."""
        parts = []
        
        # Classification explanation
        if classification_result.is_misinformation:
            parts.append("Our analysis has identified this cluster as containing misinformation.")
            parts.append(f"Key indicators include: {', '.join(classification_result.key_indicators[:3])}.")
        else:
            parts.append("Our analysis indicates this cluster contains legitimate news coverage.")
        
        # Verification explanation
        if verification_result.fact_check_sources:
            fc_count = len(verification_result.fact_check_sources)
            parts.append(f"We found {fc_count} fact-checking source(s) that have analyzed these claims.")
            false_count = sum(1 for fc in verification_result.fact_check_sources if fc.get("verdict") == "false")
            if false_count > 0:
                parts.append(f"{false_count} of these sources have verified the claims as false.")
        
        # Pattern analysis explanation
        flags = pattern_analysis.get("flags", {})
        if flags.get("has_contradictions"):
            parts.append("We detected conflicting claims within this cluster, which is a common indicator of misinformation.")
        
        if flags.get("low_credibility"):
            parts.append("The cluster contains a high proportion of low-credibility sources.")
        
        return " ".join(parts)
    
    def _extract_key_findings(
        self,
        pattern_analysis: Dict[str, Any],
        classification_result: Any,
        verification_result: Any
    ) -> List[str]:
        """Extract key findings in plain language."""
        findings = []
        
        # Classification findings
        if classification_result.is_misinformation:
            findings.append("Identified as misinformation with high confidence")
        else:
            findings.append("Appears to be legitimate news coverage")
        
        # Verification findings
        if verification_result.fact_check_sources:
            findings.append(f"Found {len(verification_result.fact_check_sources)} fact-checking source(s)")
        
        # Pattern findings
        flags = pattern_analysis.get("flags", {})
        if flags.get("has_contradictions"):
            findings.append("Detected conflicting claims within the cluster")
        if flags.get("rapid_growth"):
            findings.append("Rapid spread detected (potential misinformation indicator)")
        
        # Credibility findings
        credibility = pattern_analysis.get("credibility_analysis", {})
        credible_ratio = credibility.get("credible_ratio", 0.0)
        if credible_ratio >= 0.7:
            findings.append("High proportion of credible sources")
        elif credible_ratio < 0.3:
            findings.append("Low proportion of credible sources")
        
        return findings[:5]  # Limit to 5 findings
    
    def _generate_recommendations(
        self,
        status: str,
        severity: str,
        verification_result: Any
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if status == "misinformation":
            recommendations.append("Do not share or amplify this information")
            recommendations.append("Verify information through official sources before believing")
            if verification_result.fact_check_sources:
                recommendations.append("Check fact-checking sources for detailed analysis")
            recommendations.append("Report misinformation to platform moderators if encountered")
        elif status == "uncertain":
            recommendations.append("Exercise caution when sharing this information")
            recommendations.append("Wait for official verification before taking action")
            recommendations.append("Check multiple credible sources for confirmation")
        else:
            recommendations.append("Information appears legitimate, but always verify through official sources")
            recommendations.append("Stay informed through credible news outlets")
        
        return recommendations
    
    def _generate_evidence_summary(
        self,
        verification_result: Any,
        pattern_analysis: Dict[str, Any]
    ) -> str:
        """Generate evidence summary."""
        parts = []
        
        if verification_result.fact_check_sources:
            parts.append(f"{len(verification_result.fact_check_sources)} fact-checking source(s) analyzed these claims.")
        
        if verification_result.cross_references:
            parts.append(f"Cross-referenced with {len(verification_result.cross_references)} credible source(s).")
        
        if verification_result.evidence_against:
            parts.append(f"Found {len(verification_result.evidence_against)} piece(s) of contradicting evidence.")
        
        if verification_result.evidence_for:
            parts.append(f"Found {len(verification_result.evidence_for)} piece(s) of supporting evidence.")
        
        return " ".join(parts) if parts else "Evidence analysis completed."
    
    def _find_related_clusters(self, cluster_id: str) -> List[str]:
        """Find related clusters (placeholder - could use similarity search)."""
        # For now, return empty list
        # In future, could use embedding similarity to find related clusters
        return []
    
    def generate_updates_for_all_clusters(
        self,
        hours: int = 168,
        min_cluster_size: int = 2,
        use_llm: bool = True
    ) -> List[PublicUpdate]:
        """Generate updates for all clusters."""
        # Get all clusters
        pattern_results = self.pattern_service.analyze_all_clusters(hours, min_cluster_size)
        analyses = pattern_results.get("analyses", {})
        
        updates = []
        for cluster_id in analyses.keys():
            try:
                update = self.generate_update(cluster_id, use_llm=use_llm)
                updates.append(update)
            except Exception as e:
                logger.error(f"Failed to generate update for {cluster_id}: {e}", exc_info=True)
        
        return updates
    
    def generate_misinformation_alerts(
        self,
        hours: int = 168,
        min_confidence: float = 0.7
    ) -> List[PublicUpdate]:
        """Generate alerts for high-confidence misinformation."""
        updates = self.generate_updates_for_all_clusters(hours, min_cluster_size=2, use_llm=False)
        
        # Filter for misinformation with high confidence
        alerts = [
            update for update in updates
            if update.status == "misinformation" and update.confidence >= min_confidence
        ]
        
        # Sort by severity and confidence
        alerts.sort(key=lambda x: (
            0 if x.severity == "high" else 1 if x.severity == "medium" else 2,
            -x.confidence
        ))
        
        return alerts

