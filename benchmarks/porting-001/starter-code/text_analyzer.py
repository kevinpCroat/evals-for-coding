"""
Text Analysis Utility Module

A comprehensive text processing library with various analysis and transformation
functions. This module demonstrates common Python patterns including list
comprehensions, defaultdict, set operations, and string manipulation.
"""

from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set, Optional
import re


class TextAnalyzer:
    """Analyzes text content with various metrics and transformations."""

    def __init__(self, text: str):
        """
        Initialize the analyzer with text content.

        Args:
            text: The text to analyze
        """
        self.text = text
        self.words = self._extract_words(text)

    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text, removing punctuation."""
        return [word.lower() for word in re.findall(r'\b\w+\b', text)]

    def word_count(self) -> int:
        """Return the total number of words."""
        return len(self.words)

    def unique_words(self) -> Set[str]:
        """Return a set of unique words."""
        return set(self.words)

    def word_frequency(self) -> Dict[str, int]:
        """
        Return a dictionary of word frequencies.

        Returns:
            Dictionary mapping words to their occurrence counts
        """
        return dict(Counter(self.words))

    def most_common_words(self, n: int = 5) -> List[Tuple[str, int]]:
        """
        Return the n most common words with their frequencies.

        Args:
            n: Number of top words to return

        Returns:
            List of (word, count) tuples sorted by frequency
        """
        return Counter(self.words).most_common(n)

    def average_word_length(self) -> float:
        """Calculate the average length of words."""
        if not self.words:
            return 0.0
        return sum(len(word) for word in self.words) / len(self.words)

    def longest_words(self, n: int = 3) -> List[str]:
        """
        Return the n longest words.

        Args:
            n: Number of longest words to return

        Returns:
            List of longest words, sorted by length descending
        """
        unique_sorted = sorted(set(self.words), key=len, reverse=True)
        return unique_sorted[:n]


def tokenize(text: str, lowercase: bool = True) -> List[str]:
    """
    Tokenize text into words.

    Args:
        text: Input text to tokenize
        lowercase: Whether to convert to lowercase

    Returns:
        List of tokens
    """
    words = re.findall(r'\b\w+\b', text)
    return [w.lower() for w in words] if lowercase else words


def char_frequency_analysis(text: str, ignore_case: bool = True) -> Dict[str, int]:
    """
    Analyze character frequency in text.

    Args:
        text: Text to analyze
        ignore_case: Whether to treat upper and lower case as same

    Returns:
        Dictionary mapping characters to their counts
    """
    processed_text = text.lower() if ignore_case else text
    # Filter out whitespace and only count alphanumeric
    chars = [c for c in processed_text if c.isalnum()]
    return dict(Counter(chars))


def find_palindromes(words: List[str], min_length: int = 3) -> List[str]:
    """
    Find palindrome words in a list.

    Args:
        words: List of words to check
        min_length: Minimum length for palindromes

    Returns:
        List of palindrome words (deduplicated and sorted)
    """
    palindromes = [
        word for word in words
        if len(word) >= min_length and word.lower() == word.lower()[::-1]
    ]
    return sorted(set(palindromes))


def group_by_length(words: List[str]) -> Dict[int, List[str]]:
    """
    Group words by their length.

    Args:
        words: List of words to group

    Returns:
        Dictionary mapping lengths to lists of words
    """
    grouped = defaultdict(list)
    for word in words:
        grouped[len(word)].append(word)
    return dict(grouped)


def calculate_reading_metrics(text: str) -> Dict[str, float]:
    """
    Calculate various reading metrics for text.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with metrics including sentence count, avg sentence length, etc.
    """
    # Split into sentences (simple approach)
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    words = tokenize(text)

    metrics = {
        'sentence_count': len(sentences),
        'word_count': len(words),
        'character_count': len(text),
        'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
        'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0
    }

    return metrics


def extract_acronyms(text: str) -> List[str]:
    """
    Extract potential acronyms (all-caps words of 2+ letters).

    Args:
        text: Text to scan for acronyms

    Returns:
        List of unique acronyms found, sorted alphabetically
    """
    # Find sequences of 2 or more capital letters
    acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
    return sorted(set(acronyms))


def title_case_special(text: str, minor_words: Optional[Set[str]] = None) -> str:
    """
    Convert text to title case with special rules for minor words.

    Minor words (articles, conjunctions, prepositions) are lowercase
    unless they're the first or last word.

    Args:
        text: Text to convert
        minor_words: Set of words to keep lowercase (default: common articles/prepositions)

    Returns:
        Title-cased string
    """
    if minor_words is None:
        minor_words = {'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor',
                      'on', 'at', 'to', 'from', 'by', 'in', 'of'}

    words = text.split()
    if not words:
        return text

    # First word is always capitalized
    result = [words[0].capitalize()]

    # Middle words
    for word in words[1:-1]:
        if word.lower() in minor_words:
            result.append(word.lower())
        else:
            result.append(word.capitalize())

    # Last word is always capitalized (if more than one word)
    if len(words) > 1:
        result.append(words[-1].capitalize())

    return ' '.join(result)


def remove_duplicate_words(text: str, preserve_order: bool = True) -> str:
    """
    Remove duplicate words from text.

    Args:
        text: Input text
        preserve_order: If True, preserve first occurrence order;
                       if False, sort alphabetically

    Returns:
        Text with duplicates removed
    """
    words = text.split()

    if preserve_order:
        seen = set()
        unique_words = []
        for word in words:
            word_lower = word.lower()
            if word_lower not in seen:
                seen.add(word_lower)
                unique_words.append(word)
        return ' '.join(unique_words)
    else:
        unique_words = sorted(set(word.lower() for word in words))
        return ' '.join(unique_words)
