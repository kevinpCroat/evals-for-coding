# Code Migration Benchmark: SQLAlchemy 1.4 to 2.0

This benchmark tests an AI's ability to migrate code from deprecated APIs to new major versions of dependencies with breaking changes.

## Overview

The task requires migrating a Python codebase from SQLAlchemy 1.4 to SQLAlchemy 2.0, handling all breaking API changes while maintaining functionality and ensuring all tests continue to pass.

## Challenge Description

The starter code contains a simple blog application with Users and Posts, implemented using SQLAlchemy 1.4 patterns that are deprecated and removed in SQLAlchemy 2.0. The AI must:

1. Update dependencies to SQLAlchemy 2.0.x
2. Migrate all deprecated `session.query()` patterns to `select()`
3. Update imports and model definitions
4. Ensure all tests pass without modification
5. Remove all deprecation warnings

## Key Breaking Changes

SQLAlchemy 2.0 removes several legacy APIs:

- **Query API**: `session.query(Model)` → `session.scalars(select(Model))`
- **Imports**: `sqlalchemy.ext.declarative.declarative_base` → `sqlalchemy.orm.declarative_base`
- **Filter methods**: `filter_by()` removed in favor of `where()`
- **Session patterns**: Modernized session creation patterns

## Files

- **starter-code/**: Initial codebase with SQLAlchemy 1.4
  - `models.py`: Database models using deprecated patterns
  - `database.py`: Repository classes with deprecated query API
  - `test_database.py`: Comprehensive test suite (must pass as-is)
  - `requirements.txt`: Dependencies with old SQLAlchemy version
- **spec.md**: Detailed task specification
- **prompts.txt**: Standard prompts for the AI
- **MIGRATION_GUIDE.md**: Reference documentation on SQLAlchemy 2.0 changes
- **verification/verify.sh**: Automated scoring script

## Scoring Components

The verification script scores submissions on three components:

1. **Tests Passing (60% weight)**: All existing tests must pass with SQLAlchemy 2.0
2. **No Deprecation Warnings (20% weight)**: Code should run cleanly without SQLAlchemy deprecation warnings
3. **Build Success (20% weight)**: Requirements install cleanly with SQLAlchemy 2.0+

**Passing threshold**: 70/100

## Running the Benchmark

### Manual Testing

```bash
cd starter-code

# Install dependencies (after migration)
pip install -r requirements.txt

# Run tests
pytest test_database.py -v

# Check for deprecation warnings
pytest test_database.py -v -W default::DeprecationWarning
```

### Automated Verification

```bash
./verification/verify.sh
```

This will output JSON with detailed scoring:

```json
{
  "benchmark": "code-migration-001",
  "timestamp": "2026-01-31T12:00:00Z",
  "components": {
    "tests": {
      "score": 100,
      "weight": 0.60,
      "details": "All 15 tests passed"
    },
    "deprecation_warnings": {
      "score": 100,
      "weight": 0.20,
      "details": "No deprecation warnings detected"
    },
    "build": {
      "score": 100,
      "weight": 0.20,
      "details": "Installation successful. SQLAlchemy version: 2.0.25"
    }
  },
  "base_score": 100.00,
  "final_score": 100,
  "passed": true
}
```

## What Makes This Challenging

1. **Breaking Changes**: Multiple deprecated APIs that must be identified and replaced
2. **Pattern Differences**: Fundamentally different query patterns between versions
3. **Test Compatibility**: Tests must pass without modification, requiring exact functional equivalence
4. **Modern Practices**: Must adopt SQLAlchemy 2.0 best practices, not just minimal changes
5. **Import Changes**: Even basic imports have changed locations

## Expected Solution Approach

A successful AI agent should:

1. Read the MIGRATION_GUIDE.md to understand breaking changes
2. Update requirements.txt to SQLAlchemy 2.0.x
3. Update models.py imports and potentially use modern `mapped_column()` syntax
4. Systematically replace all `session.query()` calls in database.py with `select()` patterns
5. Test iteratively to ensure all tests pass
6. Verify no deprecation warnings remain

## Success Criteria

- SQLAlchemy 2.0+ successfully installed
- All 15 tests pass without modification
- No SQLAlchemy deprecation warnings
- Code follows SQLAlchemy 2.0 recommended patterns

## Learning Objectives

This benchmark tests:

- Reading and understanding migration documentation
- Systematic code refactoring across multiple files
- Maintaining backward compatibility at the API level
- Handling breaking changes in dependencies
- Testing and validation during migration
