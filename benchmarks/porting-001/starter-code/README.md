# Text Analyzer - Python Implementation

This is a text analysis utility library written in Python. Your task is to port this code to JavaScript/TypeScript.

## Files

- `text_analyzer.py` - Main module with text analysis functions
- `test_text_analyzer.py` - Comprehensive test suite

## Running Tests

```bash
pip install -r requirements.txt
pytest test_text_analyzer.py -v
```

## Module Overview

The `text_analyzer` module provides:

1. **TextAnalyzer class**: Object-oriented interface for analyzing text
   - Word counting and frequency analysis
   - Unique word extraction
   - Average word length calculation
   - Finding longest words

2. **Utility functions**:
   - `tokenize()`: Split text into words
   - `char_frequency_analysis()`: Analyze character frequencies
   - `find_palindromes()`: Detect palindrome words
   - `group_by_length()`: Group words by length
   - `calculate_reading_metrics()`: Compute reading statistics
   - `extract_acronyms()`: Find all-caps acronyms
   - `title_case_special()`: Smart title case conversion
   - `remove_duplicate_words()`: Remove duplicate words from text

## Python-Specific Features Used

This code uses several Python idioms that will need to be adapted for JavaScript:

- List comprehensions
- Dictionary comprehensions
- `defaultdict` and `Counter` from collections
- Type hints
- Set operations
- Keyword arguments with defaults
- Optional parameters
- String slicing and reversal (`[::-1]`)
- Multiple return values (tuples)

Your port should use equivalent idiomatic JavaScript/TypeScript patterns.
