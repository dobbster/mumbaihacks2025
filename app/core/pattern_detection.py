"""Pattern detection service for analyzing clusters and detecting misinformation patterns."""

import logging
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter, defaultdict
from dateutil import parser

from app.core.storage import StorageService
from app.core.clustering import ClusteringService

logger = logging.getLogger(__name__)


# Source credibility database (can be expanded)
CREDIBLE_SOURCES = {
    # High credibility (0.9-1.0)
    "BBC News": 0.95,
    "Reuters": 0.95,
    "Reuters Health": 0.95,
    "AP News": 0.95,
    "Associated Press": 0.95,
    "CNN": 0.90,
    "The Guardian": 0.90,
    "The New York Times": 0.90,
    "The Washington Post": 0.90,
    "Wall Street Journal": 0.90,
    "NPR": 0.90,
    "PBS": 0.90,
    "BBC": 0.95,
    
    # Medium credibility (0.6-0.8)
    "Firstpost": 0.70,
    "India Today": 0.75,
    "The Hindu": 0.80,
    "The Times of India": 0.75,
    "Hindustan Times": 0.75,
    
    # Lower credibility or unknown (0.3-0.5)
    "Tavily Search": 0.50,  # Aggregator, credibility depends on sources
    "Social Media": 0.30,
    "Blog": 0.40,
    "Unknown": 0.30,
}

# Fact-checking organizations (high credibility)
FACT_CHECK_SOURCES = {
    "Fact Check Organization",
    "Snopes",
    "PolitiFact",
    "FactCheck.org",
    "AFP Fact Check",
    "Reuters Fact Check",
}


class PatternDetectionService:
    """
    Service for detecting patterns that indicate potential misinformation.
    
    Analyzes clusters to identify:
    - Rapid growth (sudden spike in articles = potential misinformation spread)
    - Source credibility issues (too many low-credibility sources)
    - Contradictions (conflicting claims within cluster)
    - Narrative evolution (how story changes over time)
    - Temporal patterns (when misinformation emerged)
    """
    
    def __init__(
        self,
        storage_service: StorageService,
        clustering_service: Optional[ClusteringService] = None,
        rapid_growth_threshold: float = 2.0,  # 2x growth in time window
        rapid_growth_window_hours: int = 6,  # 6-hour window
        min_credible_source_ratio: float = 0.3,  # At least 30% credible sources
    ):
        """
        Initialize pattern detection service.
        
        Args:
            storage_service: Storage service for MongoDB access
            clustering_service: Optional clustering service for similarity calculations
            rapid_growth_threshold: Growth multiplier to consider "rapid" (e.g., 2.0 = 2x growth)
            rapid_growth_window_hours: Time window to check for rapid growth
            min_credible_source_ratio: Minimum ratio of credible sources (0.0-1.0)
        """
        self.storage_service = storage_service
        self.clustering_service = clustering_service
        self.rapid_growth_threshold = rapid_growth_threshold
        self.rapid_growth_window_hours = rapid_growth_window_hours
        self.min_credible_source_ratio = min_credible_source_ratio
    
    def detect_rapid_growth(
        self,
        cluster_id: str,
        time_window_hours: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Detect if a cluster is growing rapidly (potential misinformation spread).
        
        Rapid growth is a key indicator of misinformation because:
        - Misinformation spreads faster than verified news
        - Viral false claims get amplified quickly
        - Legitimate news has more controlled distribution
        
        Args:
            cluster_id: Cluster to analyze
            time_window_hours: Time window for growth analysis (default: rapid_growth_window_hours)
            
        Returns:
            Dictionary with growth analysis:
            {
                "is_rapid_growth": bool,
                "growth_rate": float,
                "current_size": int,
                "previous_size": int,
                "time_window_hours": int,
                "datapoints_per_hour": float,
                "risk_score": float (0-1)
            }
        """
        time_window = time_window_hours or self.rapid_growth_window_hours
        
        # Get all datapoints in cluster
        cluster_datapoints = self.storage_service.get_datapoints_by_cluster(cluster_id)
        
        if len(cluster_datapoints) < 2:
            return {
                "is_rapid_growth": False,
                "growth_rate": 0.0,
                "current_size": len(cluster_datapoints),
                "previous_size": 0,
                "time_window_hours": time_window,
                "datapoints_per_hour": 0.0,
                "risk_score": 0.0,
                "reason": "Insufficient datapoints for growth analysis"
            }
        
        # Parse timestamps and sort
        datapoints_with_time = []
        for dp in cluster_datapoints:
            try:
                if isinstance(dp.get("published_at"), str):
                    published_at = parser.parse(dp["published_at"])
                else:
                    published_at = dp.get("published_at")
                
                if published_at:
                    datapoints_with_time.append((published_at, dp))
            except Exception as e:
                logger.debug(f"Failed to parse timestamp for datapoint {dp.get('id')}: {e}")
                continue
        
        if len(datapoints_with_time) < 2:
            return {
                "is_rapid_growth": False,
                "growth_rate": 0.0,
                "current_size": len(cluster_datapoints),
                "previous_size": 0,
                "time_window_hours": time_window,
                "datapoints_per_hour": 0.0,
                "risk_score": 0.0,
                "reason": "Insufficient valid timestamps"
            }
        
        # Sort by time
        datapoints_with_time.sort(key=lambda x: x[0])
        
        # Get most recent timestamp
        most_recent = datapoints_with_time[-1][0]
        window_start = most_recent - timedelta(hours=time_window)
        
        # Count datapoints in recent window vs previous window
        recent_window = [dp for ts, dp in datapoints_with_time if ts >= window_start]
        previous_window_start = window_start - timedelta(hours=time_window)
        previous_window = [dp for ts, dp in datapoints_with_time 
                          if previous_window_start <= ts < window_start]
        
        current_size = len(recent_window)
        previous_size = len(previous_window)
        
        # Calculate growth rate
        if previous_size == 0:
            growth_rate = float('inf') if current_size > 0 else 0.0
        else:
            growth_rate = current_size / previous_size
        
        # Calculate datapoints per hour
        time_span_hours = max(1, (most_recent - datapoints_with_time[0][0]).total_seconds() / 3600)
        datapoints_per_hour = len(datapoints_with_time) / time_span_hours
        
        # Determine if rapid growth
        # Only flag as suspicious if growth is EXTREMELY unusual 
        is_rapid_growth = (
            growth_rate >= 10.0 and  # Very high threshold (10x growth)
            current_size >= 10  # At least 10 datapoints in recent window
        )
        
        # Calculate risk score (0-1) - Minimal impact
        # Rapid growth alone is NOT a strong indicator of misinformation
        # Legitimate breaking news (earthquakes, elections, major events) can grow very rapidly
        growth_component = 0.0
        # Only contribute to risk if growth is EXTREMELY unusual (>10x)
        if growth_rate > 15.0:  # Only penalize if growth is >15x (extremely unusual)
            growth_component = min(1.0, (growth_rate - 15.0) / 20.0) * 0.1  # Minimal weight (10% max
        
        velocity_component = 0.0
        # Only penalize if velocity is EXTREMELY high (>20 per hour)
        if datapoints_per_hour > 20.0:
            velocity_component = min(1.0, (datapoints_per_hour - 20.0) / 30.0) * 0.05  # Very minimal weight
        
        # Rapid growth contributes minimally to overall risk
        # Most legitimate breaking news will have rapid growth
        risk_score = min(0.2, growth_component + velocity_component)  # Cap at 0.2 max
        
        return {
            "is_rapid_growth": is_rapid_growth,
            "growth_rate": round(growth_rate, 2),
            "current_size": current_size,
            "previous_size": previous_size,
            "time_window_hours": time_window,
            "datapoints_per_hour": round(datapoints_per_hour, 2),
            "total_datapoints": len(cluster_datapoints),
            "risk_score": round(risk_score, 3),
            "first_datapoint_time": datapoints_with_time[0][0].isoformat() if datapoints_with_time else None,
            "last_datapoint_time": most_recent.isoformat() if datapoints_with_time else None,
        }
    
    def analyze_source_credibility(
        self,
        cluster_id: str
    ) -> Dict[str, Any]:
        """
        Analyze source credibility within a cluster.
        
        Misinformation often spreads through:
        - Low-credibility sources
        - Social media
        - Unverified blogs
        - Questionable news sites
        
        Args:
            cluster_id: Cluster to analyze
            
        Returns:
            Dictionary with credibility analysis:
            {
                "credible_sources": List[str],
                "questionable_sources": List[str],
                "credible_ratio": float,
                "source_diversity": int,
                "risk_score": float (0-1),
                "source_breakdown": Dict[str, int]
            }
        """
        cluster_datapoints = self.storage_service.get_datapoints_by_cluster(cluster_id)
        
        if not cluster_datapoints:
            return {
                "credible_sources": [],
                "questionable_sources": [],
                "credible_ratio": 0.0,
                "source_diversity": 0,
                "risk_score": 1.0,
                "source_breakdown": {},
                "reason": "No datapoints in cluster"
            }
        
        # Count sources
        source_counts = Counter()
        credible_count = 0
        questionable_count = 0
        credible_sources = set()
        questionable_sources = set()
        
        for dp in cluster_datapoints:
            source_name = dp.get("source_name", "Unknown")
            source_counts[source_name] += 1
            
            # Get credibility score
            credibility = self._get_source_credibility(source_name)
            
            if credibility >= 0.7:  # High credibility
                credible_count += 1
                credible_sources.add(source_name)
            elif credibility < 0.5:  # Low credibility
                questionable_count += 1
                questionable_sources.add(source_name)
        
        total_sources = len(cluster_datapoints)
        credible_ratio = credible_count / total_sources if total_sources > 0 else 0.0
        source_diversity = len(source_counts)
        
        # Check if fact-checkers are present (good sign) - DO THIS FIRST
        fact_checkers_present = any(
            source in FACT_CHECK_SOURCES 
            for source in source_counts.keys()
        )
        
        # Calculate risk score - More balanced, give credit to credible sources
        # Higher risk if: very low credible ratio, many questionable sources
        # Lower risk if: fact-checkers present, high credible ratio
        base_risk = (1 - credible_ratio) * 0.4  # Reduced weight (50% -> 40%)
        questionable_risk = (min(questionable_count / max(total_sources, 1), 1.0)) * 0.3
        
        # Give credit for fact-checkers and high credibility
        credibility_bonus = 0.0
        if fact_checkers_present:
            credibility_bonus = -0.2  # Reduce risk if fact-checkers present
        if credible_ratio >= 0.5:  # If majority are credible, reduce risk
            credibility_bonus = max(credibility_bonus, -0.15)
        
        # Diversity is less important - remove it from risk calculation
        risk_score = max(0.0, min(1.0, base_risk + questionable_risk + credibility_bonus))
        
        return {
            "credible_sources": sorted(list(credible_sources)),
            "questionable_sources": sorted(list(questionable_sources)),
            "credible_ratio": round(credible_ratio, 3),
            "credible_count": credible_count,
            "questionable_count": questionable_count,
            "source_diversity": source_diversity,
            "total_sources": total_sources,
            "risk_score": round(risk_score, 3),
            "source_breakdown": dict(source_counts),
            "fact_checkers_present": fact_checkers_present,
            "meets_credibility_threshold": credible_ratio >= self.min_credible_source_ratio,
        }
    
    def detect_contradictions(
        self,
        cluster_id: str,
        similarity_threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Detect contradictory claims within a cluster.
        
        Contradictions are a strong indicator of misinformation:
        - Multiple conflicting claims about the same topic
        - Claims that contradict verified facts
        - Evolving narratives that change key details
        
        Args:
            cluster_id: Cluster to analyze
            similarity_threshold: Minimum similarity to consider for contradiction analysis
            
        Returns:
            Dictionary with contradiction analysis:
            {
                "has_contradictions": bool,
                "contradiction_count": int,
                "contradiction_pairs": List[Dict],
                "risk_score": float (0-1),
                "sample_contradictions": List[str]
            }
        """
        cluster_datapoints = self.storage_service.get_datapoints_by_cluster(cluster_id)
        
        if len(cluster_datapoints) < 2:
            return {
                "has_contradictions": False,
                "contradiction_count": 0,
                "contradiction_pairs": [],
                "risk_score": 0.0,
                "sample_contradictions": [],
                "reason": "Insufficient datapoints for contradiction analysis"
            }
        
        # Extract key claims from titles and content
        # Simple approach: compare titles and first sentences
        claims = []
        for dp in cluster_datapoints:
            title = dp.get("title", "")
            content = dp.get("content", "")
            # Extract first sentence or first 200 chars as claim
            first_sentence = content.split('.')[0] if content else ""
            claim_text = f"{title}. {first_sentence[:200]}"
            claims.append({
                "id": dp.get("id"),
                "text": claim_text,
                "source": dp.get("source_name", "Unknown"),
                "title": title,
                "embedding": dp.get("embedding", [])
            })
        
        # Find contradictions using embeddings if available
        contradiction_pairs = []
        
        if self.clustering_service and claims[0].get("embedding"):
            # Use embedding similarity to find similar but potentially contradictory claims
            for i, claim1 in enumerate(claims):
                if not claim1.get("embedding"):
                    continue
                    
                for j, claim2 in enumerate(claims[i+1:], start=i+1):
                    if not claim2.get("embedding"):
                        continue
                    
                    # Calculate similarity
                    similarity = self.clustering_service.cosine_similarity(
                        claim1["embedding"],
                        claim2["embedding"]
                    )
                    
                    # If similar in topic but different in claim, might be contradiction
                    if similarity >= similarity_threshold:
                        # Check for contradiction keywords
                        if self._has_contradiction_keywords(claim1["text"], claim2["text"]):
                            contradiction_pairs.append({
                                "claim1": {
                                    "id": claim1["id"],
                                    "title": claim1["title"],
                                    "source": claim1["source"],
                                    "text": claim1["text"][:150]
                                },
                                "claim2": {
                                    "id": claim2["id"],
                                    "title": claim2["title"],
                                    "source": claim2["source"],
                                    "text": claim2["text"][:150]
                                },
                                "similarity": round(similarity, 3),
                                "contradiction_type": self._classify_contradiction(claim1["text"], claim2["text"])
                            })
        
        # Also check for explicit contradiction keywords in titles
        contradiction_keywords = [
            "false", "debunked", "unfounded", "prove unfounded", "rumors", "misinformation",
            "disproven", "incorrect", "wrong", "not true", "denied", "rejected"
        ]
        
        for claim in claims:
            title_lower = claim["title"].lower()
            if any(keyword in title_lower for keyword in contradiction_keywords):
                # Find related claims that might contradict
                for other_claim in claims:
                    if other_claim["id"] != claim["id"]:
                        # Check if they're about similar topic
                        if self._topics_similar(claim["title"], other_claim["title"]):
                            contradiction_pairs.append({
                                "claim1": {
                                    "id": claim["id"],
                                    "title": claim["title"],
                                    "source": claim["source"],
                                    "text": claim["text"][:150]
                                },
                                "claim2": {
                                    "id": other_claim["id"],
                                    "title": other_claim["title"],
                                    "source": other_claim["source"],
                                    "text": other_claim["text"][:150]
                                },
                                "similarity": 0.8,  # Estimated
                                "contradiction_type": "fact_check_vs_claim"
                            })
        
        # Remove duplicates
        unique_pairs = []
        seen_pairs = set()
        for pair in contradiction_pairs:
            pair_key = tuple(sorted([pair["claim1"]["id"], pair["claim2"]["id"]]))
            if pair_key not in seen_pairs:
                seen_pairs.add(pair_key)
                unique_pairs.append(pair)
        
        has_contradictions = len(unique_pairs) > 0
        
        # Calculate risk score - More conservative
        # Legitimate news can have different perspectives/updates
        # Only penalize if there are MANY contradictions relative to cluster size
        if len(unique_pairs) == 0:
            risk_score = 0.0
        else:
            # Only count as high risk if contradictions are >20% of datapoints
            contradiction_ratio = len(unique_pairs) / max(len(cluster_datapoints), 1)
            if contradiction_ratio > 0.2:  # More than 20% are contradictions
                risk_score = min(1.0, (contradiction_ratio - 0.2) / 0.8)  # Scale from 0.2 to 1.0
            else:
                risk_score = contradiction_ratio * 0.5  # Low risk for few contradictions
        
        # Sample contradictions for display
        sample_contradictions = [
            f"{pair['claim1']['title'][:50]}... vs {pair['claim2']['title'][:50]}..."
            for pair in unique_pairs[:3]
        ]
        
        return {
            "has_contradictions": has_contradictions,
            "contradiction_count": len(unique_pairs),
            "contradiction_pairs": unique_pairs[:10],  # Limit to top 10
            "risk_score": round(risk_score, 3),
            "sample_contradictions": sample_contradictions,
            "total_datapoints": len(cluster_datapoints)
        }
    
    def track_narrative_evolution(
        self,
        cluster_id: str
    ) -> Dict[str, Any]:
        """
        Track how the narrative/story evolves over time within a cluster.
        
        Misinformation often evolves:
        - Initial claim gets modified
        - Details change over time
        - Story becomes more extreme
        - Key facts are altered
        
        Args:
            cluster_id: Cluster to analyze
            
        Returns:
            Dictionary with narrative evolution analysis:
            {
                "has_evolution": bool,
                "evolution_stages": List[Dict],
                "key_changes": List[str],
                "risk_score": float (0-1)
            }
        """
        cluster_datapoints = self.storage_service.get_datapoints_by_cluster(cluster_id)
        
        if len(cluster_datapoints) < 3:
            return {
                "has_evolution": False,
                "evolution_stages": [],
                "key_changes": [],
                "risk_score": 0.0,
                "reason": "Insufficient datapoints for evolution tracking"
            }
        
        # Sort by publication time
        datapoints_with_time = []
        for dp in cluster_datapoints:
            try:
                if isinstance(dp.get("published_at"), str):
                    published_at = parser.parse(dp["published_at"])
                else:
                    published_at = dp.get("published_at")
                
                if published_at:
                    datapoints_with_time.append((published_at, dp))
            except Exception as e:
                logger.debug(f"Failed to parse timestamp: {e}")
                continue
        
        if len(datapoints_with_time) < 3:
            return {
                "has_evolution": False,
                "evolution_stages": [],
                "key_changes": [],
                "risk_score": 0.0,
                "reason": "Insufficient valid timestamps"
            }
        
        datapoints_with_time.sort(key=lambda x: x[0])
        
        # Analyze how titles/content change over time
        evolution_stages = []
        key_changes = []
        
        # Group into time windows
        time_windows = self._create_time_windows(datapoints_with_time, window_hours=6)
        
        for i, window in enumerate(time_windows):
            if not window:
                continue
            
            # Extract common keywords/phrases from this window
            titles = [dp.get("title", "") for _, dp in window]
            common_keywords = self._extract_common_keywords(titles)
            
            evolution_stages.append({
                "window_index": i,
                "time_range": {
                    "start": window[0][0].isoformat(),
                    "end": window[-1][0].isoformat()
                },
                "datapoint_count": len(window),
                "key_phrases": common_keywords[:5],
                "sample_titles": [dp.get("title", "")[:80] for _, dp in window[:3]]
            })
            
            # Compare with previous window
            if i > 0 and time_windows[i-1]:
                prev_keywords = self._extract_common_keywords(
                    [dp.get("title", "") for _, dp in time_windows[i-1]]
                )
                
                # Find new keywords (narrative shift)
                new_keywords = set(common_keywords) - set(prev_keywords)
                if new_keywords:
                    key_changes.append({
                        "window": i,
                        "new_keywords": list(new_keywords)[:5],
                        "description": f"Narrative shift detected: new focus on {', '.join(list(new_keywords)[:3])}"
                    })
        
        has_evolution = len(key_changes) > 0
        
        # Calculate risk score - More conservative
        # Story updates are normal in legitimate news
        # Only penalize if there are MANY significant changes
        if not has_evolution:
            risk_score = 0.0
        else:
            # Only high risk if changes are frequent (>50% of windows have changes)
            change_frequency = len(key_changes) / max(len(time_windows), 1)
            if change_frequency > 0.5:  # More than 50% of windows have changes
                risk_score = min(1.0, (change_frequency - 0.5) / 0.5) * 0.6  # Scale and reduce max
            else:
                risk_score = change_frequency * 0.3  # Low risk for occasional updates
        
        return {
            "has_evolution": has_evolution,
            "evolution_stages": evolution_stages,
            "key_changes": key_changes,
            "risk_score": round(risk_score, 3),
            "total_stages": len(evolution_stages),
            "change_count": len(key_changes)
        }
    
    def analyze_cluster(
        self,
        cluster_id: str
    ) -> Dict[str, Any]:
        """
        Comprehensive analysis of a cluster combining all pattern detection methods.
        
        Args:
            cluster_id: Cluster to analyze
            
        Returns:
            Comprehensive analysis dictionary with all pattern detection results
        """
        logger.info(f"Analyzing cluster {cluster_id} for patterns")
        
        # Get cluster datapoints
        cluster_datapoints = self.storage_service.get_datapoints_by_cluster(cluster_id)
        
        if not cluster_datapoints:
            return {
                "cluster_id": cluster_id,
                "error": "Cluster not found or empty",
                "datapoint_count": 0
            }
        
        # Run all analyses
        growth_analysis = self.detect_rapid_growth(cluster_id)
        credibility_analysis = self.analyze_source_credibility(cluster_id)
        contradiction_analysis = self.detect_contradictions(cluster_id)
        evolution_analysis = self.track_narrative_evolution(cluster_id)
        
        # Calculate overall risk score
        # Give rapid growth minimal weight (10%) since it's common in legitimate news
        # Focus on credibility, contradictions, and evolution as stronger indicators
        growth_risk = growth_analysis.get("risk_score", 0.0)
        credibility_risk = credibility_analysis.get("risk_score", 0.0)
        contradiction_risk = contradiction_analysis.get("risk_score", 0.0)
        evolution_risk = evolution_analysis.get("risk_score", 0.0)
        
        # Weighted average: rapid growth gets only 10% weight
        overall_risk_score = (
            growth_risk * 0.1 +  # Rapid growth: 10% (minimal impact)
            credibility_risk * 0.4 +  # Source credibility: 40% (strong indicator)
            contradiction_risk * 0.3 +  # Contradictions: 30% (strong indicator)
            evolution_risk * 0.2  # Narrative evolution: 20% (moderate indicator)
        )
        
        # Determine risk level - Adjusted thresholds to be more conservative
        if overall_risk_score >= 0.6:  # Raised from 0.7
            risk_level = "high"
        elif overall_risk_score >= 0.35:  # Raised from 0.4
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Flags for quick assessment - More conservative thresholds
        flags = {
            "rapid_growth": growth_analysis.get("is_rapid_growth", False),
            "low_credibility": credibility_analysis.get("credible_ratio", 1.0) < (self.min_credible_source_ratio * 0.7),  # Lower threshold (was 0.3, now 0.21)
            "has_contradictions": contradiction_analysis.get("has_contradictions", False) and contradiction_analysis.get("contradiction_count", 0) > 2,  # Require multiple contradictions
            "narrative_evolution": evolution_analysis.get("has_evolution", False) and evolution_analysis.get("change_count", 0) > 2  # Require multiple changes
        }
        
        # Count flags
        flag_count = sum(flags.values())
        
        return {
            "cluster_id": cluster_id,
            "datapoint_count": len(cluster_datapoints),
            "overall_risk_score": round(overall_risk_score, 3),
            "risk_level": risk_level,
            "flags": flags,
            "flag_count": flag_count,
            "growth_analysis": growth_analysis,
            "credibility_analysis": credibility_analysis,
            "contradiction_analysis": contradiction_analysis,
            "evolution_analysis": evolution_analysis,
            "recommendation": self._generate_recommendation(flags, overall_risk_score)
        }
    
    def analyze_all_clusters(
        self,
        hours: int = 168,
        min_cluster_size: int = 2
    ) -> Dict[str, Any]:
        """
        Analyze all clusters found in recent datapoints.
        
        Args:
            hours: Look back this many hours for clusters
            min_cluster_size: Minimum cluster size to analyze
            
        Returns:
            Dictionary with analysis of all clusters
        """
        # Get all recent clustered datapoints
        recent = self.storage_service.get_recent_datapoints(hours=hours)
        clustered = [dp for dp in recent if dp.get("cluster_id")]
        
        # Group by cluster_id
        clusters_map = defaultdict(list)
        for dp in clustered:
            cluster_id = dp.get("cluster_id")
            if cluster_id:
                clusters_map[cluster_id].append(dp)
        
        # Filter by minimum size
        clusters_to_analyze = {
            cid: dps for cid, dps in clusters_map.items() 
            if len(dps) >= min_cluster_size
        }
        
        logger.info(f"Analyzing {len(clusters_to_analyze)} clusters")
        
        # Analyze each cluster
        analyses = {}
        for cluster_id in clusters_to_analyze.keys():
            try:
                analyses[cluster_id] = self.analyze_cluster(cluster_id)
            except Exception as e:
                logger.error(f"Failed to analyze cluster {cluster_id}: {e}", exc_info=True)
                analyses[cluster_id] = {
                    "cluster_id": cluster_id,
                    "error": str(e)
                }
        
        # Summary statistics
        risk_scores = [a.get("overall_risk_score", 0.0) for a in analyses.values() if "overall_risk_score" in a]
        high_risk_clusters = [cid for cid, a in analyses.items() if a.get("risk_level") == "high"]
        medium_risk_clusters = [cid for cid, a in analyses.items() if a.get("risk_level") == "medium"]
        
        return {
            "total_clusters_analyzed": len(analyses),
            "high_risk_clusters": len(high_risk_clusters),
            "medium_risk_clusters": len(medium_risk_clusters),
            "low_risk_clusters": len(analyses) - len(high_risk_clusters) - len(medium_risk_clusters),
            "average_risk_score": round(np.mean(risk_scores), 3) if risk_scores else 0.0,
            "high_risk_cluster_ids": high_risk_clusters,
            "analyses": analyses
        }
    
    # Helper methods
    
    def _get_source_credibility(self, source_name: str) -> float:
        """Get credibility score for a source (0.0-1.0)."""
        # Check exact match
        if source_name in CREDIBLE_SOURCES:
            return CREDIBLE_SOURCES[source_name]
        
        # Check partial matches
        source_lower = source_name.lower()
        for known_source, credibility in CREDIBLE_SOURCES.items():
            if known_source.lower() in source_lower or source_lower in known_source.lower():
                return credibility
        
        # Check if fact-checker
        if any(fc.lower() in source_lower for fc in FACT_CHECK_SOURCES):
            return 0.95
        
        # Default: medium-low credibility for unknown sources
        return 0.50
    
    def _has_contradiction_keywords(self, text1: str, text2: str) -> bool:
        """Check if two texts contain contradiction keywords."""
        contradiction_patterns = [
            ("false", "true"),
            ("debunked", "confirmed"),
            ("denied", "confirmed"),
            ("not", "is"),  # Simple negation
            ("no", "yes"),
            ("unfounded", "verified"),
            ("rumor", "fact"),
            ("misinformation", "verified"),
        ]
        
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        for pattern1, pattern2 in contradiction_patterns:
            if (pattern1 in text1_lower and pattern2 in text2_lower) or \
               (pattern2 in text1_lower and pattern1 in text2_lower):
                return True
        
        return False
    
    def _classify_contradiction(self, text1: str, text2: str) -> str:
        """Classify the type of contradiction."""
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        if "false" in text1_lower or "debunked" in text1_lower:
            return "fact_check_vs_claim"
        elif "rumor" in text1_lower or "misinformation" in text1_lower:
            return "rumor_vs_fact"
        elif "denied" in text1_lower or "rejected" in text1_lower:
            return "denial_vs_claim"
        else:
            return "conflicting_claims"
    
    def _topics_similar(self, title1: str, title2: str) -> bool:
        """Simple check if two titles are about similar topics."""
        # Extract key words (remove common stop words)
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        words1 = set(word.lower() for word in title1.split() if word.lower() not in stop_words)
        words2 = set(word.lower() for word in title2.split() if word.lower() not in stop_words)
        
        # Check overlap
        if not words1 or not words2:
            return False
        
        overlap = len(words1 & words2)
        total_unique = len(words1 | words2)
        
        # If >30% overlap, consider similar
        return (overlap / total_unique) > 0.3 if total_unique > 0 else False
    
    def _create_time_windows(
        self,
        datapoints_with_time: List[Tuple[datetime, Dict]],
        window_hours: int = 6
    ) -> List[List[Tuple[datetime, Dict]]]:
        """Group datapoints into time windows."""
        if not datapoints_with_time:
            return []
        
        windows = []
        current_window = []
        window_start = None
        
        for ts, dp in datapoints_with_time:
            if window_start is None:
                window_start = ts
                current_window = [(ts, dp)]
            elif (ts - window_start).total_seconds() / 3600 <= window_hours:
                current_window.append((ts, dp))
            else:
                # Start new window
                windows.append(current_window)
                window_start = ts
                current_window = [(ts, dp)]
        
        if current_window:
            windows.append(current_window)
        
        return windows
    
    def _extract_common_keywords(self, texts: List[str], top_n: int = 5) -> List[str]:
        """Extract most common keywords from texts."""
        from collections import Counter
        
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
            "of", "with", "by", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "must", "can", "this", "that", "these", "those"
        }
        
        all_words = []
        for text in texts:
            words = text.lower().split()
            # Remove punctuation and stop words
            words = [
                word.strip(".,!?;:()[]{}'\"") 
                for word in words 
                if word.strip(".,!?;:()[]{}'\"") not in stop_words and len(word) > 3
            ]
            all_words.extend(words)
        
        word_counts = Counter(all_words)
        return [word for word, count in word_counts.most_common(top_n)]
    
    def _generate_recommendation(
        self,
        flags: Dict[str, bool],
        risk_score: float
    ) -> str:
        """Generate recommendation based on analysis."""
        if risk_score >= 0.7:
            return "HIGH RISK: Immediate review recommended. Multiple red flags detected."
        elif risk_score >= 0.4:
            return "MEDIUM RISK: Review recommended. Some concerning patterns detected."
        elif flags.get("rapid_growth") or flags.get("has_contradictions"):
            return "MONITOR: Keep monitoring for emerging patterns."
        else:
            return "LOW RISK: Appears to be legitimate news coverage."

