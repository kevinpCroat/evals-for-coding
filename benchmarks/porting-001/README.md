# Porting-001 Benchmark

Tests AI's ability to port code between programming languages while preserving behavior and using idiomatic patterns.

## Overview

This benchmark challenges AI to port a Python text analysis library (~180 lines) to JavaScript/TypeScript, including:
- Translating both implementation and comprehensive test suite (45+ tests)
- Converting Python-specific idioms to JavaScript equivalents
- Ensuring all tests pass in the target language
- Following JavaScript/TypeScript best practices

## What's Being Tested

**Core Skill**: Code porting and language translation

**Key Challenges**:
- Understanding Python patterns (list comprehensions, defaultdict, Counter, type hints)
- Translating to idiomatic JavaScript (map/filter/reduce, Maps/Sets, etc.)
- Maintaining exact functional equivalence
- Writing clean, modern JavaScript/TypeScript
- Porting comprehensive test suite to Jest

## Benchmark Structure

```
porting-001/
├── starter-code/           # Python code to be ported
│   ├── text_analyzer.py    # ~180 line Python module
│   ├── test_text_analyzer.py  # 45 comprehensive tests
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Python implementation docs
├── reference-solution/     # Example TypeScript solution
│   ├── textAnalyzer.ts    # Idiomatic TypeScript port
│   ├── textAnalyzer.test.ts  # Jest test suite
│   ├── package.json       # NPM configuration
│   ├── tsconfig.json      # TypeScript config
│   └── .eslintrc.json     # Linting configuration
├── verification/
│   └── verify.sh          # Automated scoring script
├── spec.md                # Detailed requirements
├── prompts.txt            # Task prompt for AI
└── README.md             # This file
```

## Scoring Criteria

The benchmark scores submissions on four components:

1. **Tests Passing (50%)**: All ported tests execute and pass
   - Full credit: All 45+ tests pass
   - Proportional: Partial credit based on pass rate

2. **Idiomatic Code (20%)**: Uses JavaScript/TypeScript conventions
   - camelCase naming (not snake_case)
   - No `var` usage (const/let only)
   - Modern array methods (map/filter/reduce)
   - Arrow functions
   - ESLint passes (if config provided)

3. **Feature Parity (20%)**: All functions implemented
   - TextAnalyzer class with all methods
   - All 7+ utility functions
   - Edge case handling

4. **Build Success (10%)**: Code executes without errors
   - `npm install` succeeds
   - `npm test` runs (even if some tests fail)
   - No syntax errors

**Passing Threshold**: 70/100

## Running the Benchmark

### Test the Python starter code:
```bash
cd starter-code
pip install -r requirements.txt
pytest test_text_analyzer.py -v
```

### Verify a submission:
```bash
./verification/verify.sh submission/
```

The script outputs JSON with detailed scoring.

### Test the reference solution:
```bash
cd reference-solution
npm install
npm test
npm run lint
```

## Example Porting Challenges

The Python code uses several patterns that require thoughtful translation:

**List Comprehensions**:
```python
# Python
words = [word.lower() for word in re.findall(r'\b\w+\b', text)]

// JavaScript
const words = text.match(/\b\w+\b/g)?.map(word => word.toLowerCase()) ?? [];
```

**defaultdict**:
```python
# Python
from collections import defaultdict
grouped = defaultdict(list)
for word in words:
    grouped[len(word)].append(word)

// JavaScript
const grouped = {};
for (const word of words) {
  const len = word.length;
  if (!grouped[len]) grouped[len] = [];
  grouped[len].push(word);
}
```

**Counter**:
```python
# Python
from collections import Counter
freq = dict(Counter(words))

// JavaScript
const freq = {};
for (const word of words) {
  freq[word] = (freq[word] || 0) + 1;
}
```

**String Reversal**:
```python
# Python
reversed_word = word[::-1]

// JavaScript
const reversedWord = word.split('').reverse().join('');
```

## Success Metrics

A successful port should:
- Pass all 45+ tests with identical behavior
- Use camelCase consistently
- Leverage ES6+ features appropriately
- Have clean, readable code
- Run without errors in Node.js 16+

## Notes

- **Language Choice**: JavaScript or TypeScript (TypeScript preferred)
- **Testing Framework**: Jest recommended (but others acceptable)
- **No External Libraries**: Core logic must be implemented, not delegated to text processing libraries
- **Edge Cases**: Must handle empty strings, null/undefined, edge cases identically to Python version

## Design Rationale

This benchmark tests:
1. **Language Knowledge**: Understanding both Python and JavaScript deeply
2. **Pattern Translation**: Converting idioms between languages
3. **Testing Skills**: Porting tests to verify behavior
4. **Code Quality**: Writing clean, idiomatic code in the target language
5. **Attention to Detail**: Maintaining exact functional equivalence

The text analysis domain was chosen because it:
- Uses common Python idioms (comprehensions, collections)
- Has clear, testable behavior
- Requires thoughtful string/array manipulation
- Is complex enough to be interesting but simple enough to complete
- Doesn't require domain expertise
