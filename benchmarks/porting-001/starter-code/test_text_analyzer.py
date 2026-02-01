"""
Comprehensive test suite for text_analyzer module.

These tests should be ported to JavaScript/TypeScript along with the main code.
All test cases must pass in the target language.
"""

import pytest
from text_analyzer import (
    TextAnalyzer,
    tokenize,
    char_frequency_analysis,
    find_palindromes,
    group_by_length,
    calculate_reading_metrics,
    extract_acronyms,
    title_case_special,
    remove_duplicate_words
)


class TestTextAnalyzer:
    """Test cases for TextAnalyzer class."""

    def test_initialization(self):
        """Test analyzer initialization."""
        text = "Hello world! This is a test."
        analyzer = TextAnalyzer(text)
        assert analyzer.text == text
        assert len(analyzer.words) > 0

    def test_word_count(self):
        """Test word counting."""
        analyzer = TextAnalyzer("The quick brown fox jumps over the lazy dog")
        assert analyzer.word_count() == 9

    def test_word_count_empty(self):
        """Test word count with empty text."""
        analyzer = TextAnalyzer("")
        assert analyzer.word_count() == 0

    def test_unique_words(self):
        """Test unique word extraction."""
        analyzer = TextAnalyzer("the cat and the dog")
        unique = analyzer.unique_words()
        assert unique == {"the", "cat", "and", "dog"}

    def test_word_frequency(self):
        """Test word frequency counting."""
        analyzer = TextAnalyzer("the cat and the dog and the bird")
        freq = analyzer.word_frequency()
        assert freq["the"] == 3
        assert freq["and"] == 2
        assert freq["cat"] == 1

    def test_most_common_words(self):
        """Test most common words extraction."""
        analyzer = TextAnalyzer("a b c a b a")
        common = analyzer.most_common_words(2)
        assert common[0] == ("a", 3)
        assert common[1] == ("b", 2)

    def test_average_word_length(self):
        """Test average word length calculation."""
        analyzer = TextAnalyzer("cat dog bird")  # lengths: 3, 3, 4
        avg = analyzer.average_word_length()
        assert abs(avg - 3.333) < 0.01

    def test_average_word_length_empty(self):
        """Test average word length with empty text."""
        analyzer = TextAnalyzer("")
        assert analyzer.average_word_length() == 0.0

    def test_longest_words(self):
        """Test longest words extraction."""
        analyzer = TextAnalyzer("a bb ccc dddd eeeee")
        longest = analyzer.longest_words(3)
        assert longest == ["eeeee", "dddd", "ccc"]

    def test_punctuation_handling(self):
        """Test that punctuation is properly removed."""
        analyzer = TextAnalyzer("Hello, world! How are you?")
        assert "hello" in analyzer.words
        assert "world" in analyzer.words
        assert "," not in analyzer.words


class TestTokenize:
    """Test cases for tokenize function."""

    def test_basic_tokenization(self):
        """Test basic word tokenization."""
        tokens = tokenize("Hello world test")
        assert tokens == ["hello", "world", "test"]

    def test_tokenize_with_punctuation(self):
        """Test tokenization removes punctuation."""
        tokens = tokenize("Hello, world! How are you?")
        assert tokens == ["hello", "world", "how", "are", "you"]

    def test_tokenize_preserve_case(self):
        """Test tokenization preserving case."""
        tokens = tokenize("Hello World", lowercase=False)
        assert tokens == ["Hello", "World"]

    def test_tokenize_empty(self):
        """Test tokenization of empty string."""
        tokens = tokenize("")
        assert tokens == []


class TestCharFrequencyAnalysis:
    """Test cases for character frequency analysis."""

    def test_char_frequency_basic(self):
        """Test basic character frequency."""
        freq = char_frequency_analysis("hello")
        assert freq == {"h": 1, "e": 1, "l": 2, "o": 1}

    def test_char_frequency_ignore_case(self):
        """Test character frequency ignoring case."""
        freq = char_frequency_analysis("AaBb", ignore_case=True)
        assert freq == {"a": 2, "b": 2}

    def test_char_frequency_preserve_case(self):
        """Test character frequency preserving case."""
        freq = char_frequency_analysis("AaBb", ignore_case=False)
        assert freq == {"A": 1, "a": 1, "B": 1, "b": 1}

    def test_char_frequency_filters_whitespace(self):
        """Test that whitespace is filtered out."""
        freq = char_frequency_analysis("a b c")
        assert " " not in freq
        assert freq == {"a": 1, "b": 1, "c": 1}


class TestFindPalindromes:
    """Test cases for palindrome detection."""

    def test_find_palindromes_basic(self):
        """Test basic palindrome detection."""
        words = ["racecar", "hello", "level", "world"]
        palindromes = find_palindromes(words)
        assert set(palindromes) == {"racecar", "level"}

    def test_find_palindromes_min_length(self):
        """Test palindrome detection with minimum length."""
        words = ["a", "aa", "aba", "abba"]
        palindromes = find_palindromes(words, min_length=3)
        assert set(palindromes) == {"aba", "abba"}

    def test_find_palindromes_case_insensitive(self):
        """Test palindromes are case-insensitive."""
        words = ["Racecar", "Level"]
        palindromes = find_palindromes(words)
        assert "Racecar" in palindromes or "racecar" in palindromes

    def test_find_palindromes_empty(self):
        """Test palindrome detection with empty list."""
        palindromes = find_palindromes([])
        assert palindromes == []

    def test_find_palindromes_deduplication(self):
        """Test that duplicates are removed."""
        words = ["level", "level", "kayak", "kayak"]
        palindromes = find_palindromes(words)
        assert len(palindromes) == 2


class TestGroupByLength:
    """Test cases for grouping words by length."""

    def test_group_by_length_basic(self):
        """Test basic grouping by length."""
        words = ["a", "bb", "ccc", "dd", "e"]
        grouped = group_by_length(words)
        assert grouped[1] == ["a", "e"]
        assert grouped[2] == ["bb", "dd"]
        assert grouped[3] == ["ccc"]

    def test_group_by_length_empty(self):
        """Test grouping empty list."""
        grouped = group_by_length([])
        assert grouped == {}

    def test_group_by_length_preserves_order(self):
        """Test that word order is preserved within groups."""
        words = ["cat", "dog", "ant", "bee"]
        grouped = group_by_length(words)
        assert grouped[3] == ["cat", "dog", "ant", "bee"]


class TestCalculateReadingMetrics:
    """Test cases for reading metrics calculation."""

    def test_reading_metrics_basic(self):
        """Test basic reading metrics."""
        text = "Hello world. This is a test."
        metrics = calculate_reading_metrics(text)
        assert metrics["sentence_count"] == 2
        assert metrics["word_count"] == 6
        assert metrics["character_count"] == len(text)

    def test_reading_metrics_avg_sentence_length(self):
        """Test average sentence length calculation."""
        text = "One two three. Four five six."
        metrics = calculate_reading_metrics(text)
        assert metrics["avg_sentence_length"] == 3.0

    def test_reading_metrics_empty(self):
        """Test metrics with empty text."""
        metrics = calculate_reading_metrics("")
        assert metrics["sentence_count"] == 0
        assert metrics["word_count"] == 0

    def test_reading_metrics_multiple_punctuation(self):
        """Test sentence detection with various punctuation."""
        text = "Question? Answer! Statement."
        metrics = calculate_reading_metrics(text)
        assert metrics["sentence_count"] == 3


class TestExtractAcronyms:
    """Test cases for acronym extraction."""

    def test_extract_acronyms_basic(self):
        """Test basic acronym extraction."""
        text = "The FBI and CIA work together. USA is great."
        acronyms = extract_acronyms(text)
        assert set(acronyms) == {"FBI", "CIA", "USA"}

    def test_extract_acronyms_sorted(self):
        """Test that acronyms are sorted."""
        text = "USA FBI CIA"
        acronyms = extract_acronyms(text)
        assert acronyms == ["CIA", "FBI", "USA"]

    def test_extract_acronyms_min_length(self):
        """Test that single letters are excluded."""
        text = "I love the FBI"
        acronyms = extract_acronyms(text)
        assert "I" not in acronyms
        assert "FBI" in acronyms

    def test_extract_acronyms_empty(self):
        """Test acronym extraction with no acronyms."""
        text = "Hello world this is a test"
        acronyms = extract_acronyms(text)
        assert acronyms == []


class TestTitleCaseSpecial:
    """Test cases for special title case conversion."""

    def test_title_case_basic(self):
        """Test basic title case conversion."""
        result = title_case_special("the quick brown fox")
        assert result == "The Quick Brown Fox"

    def test_title_case_minor_words(self):
        """Test that minor words are lowercase."""
        result = title_case_special("the lord of the rings")
        assert result == "The Lord of the Rings"

    def test_title_case_first_last_capitalized(self):
        """Test that first and last words are always capitalized."""
        result = title_case_special("a tale of two cities")
        assert result == "A Tale of Two Cities"

    def test_title_case_custom_minor_words(self):
        """Test with custom minor words set."""
        result = title_case_special("hello from the world", minor_words={"from"})
        assert result == "Hello from The World"

    def test_title_case_empty(self):
        """Test with empty string."""
        result = title_case_special("")
        assert result == ""

    def test_title_case_single_word(self):
        """Test with single word."""
        result = title_case_special("hello")
        assert result == "Hello"


class TestRemoveDuplicateWords:
    """Test cases for duplicate word removal."""

    def test_remove_duplicates_preserve_order(self):
        """Test duplicate removal preserving order."""
        text = "the cat and the dog and the bird"
        result = remove_duplicate_words(text, preserve_order=True)
        assert result == "the cat and dog bird"

    def test_remove_duplicates_sorted(self):
        """Test duplicate removal with sorting."""
        text = "zebra apple banana apple"
        result = remove_duplicate_words(text, preserve_order=False)
        assert result == "apple banana zebra"

    def test_remove_duplicates_case_insensitive(self):
        """Test that duplicates are case-insensitive."""
        text = "Hello world hello WORLD"
        result = remove_duplicate_words(text, preserve_order=True)
        words = result.split()
        assert len(words) == 2

    def test_remove_duplicates_empty(self):
        """Test with empty string."""
        result = remove_duplicate_words("")
        assert result == ""

    def test_remove_duplicates_no_duplicates(self):
        """Test when there are no duplicates."""
        text = "one two three"
        result = remove_duplicate_words(text)
        assert result == "one two three"
