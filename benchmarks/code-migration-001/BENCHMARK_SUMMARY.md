# Code Migration Benchmark - Summary

## Overview

This benchmark tests an AI's ability to migrate Python code from SQLAlchemy 1.4 to SQLAlchemy 2.0, handling breaking API changes while maintaining functionality.

## Benchmark Statistics

- **Difficulty**: Medium-High
- **Language**: Python
- **Domain**: Database ORM Migration
- **Test Files**: 16 tests across 3 test classes
- **Passing Score**: 70/100

## Challenge Metrics

### Code Volume
- 3 Python files to modify
- ~150 lines of application code
- ~200 lines of test code (read-only)
- 1 requirements file

### Breaking Changes
- 15+ instances of deprecated `session.query()` API
- 2 import changes
- 1 sessionmaker pattern change

### Complexity Factors
1. Multiple deprecated patterns to identify
2. Systematic refactoring required across multiple files
3. Must maintain exact functional equivalence (tests unchanged)
4. Need to understand both old and new API patterns

## Scoring Breakdown

| Component | Weight | Description |
|-----------|--------|-------------|
| Tests Passing | 60% | All 16 tests must pass with SQLAlchemy 2.0 |
| No Deprecation Warnings | 20% | Code runs without SQLAlchemy deprecation warnings |
| Build Success | 20% | Requirements install cleanly with SQLAlchemy 2.0+ |

### Scoring Examples

**Perfect Migration (100/100)**:
- SQLAlchemy 2.0.x installed
- All 16 tests pass
- No deprecation warnings
- Final: (100 * 0.6) + (100 * 0.2) + (100 * 0.2) = 100

**Partial Migration (80/100)**:
- SQLAlchemy 2.0.x installed (100)
- All 16 tests pass (100)
- Some non-SQLAlchemy warnings (80)
- Final: (100 * 0.6) + (80 * 0.2) + (100 * 0.2) = 96

**Incomplete Migration (30/100)**:
- SQLAlchemy 2.0.x installed (100)
- 8 of 16 tests pass (50)
- SQLAlchemy warnings present (0)
- Final: (50 * 0.6) + (0 * 0.2) + (100 * 0.2) = 50 (FAIL)

**No Migration (0/100)**:
- Still using SQLAlchemy 1.4.x (0)
- Tests skipped due to wrong version (0)
- Warnings check skipped (0)
- Final: 0 (FAIL)

## Expected AI Approach

A successful AI agent should:

1. **Read Documentation** (2-3 minutes)
   - Review spec.md for requirements
   - Read MIGRATION_GUIDE.md for breaking changes
   - Understand the deprecated → new pattern mappings

2. **Plan Migration** (1-2 minutes)
   - Identify files to modify
   - Map out pattern replacements needed
   - Determine testing strategy

3. **Execute Migration** (5-10 minutes)
   - Update requirements.txt to SQLAlchemy 2.0.x
   - Fix imports in models.py
   - Systematically replace session.query() in database.py
   - Update sessionmaker pattern

4. **Verify Solution** (2-3 minutes)
   - Run tests to check functionality
   - Check for deprecation warnings
   - Fix any issues found

**Estimated Total Time**: 10-18 minutes for a competent AI agent

## Common Pitfalls

1. **Incomplete Pattern Replacement**: Missing some `session.query()` calls
2. **Wrong API Usage**: Using `execute()` instead of `scalars()` for ORM queries
3. **Import Errors**: Not updating the declarative_base import
4. **Test Modifications**: Accidentally modifying test_database.py (not allowed)
5. **Version Mismatch**: Updating to SQLAlchemy 1.4.x instead of 2.0.x

## Success Indicators

- Clean install of SQLAlchemy 2.0+
- 16/16 tests passing
- Zero deprecation warnings
- Code uses modern `select()` patterns throughout

## Files Provided

### Core Files
- `spec.md` - Task specification
- `prompts.txt` - Standard AI prompts
- `README.md` - Benchmark overview
- `MIGRATION_GUIDE.md` - SQLAlchemy 2.0 migration reference

### Starter Code
- `starter-code/models.py` - Database models (deprecated patterns)
- `starter-code/database.py` - Repository classes (deprecated query API)
- `starter-code/test_database.py` - Test suite (DO NOT MODIFY)
- `starter-code/requirements.txt` - SQLAlchemy 1.4.48

### Verification
- `verification/verify.sh` - Automated scoring script (outputs JSON)

### Reference Solution
- `reference-solution/` - Working solution for validation
- Achieves 100/100 score
- Demonstrates all required changes

## Validation Results

### Starter Code (SQLAlchemy 1.4)
- ✅ All 16 tests pass
- ⚠️  Contains deprecation warnings
- ✅ Demonstrates realistic legacy codebase

### Reference Solution (SQLAlchemy 2.0)
- ✅ All 16 tests pass
- ✅ No deprecation warnings
- ✅ Achieves 100/100 score
- ✅ Uses modern SQLAlchemy 2.0 patterns

## Learning Objectives

This benchmark evaluates:

1. **Documentation Reading**: Can the AI find and use migration guides?
2. **Pattern Recognition**: Can it identify deprecated API patterns?
3. **Systematic Refactoring**: Can it apply changes consistently across files?
4. **API Understanding**: Does it understand the semantic differences between old/new APIs?
5. **Testing**: Can it validate changes and iterate on failures?
6. **Attention to Detail**: Does it catch all instances of deprecated patterns?

## Real-World Relevance

This benchmark simulates a common software engineering task:
- Upgrading dependencies when old versions reach end-of-life
- Handling breaking changes in major version updates
- Maintaining functionality during migrations
- Working with comprehensive test suites as safety nets

These skills are critical for:
- Keeping codebases modern and secure
- Reducing technical debt
- Managing dependency upgrades in production systems
- Understanding deprecation cycles in software ecosystems
