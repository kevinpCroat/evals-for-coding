#!/usr/bin/env python3
"""
Test script for legacy comprehension benchmark.
Compares AI answers against expected answers with fuzzy matching.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


class ComprehensionEvaluator:
    def __init__(self, questions_file: str, answers_file: str):
        self.questions = self._load_json(questions_file)
        self.answers = self._load_json(answers_file)
        self.results = {
            'total_questions': 0,
            'answered': 0,
            'correct': 0,
            'partial': 0,
            'incorrect': 0,
            'by_category': {},
            'details': []
        }

    def _load_json(self, filepath: str) -> dict:
        """Load JSON file."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {filepath}: {e}", file=sys.stderr)
            sys.exit(1)

    def _normalize_text(self, text: str) -> str:
        """Normalize text for comparison."""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _keyword_match_score(self, answer: str, keywords: List[str]) -> float:
        """Calculate keyword match score."""
        normalized = self._normalize_text(answer)
        matched = 0
        for keyword in keywords:
            if self._normalize_text(keyword) in normalized:
                matched += 1
        return matched / len(keywords) if keywords else 0

    def _similarity_score(self, answer: str, expected: str) -> float:
        """Calculate similarity between answer and expected answer."""
        answer_normalized = self._normalize_text(answer)
        expected_normalized = self._normalize_text(expected)

        # Split into words
        answer_words = set(answer_normalized.split())
        expected_words = set(expected_normalized.split())

        if not expected_words:
            return 0

        # Calculate Jaccard similarity
        intersection = answer_words & expected_words
        union = answer_words | expected_words

        return len(intersection) / len(union) if union else 0

    def _categorize_score(self, score: float) -> str:
        """Categorize score into correct/partial/incorrect."""
        if score >= 0.7:
            return 'correct'
        elif score >= 0.4:
            return 'partial'
        else:
            return 'incorrect'

    def _evaluate_answer(self, question: dict, answer_text: str) -> Dict:
        """Evaluate a single answer."""
        # Calculate keyword match score
        keyword_score = self._keyword_match_score(
            answer_text,
            question.get('keywords', [])
        )

        # Calculate similarity to expected answer
        similarity = self._similarity_score(
            answer_text,
            question['answer']
        )

        # Combined score (weighted average)
        # Keywords are more important (60%) than overall similarity (40%)
        combined_score = (keyword_score * 0.6) + (similarity * 0.4)

        category = self._categorize_score(combined_score)

        return {
            'question_id': question['id'],
            'category': question['category'],
            'keyword_score': keyword_score,
            'similarity_score': similarity,
            'combined_score': combined_score,
            'result': category,
            'weight': question.get('weight', 1.0)
        }

    def evaluate(self) -> Dict:
        """Evaluate all answers."""
        questions_list = self.questions.get('questions', [])
        answers_list = self.answers.get('answers', [])

        # Create answer lookup
        answer_lookup = {a['id']: a['answer'] for a in answers_list}

        self.results['total_questions'] = len(questions_list)

        for question in questions_list:
            qid = question['id']
            category = question['category']

            # Initialize category if not exists
            if category not in self.results['by_category']:
                self.results['by_category'][category] = {
                    'total': 0,
                    'correct': 0,
                    'partial': 0,
                    'incorrect': 0,
                    'unanswered': 0,
                    'weighted_score': 0,
                    'total_weight': 0
                }

            cat_stats = self.results['by_category'][category]
            cat_stats['total'] += 1

            if qid not in answer_lookup:
                # Unanswered question
                result = {
                    'question_id': qid,
                    'category': category,
                    'result': 'unanswered',
                    'combined_score': 0,
                    'weight': question.get('weight', 1.0)
                }
                cat_stats['unanswered'] += 1
            else:
                # Evaluate answer
                self.results['answered'] += 1
                result = self._evaluate_answer(question, answer_lookup[qid])
                cat_stats[result['result']] += 1
                cat_stats['weighted_score'] += result['combined_score'] * result['weight']
                cat_stats['total_weight'] += result['weight']

                # Update global counts
                if result['result'] == 'correct':
                    self.results['correct'] += 1
                elif result['result'] == 'partial':
                    self.results['partial'] += 1
                else:
                    self.results['incorrect'] += 1

            self.results['details'].append(result)

        return self.results

    def calculate_scores(self) -> Dict[str, float]:
        """Calculate final scores for each component."""
        details = self.results['details']

        # Q&A Accuracy (40%) - based on combined scores
        qa_scores = [d['combined_score'] * d['weight'] for d in details]
        total_weight = sum(d['weight'] for d in details)
        qa_accuracy = sum(qa_scores) / total_weight if total_weight > 0 else 0

        # Dependency Mapping (30%) - dependency category questions
        dep_questions = [d for d in details if d['category'] == 'dependencies']
        if dep_questions:
            dep_scores = [d['combined_score'] * d['weight'] for d in dep_questions]
            dep_weight = sum(d['weight'] for d in dep_questions)
            dep_mapping = sum(dep_scores) / dep_weight
        else:
            dep_mapping = 0

        # Impact Analysis (20%) - change_impact category
        impact_questions = [d for d in details if d['category'] == 'change_impact']
        if impact_questions:
            impact_scores = [d['combined_score'] * d['weight'] for d in impact_questions]
            impact_weight = sum(d['weight'] for d in impact_questions)
            impact_analysis = sum(impact_scores) / impact_weight
        else:
            impact_analysis = 0

        # Analysis Quality (10%) - architecture and business_logic categories
        analysis_questions = [d for d in details if d['category'] in ['architecture', 'business_logic', 'data_flow']]
        if analysis_questions:
            analysis_scores = [d['combined_score'] * d['weight'] for d in analysis_questions]
            analysis_weight = sum(d['weight'] for d in analysis_questions)
            analysis_quality = sum(analysis_scores) / analysis_weight
        else:
            analysis_quality = 0

        # Final weighted score
        final_score = (
            qa_accuracy * 0.4 +
            dep_mapping * 0.3 +
            impact_analysis * 0.2 +
            analysis_quality * 0.1
        )

        return {
            'qa_accuracy': qa_accuracy,
            'dependency_mapping': dep_mapping,
            'impact_analysis': impact_analysis,
            'analysis_quality': analysis_quality,
            'final_score': final_score
        }

    def print_summary(self):
        """Print evaluation summary."""
        print("\n" + "="*60)
        print("LEGACY CODE COMPREHENSION - EVALUATION RESULTS")
        print("="*60)

        print(f"\nQuestions Overview:")
        print(f"  Total Questions:    {self.results['total_questions']}")
        print(f"  Answered:           {self.results['answered']}")
        print(f"  Correct:            {self.results['correct']}")
        print(f"  Partial Credit:     {self.results['partial']}")
        print(f"  Incorrect:          {self.results['incorrect']}")
        print(f"  Unanswered:         {self.results['total_questions'] - self.results['answered']}")

        print(f"\nBy Category:")
        for category, stats in sorted(self.results['by_category'].items()):
            avg_score = stats['weighted_score'] / stats['total_weight'] if stats['total_weight'] > 0 else 0
            print(f"  {category:20s}: {stats['correct']}/{stats['total']} correct, "
                  f"{stats['partial']} partial, {stats['incorrect']} incorrect, "
                  f"{stats['unanswered']} unanswered (avg: {avg_score:.2%})")

        scores = self.calculate_scores()
        print(f"\nComponent Scores:")
        print(f"  Q&A Accuracy (40%):        {scores['qa_accuracy']:.2%}")
        print(f"  Dependency Mapping (30%):  {scores['dependency_mapping']:.2%}")
        print(f"  Impact Analysis (20%):     {scores['impact_analysis']:.2%}")
        print(f"  Analysis Quality (10%):    {scores['analysis_quality']:.2%}")
        print(f"\n  FINAL SCORE:               {scores['final_score']:.2%}")
        print("="*60 + "\n")

    def generate_json_output(self) -> Dict:
        """Generate JSON output for verification script."""
        scores = self.calculate_scores()

        return {
            'benchmark': 'legacy-comprehension-001',
            'passed': scores['final_score'] >= 0.7,
            'score': round(scores['final_score'] * 100, 2),
            'max_score': 100,
            'components': {
                'qa_accuracy': {
                    'score': round(scores['qa_accuracy'] * 100, 2),
                    'weight': 40,
                    'weighted_score': round(scores['qa_accuracy'] * 40, 2)
                },
                'dependency_mapping': {
                    'score': round(scores['dependency_mapping'] * 100, 2),
                    'weight': 30,
                    'weighted_score': round(scores['dependency_mapping'] * 30, 2)
                },
                'impact_analysis': {
                    'score': round(scores['impact_analysis'] * 100, 2),
                    'weight': 20,
                    'weighted_score': round(scores['impact_analysis'] * 20, 2)
                },
                'analysis_quality': {
                    'score': round(scores['analysis_quality'] * 100, 2),
                    'weight': 10,
                    'weighted_score': round(scores['analysis_quality'] * 10, 2)
                }
            },
            'summary': {
                'total_questions': self.results['total_questions'],
                'answered': self.results['answered'],
                'correct': self.results['correct'],
                'partial': self.results['partial'],
                'incorrect': self.results['incorrect'],
                'unanswered': self.results['total_questions'] - self.results['answered']
            },
            'details': self.results['details']
        }


def main():
    if len(sys.argv) != 3:
        print("Usage: test_comprehension.py <questions.json> <answers.json>")
        sys.exit(1)

    questions_file = sys.argv[1]
    answers_file = sys.argv[2]

    evaluator = ComprehensionEvaluator(questions_file, answers_file)
    evaluator.evaluate()
    evaluator.print_summary()

    # Output JSON for verification script
    output = evaluator.generate_json_output()
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
