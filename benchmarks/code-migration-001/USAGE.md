# Using the Code Migration Benchmark

## Quick Start

### For AI Agents

1. Read the task specification:
   ```bash
   cat prompts.txt
   cat spec.md
   ```

2. Review the migration guide:
   ```bash
   cat MIGRATION_GUIDE.md
   ```

3. Examine the starter code:
   ```bash
   cd starter-code
   ls -la
   cat requirements.txt
   ```

4. Perform the migration:
   - Update `requirements.txt` to SQLAlchemy 2.0.x
   - Update `models.py` imports and patterns
   - Update `database.py` query patterns
   - DO NOT modify `test_database.py`

5. Test your solution:
   ```bash
   cd starter-code
   pip install -r requirements.txt
   pytest test_database.py -v
   ```

6. Run verification:
   ```bash
   cd ..
   ./verification/verify.sh
   ```

### For Benchmark Evaluators

1. Set up a clean environment for each test run
2. Provide the AI with access to:
   - `prompts.txt` - initial instructions
   - `spec.md` - detailed requirements
   - `MIGRATION_GUIDE.md` - reference documentation
   - `starter-code/` - code to migrate

3. Allow the AI to modify only:
   - `starter-code/requirements.txt`
   - `starter-code/models.py`
   - `starter-code/database.py`

4. After the AI completes, run:
   ```bash
   ./verification/verify.sh
   ```

5. Capture the JSON output for scoring

## Scoring Interpretation

### Score Ranges

- **100**: Perfect migration - all tests pass, no warnings
- **80-99**: Good migration - tests pass, minor warnings
- **70-79**: Acceptable migration - tests pass, some issues (PASSING)
- **50-69**: Incomplete migration - some tests fail (FAILING)
- **0-49**: Failed migration - most tests fail or wrong version (FAILING)

### Component Analysis

**Tests (60% weight)**:
- 100 = All 16 tests pass
- 50 = 8 tests pass
- 0 = No tests pass

**Deprecation Warnings (20% weight)**:
- 100 = No warnings
- 80 = Non-SQLAlchemy warnings only
- 0 = SQLAlchemy deprecation warnings present

**Build (20% weight)**:
- 100 = SQLAlchemy 2.0+ installed
- 0 = Wrong version or install failed

## Example AI Workflow

### Successful Approach

1. **Read and understand** (2 min)
   - Review spec.md
   - Read MIGRATION_GUIDE.md
   - Note key changes needed

2. **Update dependencies** (1 min)
   - Change `requirements.txt`: `SQLAlchemy==2.0.25`

3. **Fix imports** (1 min)
   - Update `models.py`: `from sqlalchemy.orm import declarative_base`
   - Update `models.py`: `sessionmaker(engine)` instead of `sessionmaker(bind=engine)`

4. **Migrate queries** (5 min)
   - Add to `database.py`: `from sqlalchemy import select`
   - Replace all `session.query(Model)` with `session.scalars(select(Model))`
   - Replace all `.filter()` with `.where()`
   - Replace all `.filter_by()` with `.where()` with explicit comparisons

5. **Test and iterate** (3 min)
   - Run tests: `pytest test_database.py -v`
   - Fix any failures
   - Check for warnings: `pytest -W default::DeprecationWarning`

6. **Verify** (1 min)
   - Run `./verification/verify.sh`
   - Confirm 100/100 score

**Total Time**: ~13 minutes

### Common Mistakes

1. **Forgetting imports**
   ```python
   # Missing: from sqlalchemy import select
   # Results in: NameError: name 'select' is not defined
   ```

2. **Using execute() instead of scalars()**
   ```python
   # Wrong: session.execute(select(User)).all()
   # Right: session.scalars(select(User)).all()
   ```

3. **Not updating all query instances**
   ```python
   # Missed one: session.query(Post).filter(...)
   # Should be: session.scalars(select(Post).where(...))
   ```

4. **Modifying tests**
   ```python
   # NEVER modify test_database.py
   # Tests must pass as-is
   ```

## Manual Testing

### Test with SQLAlchemy 1.4 (should fail verification)

```bash
cd starter-code
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
# Should show: 1.4.48
pytest test_database.py -v
# Should pass but with deprecation warning
deactivate
rm -rf venv
```

### Test with SQLAlchemy 2.0 (should pass verification)

```bash
cd starter-code
# First migrate the code as instructed
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
# Should show: 2.0.x
pytest test_database.py -v -W default::DeprecationWarning
# Should pass with no warnings
deactivate
rm -rf venv
```

## Troubleshooting

### "No module named 'sqlalchemy'"
- Install dependencies: `pip install -r requirements.txt`

### "RemovedIn20Warning" or "MovedIn20Warning"
- Still using deprecated APIs - check MIGRATION_GUIDE.md
- Common: forgot to update imports or query patterns

### Tests failing after migration
- Likely incorrect query pattern - compare with MIGRATION_GUIDE.md examples
- Check you're using `scalars()` not `execute()` for ORM queries
- Verify `where()` conditions match original `filter()` logic

### Verification script fails
- Ensure you're in the benchmark root directory
- Check that starter-code/ contains the modified files
- Verify requirements.txt has SQLAlchemy 2.0.x

## Reference Solution

A complete working solution is available in `reference-solution/` for:
- Validating the benchmark works correctly
- Understanding the expected changes
- Debugging scoring issues

**Note**: AI agents should NOT be given access to the reference solution during testing.

## Integration with Evaluation Frameworks

### JSON Output Format

The verification script outputs standardized JSON:

```json
{
  "benchmark": "code-migration-001",
  "timestamp": "2026-01-31T12:00:00Z",
  "components": {
    "tests": {"score": 100, "weight": 0.60, "details": "..."},
    "deprecation_warnings": {"score": 100, "weight": 0.20, "details": "..."},
    "build": {"score": 100, "weight": 0.20, "details": "..."}
  },
  "base_score": 100.00,
  "final_score": 100,
  "passed": true
}
```

### Exit Codes

- `0`: Passed (score >= 70)
- `1`: Failed (score < 70)

### Automation

```bash
# Run benchmark and capture results
RESULT=$(./verification/verify.sh)
EXIT_CODE=$?

# Parse JSON
SCORE=$(echo "$RESULT" | jq '.final_score')
PASSED=$(echo "$RESULT" | jq '.passed')

echo "Score: $SCORE/100"
echo "Passed: $PASSED"
exit $EXIT_CODE
```

## Support

For issues or questions about this benchmark:
1. Check MIGRATION_GUIDE.md for SQLAlchemy migration details
2. Review BENCHMARK_SUMMARY.md for scoring explanation
3. Examine reference-solution/ for working example
