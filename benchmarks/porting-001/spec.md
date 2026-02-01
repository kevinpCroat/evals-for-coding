# Code Porting Challenge - Specification

## Objective

Port a Python text analysis library to JavaScript/TypeScript while preserving exact behavior and using idiomatic target language patterns.

## Background

The `starter-code/` directory contains a Python module (`text_analyzer.py`) with approximately 180 lines of text processing functionality. The module includes both a class-based interface and standalone utility functions, using common Python idioms like list comprehensions, defaultdict, Counter, and type hints.

Your task is to create a functionally equivalent JavaScript or TypeScript implementation that passes all the same tests when translated to the target language.

## Requirements

### Functional Requirements

1. **Port the TextAnalyzer class** with all its methods:
   - `word_count()`: Count total words
   - `unique_words()`: Extract unique words as a Set
   - `word_frequency()`: Return word frequency map
   - `most_common_words(n)`: Get top n most frequent words
   - `average_word_length()`: Calculate average word length
   - `longest_words(n)`: Get n longest words

2. **Port all utility functions**:
   - `tokenize(text, lowercase)`: Tokenize text into words
   - `charFrequencyAnalysis(text, ignoreCase)`: Analyze character frequencies
   - `findPalindromes(words, minLength)`: Find palindrome words
   - `groupByLength(words)`: Group words by their length
   - `calculateReadingMetrics(text)`: Compute reading statistics
   - `extractAcronyms(text)`: Extract all-caps acronyms
   - `titleCaseSpecial(text, minorWords)`: Smart title case conversion
   - `removeDuplicateWords(text, preserveOrder)`: Remove duplicates

3. **Translate the test suite** to Jest (or another JavaScript testing framework):
   - All 50+ test cases must be ported
   - Tests must verify identical behavior
   - All tests must pass

### Technical Constraints

- Use **JavaScript (ES6+)** or **TypeScript** (TypeScript preferred for type safety)
- Use **Jest** for testing (or another modern JS testing framework)
- Must work in Node.js environment (v16+)
- No external text processing libraries - implement core logic yourself
- Handle edge cases identically to Python version (empty strings, null/undefined, etc.)

### Quality Requirements

- All ported tests must pass (50+ test cases)
- Code must follow JavaScript/TypeScript conventions:
  - camelCase for functions and variables (not snake_case)
  - Proper use of const/let (no var)
  - Use modern ES6+ features (arrow functions, destructuring, spread operator, etc.)
  - Use idiomatic JS patterns for Python constructs:
    - List comprehensions → map/filter/reduce
    - defaultdict → Map with default handling or object with logic
    - Counter → Map or object with counting logic
    - Set operations → JavaScript Set
- ESLint must pass with standard configuration
- Include proper JSDoc or TypeScript type definitions

## Success Criteria

The implementation will be considered successful when:

1. **All tests pass** - The ported test suite runs successfully with 0 failures
2. **Idiomatic code** - Uses JavaScript/TypeScript best practices, not Python patterns directly translated
3. **Feature parity** - All functions and methods from Python version are implemented
4. **Build success** - Code runs without errors in Node.js environment

## Deliverables

Create the following files in the submission directory:

1. **textAnalyzer.js** or **textAnalyzer.ts** - Main implementation
2. **textAnalyzer.test.js** or **textAnalyzer.test.ts** - Ported test suite
3. **package.json** - NPM configuration with dependencies
4. **README.md** - Brief documentation explaining how to run tests

Optional but recommended:
- **.eslintrc.js** or **.eslintrc.json** - Linting configuration
- **tsconfig.json** - TypeScript configuration (if using TS)

## Evaluation

Your submission will be scored on:

- **Tests Pass** (50%): All ported tests execute and pass
  - 50 points: All tests pass
  - Proportional: Partial credit for passing subset of tests

- **Idiomatic Code** (20%): Uses JavaScript/TypeScript conventions
  - ESLint passes with no errors
  - Uses camelCase naming
  - Uses appropriate JS data structures (Map, Set, Array methods)
  - No direct Python-style patterns (e.g., manually incrementing counters instead of reduce)

- **Feature Parity** (20%): All functions implemented correctly
  - All class methods present and working
  - All utility functions present and working
  - Handles edge cases properly

- **Build Success** (10%): Code executes without errors
  - npm install succeeds
  - npm test runs successfully
  - No syntax errors or runtime crashes

See `verification/verify.sh` for automated scoring implementation.
