"""Verification service for fact-checking and cross-referencing claims."""

import logging
import os
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.storage import StorageService
from app.core.pattern_detection import FACT_CHECK_SOURCES, CREDIBLE_SOURCES

logger = logging.getLogger(__name__)


class VerificationResult(BaseModel):
    """Result of verification for a claim or cluster."""
    is_verified: bool = Field(description="Whether the claim is verified as true")
    verification_status: str = Field(description="'verified', 'false', 'partially_true', 'unverified', or 'disputed'")
    confidence: float = Field(description="Confidence in verification (0.0 to 1.0)")
    fact_check_sources: List[Dict[str, Any]] = Field(description="Fact-checking sources found")
    cross_references: List[Dict[str, Any]] = Field(description="Cross-references with credible sources")
    evidence_for: List[str] = Field(description="Evidence supporting the claim")
    evidence_against: List[str] = Field(description="Evidence contradicting the claim")
    verification_summary: str = Field(description="Summary of verification findings")
    sources: List[str] = Field(description="URLs of verification sources")


class VerificationService:
    """
    Service for verifying claims through fact-checking and cross-referencing.
    
    Methods:
    1. Search for fact-checking articles
    2. Cross-reference with credible sources
    3. Check against known fact-checking databases
    4. Build verification evidence chains
    5. Provide verification scores
    """
    
    # Fact-checking keywords to search for
    FACT_CHECK_KEYWORDS = [
        "fact check", "fact-check", "debunked", "verified", "false", "unfounded",
        "misinformation", "disinformation", "hoax", "rumor", "claim", "verified claim",
        "snopes", "politifact", "factcheck", "full fact", "afp fact check"
    ]
    
    # Keywords indicating false claims
    FALSE_INDICATORS = [
        "false", "debunked", "unfounded", "incorrect", "wrong", "misleading",
        "hoax", "fabricated", "not true", "disproven", "refuted"
    ]
    
    # Keywords indicating verified claims
    VERIFIED_INDICATORS = [
        "verified", "confirmed", "true", "accurate", "correct", "factual",
        "validated", "authenticated", "substantiated"
    ]
    
    def __init__(self, storage_service: StorageService):
        """
        Initialize verification service.
        
        Args:
            storage_service: Storage service for accessing datapoints
        """
        self.storage_service = storage_service
    
    def verify_cluster(
        self,
        cluster_id: str,
        classification_result: Optional[Dict[str, Any]] = None
    ) -> VerificationResult:
        """
        Verify a cluster by fact-checking and cross-referencing.
        
        Args:
            cluster_id: Cluster to verify
            classification_result: Optional classification result for context
            
        Returns:
            VerificationResult with verification status and evidence
        """
        logger.info(f"Verifying cluster {cluster_id}")
        
        # Get cluster datapoints
        cluster_datapoints = self.storage_service.get_datapoints_by_cluster(cluster_id)
        
        if not cluster_datapoints:
            return VerificationResult(
                is_verified=False,
                verification_status="unverified",
                confidence=0.0,
                fact_check_sources=[],
                cross_references=[],
                evidence_for=[],
                evidence_against=[],
                verification_summary="No datapoints found in cluster",
                sources=[]
            )
        
        # Extract key claims from cluster
        key_claims = self._extract_key_claims(cluster_datapoints)
        
        # Search for fact-checking sources
        fact_check_sources = self._find_fact_check_sources(cluster_datapoints, key_claims)
        
        # Cross-reference with credible sources
        cross_references = self._cross_reference_credible_sources(cluster_datapoints)
        
        # Analyze evidence
        evidence_for, evidence_against = self._analyze_evidence(
            cluster_datapoints,
            fact_check_sources,
            cross_references
        )
        
        # Determine verification status
        verification_status, confidence = self._determine_verification_status(
            fact_check_sources,
            cross_references,
            evidence_for,
            evidence_against,
            classification_result
        )
        
        # Build summary
        verification_summary = self._build_verification_summary(
            verification_status,
            fact_check_sources,
            cross_references,
            evidence_for,
            evidence_against
        )
        
        # Collect source URLs
        sources = self._collect_source_urls(fact_check_sources, cross_references)
        
        is_verified = verification_status in ["verified", "partially_true"]
        
        return VerificationResult(
            is_verified=is_verified,
            verification_status=verification_status,
            confidence=confidence,
            fact_check_sources=fact_check_sources,
            cross_references=cross_references,
            evidence_for=evidence_for,
            evidence_against=evidence_against,
            verification_summary=verification_summary,
            sources=sources
        )
    
    def verify_claim(
        self,
        claim_text: str,
        context: Optional[str] = None
    ) -> VerificationResult:
        """
        Verify a specific claim.
        
        Args:
            claim_text: The claim to verify
            context: Optional context about the claim
            
        Returns:
            VerificationResult
        """
        logger.info(f"Verifying claim: {claim_text[:100]}...")
        
        # Search for fact-checking articles (simulated - in production, use web search API)
        fact_check_sources = self._search_fact_check_articles(claim_text)
        
        # For now, analyze the claim text for indicators
        evidence_for = []
        evidence_against = []
        
        claim_lower = claim_text.lower()
        
        # Check for false indicators
        if any(keyword in claim_lower for keyword in self.FALSE_INDICATORS):
            evidence_against.append("Claim contains keywords indicating false information")
        
        # Check for verified indicators
        if any(keyword in claim_lower for keyword in self.VERIFIED_INDICATORS):
            evidence_for.append("Claim contains keywords indicating verified information")
        
        # Determine status
        if evidence_against and not evidence_for:
            verification_status = "false"
            confidence = 0.7
        elif evidence_for and not evidence_against:
            verification_status = "verified"
            confidence = 0.7
        else:
            verification_status = "unverified"
            confidence = 0.3
        
        return VerificationResult(
            is_verified=verification_status in ["verified", "partially_true"],
            verification_status=verification_status,
            confidence=confidence,
            fact_check_sources=fact_check_sources,
            cross_references=[],
            evidence_for=evidence_for,
            evidence_against=evidence_against,
            verification_summary=f"Claim analysis: {verification_status}",
            sources=[fc.get("url", "") for fc in fact_check_sources if fc.get("url")]
        )
    
    def _extract_key_claims(self, datapoints: List[Dict[str, Any]]) -> List[str]:
        """Extract key claims from datapoints."""
        claims = []
        
        for dp in datapoints:
            title = dp.get("title", "")
            content = dp.get("content", "")
            
            # Extract first sentence or key phrase
            if title:
                claims.append(title)
            elif content:
                first_sentence = content.split('.')[0]
                if len(first_sentence) > 20:  # Meaningful sentence
                    claims.append(first_sentence)
        
        return claims[:5]  # Limit to top 5 claims
    
    def _find_fact_check_sources(
        self,
        datapoints: List[Dict[str, Any]],
        key_claims: List[str]
    ) -> List[Dict[str, Any]]:
        """Find fact-checking sources in the cluster."""
        fact_check_sources = []
        
        for dp in datapoints:
            source_name = dp.get("source_name", "")
            title = dp.get("title", "").lower()
            content = dp.get("content", "").lower()
            categories = [c.lower() for c in dp.get("categories", [])]
            
            # Check if source is a fact-checker
            is_fact_checker = any(
                fc.lower() in source_name.lower() 
                for fc in FACT_CHECK_SOURCES
            )
            
            # Check for fact-check keywords
            has_fact_check_keywords = any(
                keyword in title or keyword in content
                for keyword in self.FACT_CHECK_KEYWORDS
            )
            
            # Check categories
            has_fact_check_category = "fact_check" in categories or "fact-check" in categories
            
            if is_fact_checker or has_fact_check_keywords or has_fact_check_category:
                # Determine verdict
                verdict = self._extract_verdict(title, content)
                
                fact_check_sources.append({
                    "source": source_name,
                    "title": dp.get("title", ""),
                    "url": dp.get("url", ""),
                    "verdict": verdict,
                    "published_at": dp.get("published_at"),
                    "relevance": "high" if is_fact_checker else "medium"
                })
        
        return fact_check_sources
    
    def _extract_verdict(self, title: str, content: str) -> str:
        """Extract verdict from fact-check article."""
        text = (title + " " + content).lower()
        
        # Check for false indicators
        if any(keyword in text for keyword in self.FALSE_INDICATORS):
            return "false"
        
        # Check for verified indicators
        if any(keyword in text for keyword in self.VERIFIED_INDICATORS):
            return "verified"
        
        # Check for disputed
        if "disputed" in text or "unclear" in text or "uncertain" in text:
            return "disputed"
        
        return "unverified"
    
    def _cross_reference_credible_sources(
        self,
        datapoints: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Cross-reference with credible sources in the cluster."""
        cross_refs = []
        credible_dps = []
        
        for dp in datapoints:
            source_name = dp.get("source_name", "")
            credibility = CREDIBLE_SOURCES.get(source_name, 0.5)
            
            if credibility >= 0.7:  # High credibility
                credible_dps.append({
                    "source": source_name,
                    "title": dp.get("title", ""),
                    "url": dp.get("url", ""),
                    "content": dp.get("content", "")[:200],  # First 200 chars
                    "credibility": credibility,
                    "published_at": dp.get("published_at")
                })
        
        # Group by source
        source_groups = {}
        for dp in credible_dps:
            source = dp["source"]
            if source not in source_groups:
                source_groups[source] = []
            source_groups[source].append(dp)
        
        # Create cross-references
        for source, dps in source_groups.items():
            cross_refs.append({
                "source": source,
                "count": len(dps),
                "articles": dps[:3],  # Top 3 articles per source
                "credibility": dps[0]["credibility"] if dps else 0.7
            })
        
        return cross_refs
    
    def _analyze_evidence(
        self,
        datapoints: List[Dict[str, Any]],
        fact_check_sources: List[Dict[str, Any]],
        cross_references: List[Dict[str, Any]]
    ) -> Tuple[List[str], List[str]]:
        """Analyze evidence for and against the claims."""
        evidence_for = []
        evidence_against = []
        
        # Analyze fact-check sources
        false_count = sum(1 for fc in fact_check_sources if fc.get("verdict") == "false")
        verified_count = sum(1 for fc in fact_check_sources if fc.get("verdict") == "verified")
        
        if false_count > 0:
            evidence_against.append(
                f"{false_count} fact-checking source(s) indicate the claim is false"
            )
        
        if verified_count > 0:
            evidence_for.append(
                f"{verified_count} fact-checking source(s) verify the claim"
            )
        
        # Analyze credible sources
        if cross_references:
            credible_count = len(cross_references)
            evidence_for.append(
                f"{credible_count} credible source(s) reporting on this topic"
            )
        
        # Check for contradictions in titles
        titles = [dp.get("title", "").lower() for dp in datapoints]
        has_false_keywords = any(
            any(kw in title for kw in self.FALSE_INDICATORS)
            for title in titles
        )
        has_verified_keywords = any(
            any(kw in title for kw in self.VERIFIED_INDICATORS)
            for title in titles
        )
        
        if has_false_keywords and not has_verified_keywords:
            evidence_against.append("Multiple articles contain false/misinformation indicators")
        elif has_verified_keywords and not has_false_keywords:
            evidence_for.append("Multiple articles contain verification indicators")
        
        return evidence_for, evidence_against
    
    def _determine_verification_status(
        self,
        fact_check_sources: List[Dict[str, Any]],
        cross_references: List[Dict[str, Any]],
        evidence_for: List[str],
        evidence_against: List[str],
        classification_result: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, float]:
        """Determine verification status and confidence."""
        # Count verdicts
        verdicts = [fc.get("verdict") for fc in fact_check_sources]
        false_count = verdicts.count("false")
        verified_count = verdicts.count("verified")
        disputed_count = verdicts.count("disputed")
        
        # Base confidence
        confidence = 0.5
        
        # Strong evidence: fact-checkers present
        if fact_check_sources:
            confidence += 0.2
            if false_count > verified_count:
                return ("false", min(0.9, confidence + 0.2 * false_count))
            elif verified_count > false_count:
                return ("verified", min(0.9, confidence + 0.2 * verified_count))
            elif disputed_count > 0:
                return ("disputed", 0.6)
        
        # Moderate evidence: credible sources
        if cross_references:
            confidence += 0.15
            if len(evidence_for) > len(evidence_against):
                return ("partially_true", min(0.8, confidence))
            elif len(evidence_against) > len(evidence_for):
                return ("false", min(0.7, confidence))
        
        # Weak evidence: classification result
        if classification_result:
            is_misinfo = classification_result.get("is_misinformation", False)
            class_confidence = classification_result.get("confidence", 0.5)
            
            if is_misinfo and class_confidence > 0.7:
                return ("false", min(0.7, confidence + 0.1))
            elif not is_misinfo and class_confidence > 0.7:
                return ("verified", min(0.7, confidence + 0.1))
        
        # Default: unverified
        return ("unverified", max(0.3, confidence - 0.1))
    
    def _build_verification_summary(
        self,
        verification_status: str,
        fact_check_sources: List[Dict[str, Any]],
        cross_references: List[Dict[str, Any]],
        evidence_for: List[str],
        evidence_against: List[str]
    ) -> str:
        """Build a human-readable verification summary."""
        summary_parts = []
        
        summary_parts.append(f"Verification Status: {verification_status.upper()}")
        
        if fact_check_sources:
            summary_parts.append(
                f"Found {len(fact_check_sources)} fact-checking source(s)"
            )
            verdicts = [fc.get("verdict") for fc in fact_check_sources]
            if verdicts:
                verdict_summary = ", ".join(set(verdicts))
                summary_parts.append(f"Verdicts: {verdict_summary}")
        
        if cross_references:
            summary_parts.append(
                f"Cross-referenced with {len(cross_references)} credible source(s)"
            )
        
        if evidence_for:
            summary_parts.append(f"Supporting evidence: {len(evidence_for)} point(s)")
        
        if evidence_against:
            summary_parts.append(f"Contradicting evidence: {len(evidence_against)} point(s)")
        
        return ". ".join(summary_parts) + "."
    
    def _collect_source_urls(
        self,
        fact_check_sources: List[Dict[str, Any]],
        cross_references: List[Dict[str, Any]]
    ) -> List[str]:
        """Collect all source URLs."""
        urls = []
        
        for fc in fact_check_sources:
            url = fc.get("url")
            if url:
                urls.append(url)
        
        for cr in cross_references:
            for article in cr.get("articles", []):
                url = article.get("url")
                if url:
                    urls.append(url)
        
        return list(set(urls))  # Remove duplicates
    
    def _search_fact_check_articles(self, claim_text: str) -> List[Dict[str, Any]]:
        """
        Search for fact-checking articles (placeholder for web search integration).
        
        In production, this would:
        1. Use Tavily search API to find fact-checking articles
        2. Use Google Fact Check API if available
        3. Search fact-checking databases
        """
        # Placeholder - in production, integrate with web search
        # For now, return empty list
        logger.debug(f"Would search for fact-check articles for: {claim_text[:100]}")
        return []
    
    def build_evidence_chain(
        self,
        cluster_id: str,
        verification_result: VerificationResult
    ) -> List[Dict[str, Any]]:
        """
        Build a comprehensive evidence chain for verification.
        
        Args:
            cluster_id: Cluster ID
            verification_result: Verification result
            
        Returns:
            List of evidence chain steps
        """
        chain = []
        
        # Step 1: Fact-check sources
        if verification_result.fact_check_sources:
            chain.append({
                "step": 1,
                "type": "fact_check",
                "description": f"Found {len(verification_result.fact_check_sources)} fact-checking source(s)",
                "sources": verification_result.fact_check_sources,
                "weight": 0.4
            })
        
        # Step 2: Cross-references
        if verification_result.cross_references:
            chain.append({
                "step": 2,
                "type": "cross_reference",
                "description": f"Cross-referenced with {len(verification_result.cross_references)} credible source(s)",
                "sources": verification_result.cross_references,
                "weight": 0.3
            })
        
        # Step 3: Evidence analysis
        if verification_result.evidence_for or verification_result.evidence_against:
            chain.append({
                "step": 3,
                "type": "evidence_analysis",
                "description": "Analyzed supporting and contradicting evidence",
                "evidence_for": verification_result.evidence_for,
                "evidence_against": verification_result.evidence_against,
                "weight": 0.3
            })
        
        return chain

