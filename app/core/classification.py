"""Classification service for misinformation detection using LLM analysis."""

import logging
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# Together AI via LangChain
# langchain-together may not have ChatTogether, use langchain_community instead
try:
    from langchain_community.chat_models import ChatTogether
except ImportError:
    try:
        # Try langchain-together as fallback
        from langchain_together import ChatTogether
    except ImportError:
        ChatTogether = None

logger = logging.getLogger(__name__)


class ClassificationResult(BaseModel):
    """Result of misinformation classification."""
    is_misinformation: bool = Field(description="Whether the cluster contains misinformation")
    confidence: float = Field(description="Confidence score (0.0 to 1.0)")
    classification: str = Field(description="Classification: 'misinformation', 'legitimate', or 'uncertain'")
    topic_representation: str = Field(description="Concise human-readable description of what this cluster is about")
    evidence_chain: List[Dict[str, Any]] = Field(description="Chain of evidence supporting the classification")
    key_indicators: List[str] = Field(description="Key indicators that led to this classification")
    reasoning: str = Field(description="Detailed reasoning for the classification")
    supporting_evidence: List[str] = Field(description="Evidence supporting misinformation claim")
    contradictory_evidence: List[str] = Field(description="Evidence contradicting misinformation claim")
    sources: List[str] = Field(description="List of source URLs from all datapoints in the cluster", default_factory=list)


class ClassificationService:
    """
    Service for classifying clusters as misinformation using LLM analysis.
    
    Uses Together AI LLM to analyze pattern detection results and provide:
    - Binary classification (misinformation vs legitimate)
    - Confidence scoring (0.0-1.0)
    - Evidence chain (transparent reasoning)
    - Key indicators
    """
    
    # Recommended Together AI models for classification
    RECOMMENDED_MODELS = {
        "fast": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",  # Fast, good for classification
        "balanced": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",  # Better reasoning, balanced
        "best": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Best reasoning, slower
        "default": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"  # Default
    }
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.1,  # Low temperature for consistent classification
        together_api_key: Optional[str] = None
    ):
        """
        Initialize classification service.
        
        Args:
            model_name: Together AI model name (default: Meta-Llama-3.1-8B-Instruct-Turbo)
            temperature: LLM temperature (0.0-1.0, lower = more deterministic)
            together_api_key: Together AI API key (if not provided, uses TOGETHER_API_KEY env var)
        """
        import os
        
        if ChatTogether is None:
            raise ImportError(
                "ChatTogether not available. Install langchain-together or langchain-community. "
                "Run: uv add langchain-together"
            )
        
        self.model_name = model_name or os.getenv(
            "TOGETHER_LLM_MODEL",
            self.RECOMMENDED_MODELS["default"]
        )
        self.temperature = temperature
        
        api_key = together_api_key or os.getenv("TOGETHER_API_KEY")
        if not api_key:
            raise ValueError(
                "TOGETHER_API_KEY environment variable is required. "
                "Get your API key from https://api.together.xyz/"
            )
        
        # Initialize Together AI LLM
        self.llm = ChatTogether(
            model=self.model_name,
            together_api_key=api_key,
            temperature=temperature,
            max_tokens=2000,  # Enough for detailed analysis
        )
        
        logger.info(f"Initialized ClassificationService with model: {self.model_name}")
    
    def classify_cluster(
        self,
        cluster_id: str,
        pattern_analysis: Dict[str, Any],
        cluster_datapoints: Optional[List[Dict[str, Any]]] = None
    ) -> ClassificationResult:
        """
        Classify a cluster as misinformation or legitimate news.
        
        Args:
            cluster_id: Cluster ID to classify
            pattern_analysis: Results from PatternDetectionService.analyze_cluster()
            cluster_datapoints: Optional list of datapoints in cluster (for detailed analysis)
            
        Returns:
            ClassificationResult with classification, confidence, and evidence chain
        """
        logger.info(f"Classifying cluster {cluster_id} using LLM")
        
        # Build prompt with pattern analysis
        prompt = self._build_classification_prompt(cluster_id, pattern_analysis, cluster_datapoints)
        
        # Call LLM
        try:
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Parse JSON response
            result = self._parse_llm_response(content)
            
            # Extract source URLs from cluster datapoints
            sources = []
            if cluster_datapoints:
                for dp in cluster_datapoints:
                    url = dp.get("url") or dp.get("source_url")
                    if url and url not in sources:
                        sources.append(url)
            
            # Add sources to the result
            result.sources = sources
            
            logger.info(
                f"Classification complete for {cluster_id}: "
                f"{result.classification} (confidence: {result.confidence:.3f}, "
                f"{len(sources)} sources)"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error classifying cluster {cluster_id}: {e}", exc_info=True)
            # Return uncertain classification on error
            # Extract sources even on error
            sources = []
            if cluster_datapoints:
                for dp in cluster_datapoints:
                    url = dp.get("url") or dp.get("source_url")
                    if url and url not in sources:
                        sources.append(url)
            
            # Return uncertain classification with low confidence on error
            return ClassificationResult(
                is_misinformation=False,
                confidence=0.0,  # No confidence when error occurs
                classification="uncertain",
                topic_representation="Error: Could not determine topic",
                evidence_chain=[],
                key_indicators=[f"Error during classification: {str(e)}"],
                reasoning=f"Failed to classify due to error: {str(e)}",
                supporting_evidence=[],
                contradictory_evidence=[],
                sources=sources
            )
    
    def _build_classification_prompt(
        self,
        cluster_id: str,
        pattern_analysis: Dict[str, Any],
        cluster_datapoints: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Build the classification prompt for the LLM.
        
        This prompt is designed to:
        1. Analyze pattern detection results
        2. Classify as misinformation/legitimate/uncertain
        3. Provide confidence score
        4. Build evidence chain
        """
        # Extract key information from pattern analysis
        risk_score = pattern_analysis.get("overall_risk_score", 0.0)
        risk_level = pattern_analysis.get("risk_level", "unknown")
        flags = pattern_analysis.get("flags", {})
        growth = pattern_analysis.get("growth_analysis", {})
        credibility = pattern_analysis.get("credibility_analysis", {})
        contradictions = pattern_analysis.get("contradiction_analysis", {})
        evolution = pattern_analysis.get("evolution_analysis", {})
        
        # Build sample titles for context (limit to 5)
        sample_titles = []
        if cluster_datapoints:
            for dp in cluster_datapoints[:5]:
                title = dp.get("title", "No title")
                source = dp.get("source_name", "Unknown")
                sample_titles.append(f"- [{source}] {title}")
        else:
            sample_titles = ["- Sample datapoints not provided"]
        
        prompt = f"""You are an expert misinformation detection analyst. Your task is to analyze a cluster of news articles and determine if it contains misinformation.

## Cluster Information
- Cluster ID: {cluster_id}
- Number of Articles: {pattern_analysis.get('datapoint_count', 0)}
- Overall Risk Score: {risk_score:.3f} (Risk Level: {risk_level.upper()})

## Pattern Detection Results

### 1. Rapid Growth Analysis
- Is Rapid Growth: {growth.get('is_rapid_growth', False)}
- Growth Rate: {growth.get('growth_rate', 'N/A')}
- Datapoints per Hour: {growth.get('datapoints_per_hour', 0.0):.2f}
- Growth Risk Score: {growth.get('risk_score', 0.0):.3f}

### 2. Source Credibility Analysis
- Credible Sources Ratio: {credibility.get('credible_ratio', 0.0):.3f}
- Credible Sources: {', '.join(credibility.get('credible_sources', [])[:5]) or 'None'}
- Questionable Sources: {', '.join(credibility.get('questionable_sources', [])[:5]) or 'None'}
- Source Diversity: {credibility.get('source_diversity', 0)}
- Credibility Risk Score: {credibility.get('risk_score', 0.0):.3f}
- Fact Checkers Present: {credibility.get('fact_checkers_present', False)}

### 3. Contradiction Detection
- Has Contradictions: {contradictions.get('has_contradictions', False)}
- Contradiction Count: {contradictions.get('contradiction_count', 0)}
- Contradiction Risk Score: {contradictions.get('risk_score', 0.0):.3f}
- Sample Contradictions:
{chr(10).join(f'  - {c}' for c in contradictions.get('sample_contradictions', [])[:3]) or '  - None detected'}

### 4. Narrative Evolution
- Has Evolution: {evolution.get('has_evolution', False)}
- Evolution Stages: {evolution.get('total_stages', 0)}
- Key Changes: {evolution.get('change_count', 0)}
- Evolution Risk Score: {evolution.get('risk_score', 0.0):.3f}

## Red Flags Detected
- Rapid Growth: {flags.get('rapid_growth', False)}
- Low Credibility: {flags.get('low_credibility', False)}
- Has Contradictions: {flags.get('has_contradictions', False)}
- Narrative Evolution: {flags.get('narrative_evolution', False)}
- Total Flags: {pattern_analysis.get('flag_count', 0)}/4

## Sample Article Titles
{chr(10).join(sample_titles)}

---

## Your Task

Analyze the above pattern detection results and classify this cluster. **IMPORTANT: Be balanced and conservative. Do not assume misinformation without strong evidence.**

Consider:

1. **Rapid Growth**: 
   - Legitimate breaking news ALWAYS spreads rapidly (earthquakes, elections, major events, viral stories)
   - High-quality news outlets often report breaking news very quickly
   - Rapid growth is NORMAL and EXPECTED for legitimate news
   - **Do NOT use rapid growth to support misinformation classification**
   - Only consider it if ALL other indicators strongly suggest misinformation AND growth is extremely unusual (>15x)

2. **Source Credibility**: 
   - High-credibility sources (BBC, Reuters, AP, etc.) strongly indicate legitimate news
   - Fact-checkers present is a STRONG indicator of legitimate content
   - Multiple credible sources reporting the same story suggests legitimacy

3. **Contradictions**: 
   - Legitimate news can have different perspectives or angles on the same topic
   - Updates and corrections are normal in developing stories
   - Only consider contradictions suspicious if they involve clearly false claims

4. **Narrative Evolution**: 
   - Story updates and corrections are NORMAL in legitimate journalism
   - Breaking news stories naturally evolve as more information becomes available
   - Only suspicious if the narrative changes in ways that contradict verified facts

5. **Risk Score**: 
   - Use risk score as ONE factor, not the sole determinant
   - Low risk score with credible sources = likely legitimate
   - High risk score alone is NOT sufficient - need multiple strong indicators

## Classification Criteria

- **MISINFORMATION**: 
  - REQUIRES clear evidence of false information
  - Multiple strong red flags (e.g., low credibility + contradictions + high risk)
  - Claims that contradict verified facts from credible sources
  - Do NOT classify as misinformation based on rapid growth alone
  - Do NOT classify as misinformation if credible sources are present

- **LEGITIMATE**: 
  - Credible sources present (especially fact-checkers)
  - No major contradictions with verified facts
  - Story updates are normal and expected
  - Even with some risk indicators, if credible sources dominate, classify as legitimate

- **UNCERTAIN**: 
  - Mixed signals with no clear evidence either way
  - Moderate risk but insufficient evidence
  - When in doubt, choose UNCERTAIN rather than MISINFORMATION

## Output Format

Respond with a JSON object in this exact format:

```json
{{
    "is_misinformation": true/false,
    "confidence": 0.0-1.0,
    "classification": "misinformation" | "legitimate" | "uncertain",
    "topic_representation": "A concise, human-readable description (1-2 sentences) of what this cluster is about, e.g., 'Climate change denial claims about rising sea levels' or 'Breaking news about a natural disaster in India'",
    "evidence_chain": [
        {{
            "step": 1,
            "evidence": "Description of evidence",
            "weight": 0.0-1.0,
            "indicator": "rapid_growth" | "low_credibility" | "contradictions" | "evolution" | "other"
        }}
    ],
    "key_indicators": [
        "Indicator 1",
        "Indicator 2"
    ],
    "reasoning": "Detailed explanation of your classification decision, considering all factors",
    "supporting_evidence": [
        "Evidence that supports misinformation classification"
    ],
    "contradictory_evidence": [
        "Evidence that contradicts misinformation classification"
    ]
}}
```

## Topic Representation Guidelines

The "topic_representation" field should:
- Be concise (1-2 sentences maximum)
- Clearly describe the main topic/subject of the cluster
- Use plain, human-readable language
- Focus on WHAT the cluster is about, not the classification result
- Examples:
  - "Claims about vaccine side effects and safety concerns"
  - "News coverage of a recent earthquake in Mumbai"
  - "Social media posts questioning election results"
  - "Articles discussing climate change and global warming"

## Important Guidelines

1. **Confidence Scoring** (CRITICAL - Must be accurate and align with classification):
   - **0.9-1.0**: Very high confidence - Use ONLY when you are VERY CERTAIN
     - For "misinformation": Clear, undeniable false claims with multiple strong indicators
     - For "legitimate": Multiple credible sources, fact-checkers present, no contradictions
   - **0.7-0.9**: High confidence - Strong evidence supports your classification
     - For "misinformation": Strong indicators present, credible sources absent
     - For "legitimate": Credible sources dominate, minimal risk indicators
   - **0.5-0.7**: Moderate confidence - Some evidence but mixed signals
     - Use for "legitimate" when credible sources present but some risk indicators exist
     - Use for "uncertain" when signals are truly mixed
   - **0.3-0.5**: Low confidence - Weak evidence, high uncertainty
     - Use for "uncertain" classification when evidence is insufficient
     - Use for "legitimate" when credible sources are present but evidence is limited
   - **0.0-0.3**: Very low confidence - Insufficient data
     - Use ONLY for "uncertain" classification
   
   **IMPORTANT RULES**:
   - If classification is "legitimate", confidence should be >= 0.5 (at least moderate)
   - If classification is "misinformation", confidence should be >= 0.3 (at least low)
   - If classification is "uncertain", confidence should be <= 0.6 (at most moderate)
   - Confidence MUST reflect how certain you are about the classification
   - High confidence (>=0.7) requires strong, clear evidence
   - Low confidence (<0.5) should typically result in "uncertain" classification

2. **Evidence Chain**: Build a logical chain showing how you reached your conclusion
   - Start with strongest evidence
   - Each step should build on previous steps
   - Weight each piece of evidence (0.0-1.0)
   - **Give more weight to credible sources and fact-checkers**

3. **Be VERY Conservative**: 
   - **Default to "legitimate" or "uncertain" unless there is STRONG evidence of misinformation**
   - When uncertain, classify as "uncertain" or "legitimate" rather than "misinformation"
   - **Do NOT classify as misinformation based on risk score alone**
   - **Presence of credible sources should strongly favor "legitimate" classification**

4. **Consider Context**: 
   - Legitimate breaking news can have rapid growth - this is NORMAL
   - Different perspectives or angles are NORMAL in legitimate journalism
   - Story updates and corrections are EXPECTED in developing stories
   - Fact-checkers present is a STRONG indicator of legitimate content
   - Multiple credible sources reporting the same story suggests legitimacy

5. **Bias Against Misinformation Classification**:
   - **Require multiple strong indicators before classifying as misinformation**
   - **If credible sources are present, strongly favor "legitimate"**
   - **Rapid growth + credible sources = likely legitimate breaking news**
   - **Only classify as misinformation if there is clear evidence of false claims**

Now analyze the cluster and provide your classification in the JSON format above.
"""
        return prompt
    
    def _validate_classification_result(self, result: ClassificationResult) -> ClassificationResult:
        """
        Validate and ensure consistency of classification result.
        
        Ensures:
        - Confidence is in valid range [0.0, 1.0]
        - Classification and is_misinformation are consistent
        - Confidence aligns with classification
        """
        # Ensure confidence is in valid range
        confidence = max(0.0, min(1.0, result.confidence))
        confidence = round(confidence, 3)
        
        # Ensure classification and is_misinformation are consistent
        classification = result.classification.lower()
        is_misinformation = result.is_misinformation
        
        if classification == "misinformation":
            is_misinformation = True
        elif classification == "legitimate":
            is_misinformation = False
        elif classification == "uncertain":
            is_misinformation = False
        else:
            # If classification is invalid, infer from is_misinformation
            if is_misinformation:
                classification = "misinformation"
            else:
                classification = "uncertain"
        
        # Ensure confidence aligns with classification
        if classification == "uncertain":
            # For uncertain, cap confidence at 0.6 (moderate)
            confidence = min(confidence, 0.6)
        elif classification == "legitimate":
            # For legitimate, ensure confidence is at least 0.5 (moderate)
            confidence = max(0.5, confidence)
        elif classification == "misinformation":
            # For misinformation, ensure confidence is at least 0.3 (low)
            confidence = max(0.3, confidence)
        
        # Create validated result
        return ClassificationResult(
            is_misinformation=is_misinformation,
            confidence=confidence,
            classification=classification,
            topic_representation=result.topic_representation,
            evidence_chain=result.evidence_chain,
            key_indicators=result.key_indicators,
            reasoning=result.reasoning,
            supporting_evidence=result.supporting_evidence,
            contradictory_evidence=result.contradictory_evidence,
            sources=result.sources
        )
    
    def _parse_llm_response(self, content: str) -> ClassificationResult:
        """
        Parse LLM response and extract classification result.
        
        Handles both JSON and text responses, including markdown code blocks.
        """
        import re
        
        # Try multiple extraction strategies
        json_str = None
        
        # Strategy 1: Extract JSON from markdown code blocks
        # First find code block boundaries, then extract JSON inside
        code_block_pattern = r'```(?:json)?\s*\n?(.*?)\n?```'
        match = re.search(code_block_pattern, content, re.DOTALL)
        if match:
            potential_json = match.group(1).strip()
            # Try to find JSON object within the code block
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
        
        # Strategy 2: Find JSON object in the response (look for { ... })
        # This handles nested braces correctly
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
        
        # Strategy 3: Try parsing the entire content (in case it's pure JSON)
        if not json_str:
            json_str = content.strip()
            # Remove markdown code blocks if present
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.startswith("```"):
                json_str = json_str[3:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            json_str = json_str.strip()
        
        # Try to parse the extracted JSON
        if json_str:
            try:
                data = json.loads(json_str)
                
                # Extract and validate classification
                classification = data.get("classification", "uncertain").lower()
                is_misinformation = data.get("is_misinformation", False)
                
                # Ensure classification and is_misinformation are consistent
                if classification == "misinformation":
                    is_misinformation = True
                elif classification == "legitimate":
                    is_misinformation = False
                elif classification == "uncertain":
                    is_misinformation = False
                else:
                    # If classification doesn't match, use is_misinformation
                    if is_misinformation:
                        classification = "misinformation"
                    else:
                        classification = "uncertain"
                
                # Extract and validate confidence
                raw_confidence = data.get("confidence", 0.0)
                try:
                    confidence = float(raw_confidence)
                except (ValueError, TypeError):
                    logger.warning(f"Invalid confidence value: {raw_confidence}, defaulting to 0.5")
                    confidence = 0.5
                
                # Clamp confidence to valid range [0.0, 1.0]
                confidence = max(0.0, min(1.0, confidence))
                
                # Ensure confidence aligns with classification
                # If classified as "legitimate" with high confidence, confidence should reflect that
                # If classified as "misinformation" with high confidence, confidence should reflect that
                # If classified as "uncertain", confidence should be moderate to low
                if classification == "uncertain":
                    # For uncertain, cap confidence at 0.6 (moderate)
                    confidence = min(confidence, 0.6)
                elif classification == "legitimate" and confidence < 0.5:
                    # If legitimate but low confidence, boost it slightly (at least 0.5)
                    confidence = max(0.5, confidence)
                elif classification == "misinformation" and confidence < 0.5:
                    # If misinformation but low confidence, it's suspicious - keep it low
                    # But ensure it's at least 0.3 if classified as misinformation
                    confidence = max(0.3, confidence)
                
                # Validate and create result
                result = ClassificationResult(
                    is_misinformation=is_misinformation,
                    confidence=round(confidence, 3),  # Round to 3 decimal places
                    classification=classification,
                    topic_representation=data.get("topic_representation", "Topic not specified"),
                    evidence_chain=data.get("evidence_chain", []),
                    key_indicators=data.get("key_indicators", []),
                    reasoning=data.get("reasoning", "No reasoning provided"),
                    supporting_evidence=data.get("supporting_evidence", []),
                    contradictory_evidence=data.get("contradictory_evidence", []),
                    sources=data.get("sources", [])  # Sources will be populated from cluster_datapoints
                )
                
                # Final validation: ensure consistency
                result = self._validate_classification_result(result)
                
                # Log if confidence seems inconsistent (after validation)
                if result.classification == "legitimate" and result.confidence < 0.5:
                    logger.warning(f"Low confidence ({result.confidence}) for legitimate classification - may indicate uncertainty")
                elif result.classification == "misinformation" and result.confidence > 0.8:
                    logger.info(f"High confidence ({result.confidence}) for misinformation classification")
                elif result.classification == "uncertain" and result.confidence > 0.7:
                    logger.warning(f"High confidence ({result.confidence}) for uncertain classification - may need review")
                
                return result
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse extracted JSON: {e}")
                logger.debug(f"Extracted JSON string: {json_str[:500]}")
        
        # Fallback: try to extract key information from text
        logger.warning("JSON parsing failed, attempting text extraction")
        logger.debug(f"Full response content: {content[:1000]}")
        return self._parse_text_response(content)
    
    def _parse_text_response(self, content: str) -> ClassificationResult:
        """
        Fallback: Parse text response when JSON parsing fails.
        """
        content_lower = content.lower()
        
        # Try to extract classification
        is_misinformation = False
        if "misinformation" in content_lower and "not" not in content_lower[:50]:
            is_misinformation = True
        elif "legitimate" in content_lower or "not misinformation" in content_lower:
            is_misinformation = False
        
        # Try to extract confidence (look for numbers 0-1 or percentages)
        confidence = 0.5  # Default moderate confidence for fallback parsing
        import re
        confidence_matches = re.findall(r'(?:confidence|score)[:\s]+([0-9.]+)', content_lower)
        if confidence_matches:
            try:
                conf_val = float(confidence_matches[0])
                if conf_val > 1.0:
                    confidence = conf_val / 100.0  # Percentage
                else:
                    confidence = conf_val
            except ValueError:
                pass
        
        # Clamp confidence to valid range
        confidence = max(0.0, min(1.0, confidence))
        
        # Determine classification from extracted information
        if is_misinformation:
            classification = "misinformation"
            # If classified as misinformation, ensure confidence is at least 0.3
            confidence = max(0.3, confidence)
        elif "legitimate" in content_lower or "not misinformation" in content_lower:
            classification = "legitimate"
            is_misinformation = False
            # If legitimate, ensure confidence is at least 0.5
            confidence = max(0.5, confidence)
        else:
            classification = "uncertain"
            is_misinformation = False
            # For uncertain, cap confidence at 0.6
            confidence = min(0.6, confidence)
        
        # Try to extract topic representation from text
        topic_representation = "Topic not specified"
        # Look for patterns like "topic:", "about:", "cluster is about", etc.
        topic_patterns = [
            r'topic[:\s]+(.+?)(?:\.|$|evidence|classification)',
            r'about[:\s]+(.+?)(?:\.|$|evidence|classification)',
            r'cluster is about (.+?)(?:\.|$|evidence|classification)',
            r'subject[:\s]+(.+?)(?:\.|$|evidence|classification)'
        ]
        for pattern in topic_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                topic_representation = match.group(1).strip()
                if len(topic_representation) > 200:
                    topic_representation = topic_representation[:200] + "..."
                break
        
        # Round confidence to 3 decimal places
        confidence = round(max(0.0, min(1.0, confidence)), 3)
        
        # Create result and validate it
        result = ClassificationResult(
            is_misinformation=is_misinformation,
            confidence=confidence,
            classification=classification,
            topic_representation=topic_representation,
            evidence_chain=[{
                "step": 1,
                "evidence": "Parsed from text response (JSON parsing failed)",
                "weight": confidence,
                "indicator": "other"
            }],
            key_indicators=["LLM response parsing required manual extraction"],
            reasoning=content[:500],  # First 500 chars
            supporting_evidence=[],
            contradictory_evidence=[],
            sources=[]  # Sources will be populated from cluster_datapoints
        )
        
        # Validate the result
        return self._validate_classification_result(result)

