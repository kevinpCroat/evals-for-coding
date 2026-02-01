#!/usr/bin/env python3
"""
LLM-as-judge evaluator for architecture design benchmark.
Uses Claude API to score architectural decisions based on evaluation criteria.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Try to import anthropic, fall back gracefully if not available
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic package not available. Install with: pip install anthropic", file=sys.stderr)


class ArchitectureEvaluator:
    """Evaluates architecture submissions using LLM-as-judge approach."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize evaluator with API key."""
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key and ANTHROPIC_AVAILABLE:
            print("Warning: ANTHROPIC_API_KEY not set. Evaluation will fail.", file=sys.stderr)

        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            self.client = None

    def read_file_safe(self, filepath: Path) -> str:
        """Read file content safely, returning empty string if not found."""
        try:
            if filepath.exists():
                return filepath.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return ""

    def check_file_exists(self, base_dir: Path, filepath: str) -> bool:
        """Check if a required file exists."""
        return (base_dir / filepath).exists()

    def evaluate_adr_quality(self, base_dir: Path) -> Tuple[float, str]:
        """Evaluate ADR quality (30% weight)."""
        adrs_dir = base_dir / "adrs"

        if not adrs_dir.exists():
            return 0.0, "ADRs directory not found"

        adr_files = list(adrs_dir.glob("*.md"))

        if len(adr_files) == 0:
            return 0.0, "No ADR files found"

        if len(adr_files) < 3:
            return 30.0, f"Only {len(adr_files)} ADRs found (minimum 3 recommended)"

        # Read all ADRs
        adrs_content = []
        for adr_file in adr_files[:5]:  # Limit to first 5 ADRs
            content = self.read_file_safe(adr_file)
            adrs_content.append(f"=== {adr_file.name} ===\n{content}\n")

        combined_adrs = "\n".join(adrs_content)

        # Check for basic ADR structure
        structure_score = 0
        required_sections = ["Status", "Context", "Decision", "Consequences", "Alternatives"]
        sections_found = sum(1 for section in required_sections if section.lower() in combined_adrs.lower())
        structure_score = (sections_found / len(required_sections)) * 30

        if not self.client:
            # Fallback scoring without LLM
            details = f"Found {len(adr_files)} ADRs with {sections_found}/{len(required_sections)} required sections"
            return min(structure_score + 20, 80), details

        # LLM evaluation prompt
        evaluation_prompt = f"""You are evaluating Architecture Decision Records (ADRs) for a software architecture design task.

ADRs Content:
{combined_adrs[:15000]}  # Limit content size

Evaluate the ADRs on the following criteria:

1. Format and Structure (20 points):
   - Do they follow a consistent format?
   - Are all required sections present (Status, Context, Decision, Consequences, Alternatives)?
   - Is the writing clear and well-organized?

2. Depth of Reasoning (40 points):
   - Is the context well-explained with relevant constraints?
   - Are decisions specific and concrete (not vague)?
   - Are consequences thoroughly analyzed (both positive and negative)?
   - Is the reasoning sound and justified?

3. Alternatives Analysis (40 points):
   - Are 2-3 alternatives considered for each decision?
   - Are pros/cons of alternatives clearly stated?
   - Is the reason for rejecting alternatives well-justified?
   - Does the analysis show critical thinking?

Provide your evaluation as a JSON object:
{{
  "format_structure_score": 0-20,
  "reasoning_depth_score": 0-40,
  "alternatives_analysis_score": 0-40,
  "total_score": 0-100,
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "summary": "Brief 1-2 sentence summary"
}}

Be objective and fair. Consider that multiple valid architectural approaches exist."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": evaluation_prompt}]
            )

            # Extract JSON from response
            response_text = response.content[0].text
            # Find JSON in response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result = json.loads(response_text[json_start:json_end])
                score = result.get('total_score', 50)
                details = result.get('summary', 'ADR evaluation completed')
                return score, details
            else:
                return 50.0, "Could not parse LLM evaluation response"

        except Exception as e:
            print(f"Error in LLM evaluation: {e}", file=sys.stderr)
            return structure_score + 20, f"LLM evaluation failed, using structural analysis"

    def evaluate_diagram_completeness(self, base_dir: Path) -> Tuple[float, str]:
        """Evaluate diagram completeness (20% weight)."""
        diagrams_dir = base_dir / "diagrams"

        if not diagrams_dir.exists():
            return 0.0, "Diagrams directory not found"

        required_diagrams = {
            "component-diagram.md": "Component diagram",
            "deployment-diagram.md": "Deployment diagram",
            "data-flow-diagram.md": "Data flow diagram"
        }

        found_diagrams = []
        missing_diagrams = []
        total_content_length = 0

        for filename, description in required_diagrams.items():
            filepath = diagrams_dir / filename
            if filepath.exists():
                content = self.read_file_safe(filepath)
                total_content_length += len(content)
                found_diagrams.append(description)
            else:
                missing_diagrams.append(description)

        # Base score on presence of diagrams
        base_score = (len(found_diagrams) / len(required_diagrams)) * 60

        # Bonus for substantial content (diagrams should have reasonable length)
        if total_content_length > 1000:
            content_bonus = min(40, (total_content_length / 3000) * 40)
        else:
            content_bonus = (total_content_length / 1000) * 20

        score = base_score + content_bonus

        if missing_diagrams:
            details = f"Found {len(found_diagrams)}/3 required diagrams. Missing: {', '.join(missing_diagrams)}"
        else:
            details = f"All required diagrams present ({total_content_length} chars total)"

        return min(score, 100), details

    def evaluate_tradeoff_analysis(self, base_dir: Path) -> Tuple[float, str]:
        """Evaluate trade-off analysis (25% weight)."""
        tradeoffs_file = base_dir / "trade-offs.md"

        if not tradeoffs_file.exists():
            # Try alternative naming
            alt_file = base_dir / "tradeoffs.md"
            if alt_file.exists():
                tradeoffs_file = alt_file
            else:
                return 0.0, "trade-offs.md not found"

        content = self.read_file_safe(tradeoffs_file)

        if len(content) < 500:
            return 20.0, f"Trade-offs analysis too brief ({len(content)} chars)"

        # Check for key terms indicating good analysis
        quality_indicators = [
            "alternative", "pros", "cons", "trade-off", "tradeoff",
            "advantage", "disadvantage", "risk", "benefit", "cost"
        ]

        indicators_found = sum(1 for indicator in quality_indicators
                              if indicator in content.lower())

        # Basic scoring based on length and key terms
        length_score = min(30, (len(content) / 2000) * 30)
        indicators_score = min(30, (indicators_found / len(quality_indicators)) * 40)

        if not self.client:
            score = length_score + indicators_score
            details = f"Found {indicators_found} quality indicators in {len(content)} chars"
            return min(score, 80), details

        # LLM evaluation
        evaluation_prompt = f"""You are evaluating a trade-offs analysis document for a software architecture design.

Trade-offs Analysis Content:
{content[:10000]}  # Limit content size

Evaluate the trade-offs analysis on:

1. Breadth of Analysis (30 points):
   - Are multiple major architectural decisions covered?
   - Are diverse aspects considered (performance, cost, complexity, scalability)?

2. Depth of Analysis (40 points):
   - Are alternatives clearly described?
   - Are pros/cons explicitly stated for each alternative?
   - Is the reasoning for choices well-justified?
   - Are trade-offs realistic and honest (acknowledging sacrifices)?

3. Critical Thinking (30 points):
   - Does the analysis show understanding of real-world constraints?
   - Are risks and mitigation strategies discussed?
   - Does it avoid being one-sided or superficial?

Provide your evaluation as JSON:
{{
  "breadth_score": 0-30,
  "depth_score": 0-40,
  "critical_thinking_score": 0-30,
  "total_score": 0-100,
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "summary": "Brief 1-2 sentence summary"
}}"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": evaluation_prompt}]
            )

            response_text = response.content[0].text
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result = json.loads(response_text[json_start:json_end])
                score = result.get('total_score', 50)
                details = result.get('summary', 'Trade-offs evaluation completed')
                return score, details
            else:
                return 50.0, "Could not parse LLM evaluation response"

        except Exception as e:
            print(f"Error in LLM evaluation: {e}", file=sys.stderr)
            return length_score + indicators_score, "LLM evaluation failed"

    def evaluate_technical_soundness(self, base_dir: Path) -> Tuple[float, str]:
        """Evaluate technical soundness (25% weight)."""
        architecture_file = base_dir / "architecture.md"

        if not architecture_file.exists():
            return 0.0, "architecture.md not found"

        content = self.read_file_safe(architecture_file)
        requirements_content = self.read_file_safe(base_dir / "requirements.md")

        if len(content) < 1000:
            return 20.0, f"Architecture document too brief ({len(content)} chars)"

        # Check for coverage of key topics
        key_topics = {
            "scalability": ["scale", "horizontal", "vertical", "replicas", "sharding"],
            "performance": ["latency", "throughput", "performance", "cache", "optimization"],
            "reliability": ["availability", "redundancy", "failover", "backup", "disaster recovery"],
            "security": ["authentication", "authorization", "encryption", "security", "compliance"],
            "technology": ["database", "api", "protocol", "framework", "infrastructure"]
        }

        topics_covered = 0
        for topic, keywords in key_topics.items():
            if any(keyword in content.lower() for keyword in keywords):
                topics_covered += 1

        coverage_score = (topics_covered / len(key_topics)) * 40

        # Check document structure
        structure_score = 0
        if len(content) > 2000:
            structure_score += 20
        if "##" in content or "###" in content:  # Has sections
            structure_score += 10

        if not self.client:
            score = coverage_score + structure_score
            details = f"Covers {topics_covered}/{len(key_topics)} key topics in {len(content)} chars"
            return min(score, 80), details

        # LLM evaluation
        evaluation_prompt = f"""You are evaluating a system architecture document for technical soundness.

Requirements (for reference):
{requirements_content[:3000]}

Architecture Document:
{content[:12000]}

Evaluate on:

1. Requirements Coverage (30 points):
   - Does it address the key requirements (100k concurrent users, <100ms latency, 99.9% availability)?
   - Are scalability, security, and compliance needs addressed?

2. Technical Feasibility (40 points):
   - Are technology choices appropriate and justified?
   - Is the architecture realistic and implementable?
   - Are there any obvious technical flaws or impossibilities?
   - Do the components work together coherently?

3. Completeness (30 points):
   - Are all major system components described?
   - Is the technology stack specified?
   - Are operational concerns (monitoring, deployment, DR) addressed?

Provide evaluation as JSON:
{{
  "requirements_coverage_score": 0-30,
  "technical_feasibility_score": 0-40,
  "completeness_score": 0-30,
  "total_score": 0-100,
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "summary": "Brief 1-2 sentence summary"
}}"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": evaluation_prompt}]
            )

            response_text = response.content[0].text
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result = json.loads(response_text[json_start:json_end])
                score = result.get('total_score', 50)
                details = result.get('summary', 'Technical soundness evaluation completed')
                return score, details
            else:
                return 50.0, "Could not parse LLM evaluation response"

        except Exception as e:
            print(f"Error in LLM evaluation: {e}", file=sys.stderr)
            return coverage_score + structure_score, "LLM evaluation failed"

    def evaluate(self, submission_dir: str) -> Dict:
        """Run full evaluation and return results."""
        base_dir = Path(submission_dir)

        # Run evaluations
        adr_score, adr_details = self.evaluate_adr_quality(base_dir)
        diagram_score, diagram_details = self.evaluate_diagram_completeness(base_dir)
        tradeoff_score, tradeoff_details = self.evaluate_tradeoff_analysis(base_dir)
        technical_score, technical_details = self.evaluate_technical_soundness(base_dir)

        # Calculate weighted score
        components = {
            "adr_quality": {
                "score": round(adr_score, 2),
                "weight": 0.30,
                "details": adr_details
            },
            "diagram_completeness": {
                "score": round(diagram_score, 2),
                "weight": 0.20,
                "details": diagram_details
            },
            "tradeoff_analysis": {
                "score": round(tradeoff_score, 2),
                "weight": 0.25,
                "details": tradeoff_details
            },
            "technical_soundness": {
                "score": round(technical_score, 2),
                "weight": 0.25,
                "details": technical_details
            }
        }

        # Calculate base score
        base_score = sum(
            comp["score"] * comp["weight"]
            for comp in components.values()
        )

        # Determine pass/fail (>70 to pass)
        passed = base_score >= 70

        return {
            "benchmark": "architecture-001",
            "components": components,
            "base_score": round(base_score, 2),
            "penalties": {
                "time_penalty": 0.0,
                "iteration_penalty": 0.0,
                "error_penalty": 0.0
            },
            "final_score": round(base_score, 2),
            "passed": passed
        }


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Evaluate architecture design submission')
    parser.add_argument('submission_dir', help='Directory containing architecture submission')
    parser.add_argument('--api-key', help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')

    args = parser.parse_args()

    evaluator = ArchitectureEvaluator(api_key=args.api_key)
    results = evaluator.evaluate(args.submission_dir)

    print(json.dumps(results, indent=2))

    # Exit with appropriate code
    sys.exit(0 if results['passed'] else 1)


if __name__ == '__main__':
    main()
