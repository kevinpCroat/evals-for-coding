# Code Migration Challenge: SQLAlchemy 1.4 to 2.0

## Objective

Migrate the existing codebase from SQLAlchemy 1.4 to SQLAlchemy 2.0. This involves updating deprecated APIs, adopting new patterns, and ensuring all tests continue to pass.

## Task Description

The starter code contains a simple blog application with Users and Posts, implemented using SQLAlchemy 1.4 patterns that are deprecated in SQLAlchemy 2.0. Your task is to:

1. **Update dependencies**: Upgrade SQLAlchemy from 1.4.48 to 2.0.x in requirements.txt
2. **Migrate deprecated APIs**: Replace all deprecated patterns with SQLAlchemy 2.0 equivalents
3. **Ensure test compatibility**: All existing tests must pass without modification
4. **Remove deprecation warnings**: Code should run cleanly without any deprecation warnings

## Breaking Changes to Address

The code currently uses several deprecated SQLAlchemy 1.4 patterns that must be updated:

### 1. Declarative Base (models.py)
- **OLD**: `from sqlalchemy.ext.declarative import declarative_base`
- **NEW**: Use `DeclarativeBase` class or `declarative_base()` from `sqlalchemy.orm`

### 2. Column Definitions (models.py)
- **OLD**: `Column(Integer, primary_key=True)`
- **NEW**: Use `mapped_column()` with `Mapped[type]` annotations (preferred in 2.0)
- Alternatively, continue using `Column()` but follow 2.0 patterns

### 3. Query API (database.py)
- **OLD**: `session.query(User).filter(User.id == user_id).first()`
- **NEW**: Use `select()` with `session.execute()` or `session.scalars()`
- **OLD**: `session.query(User).all()`
- **NEW**: `session.scalars(select(User)).all()`

### 4. Filter Methods
- **OLD**: `session.query(User).filter_by(username=username)`
- **NEW**: `session.scalars(select(User).where(User.username == username))`

### 5. Session Creation (models.py)
- **OLD**: `sessionmaker(bind=engine)`
- **NEW**: While still supported, consider using context managers or the new session patterns

### 6. Engine Configuration
- Ensure proper SQLAlchemy 2.0 style configuration
- Add `future=True` flag if maintaining 1.4 compatibility, or remove it for 2.0+

## Requirements

1. **All tests must pass**: The existing test suite (test_database.py) must pass without any modifications to the tests themselves
2. **No deprecation warnings**: Running the tests should produce no SQLAlchemy deprecation warnings
3. **Clean installation**: `pip install -r requirements.txt` should complete without conflicts
4. **Maintain functionality**: All existing features must work identically from the user's perspective
5. **Modern patterns**: Use SQLAlchemy 2.0 recommended patterns (not just minimum compatibility)

## Files to Modify

- `requirements.txt` - Update SQLAlchemy version
- `models.py` - Update model definitions and session creation
- `database.py` - Migrate all query patterns to use `select()`

## Files NOT to Modify

- `test_database.py` - Tests should pass as-is after migration

## Success Criteria

1. All tests pass with SQLAlchemy 2.0.x
2. No deprecation warnings when running tests
3. Code follows SQLAlchemy 2.0 best practices
4. Clean pip install with no dependency conflicts

## Testing

Run the test suite with:
```bash
pytest test_database.py -v
```

Check for deprecation warnings:
```bash
pytest test_database.py -v -W default::DeprecationWarning
```

## Reference

Consult the MIGRATION_GUIDE.md for detailed information about SQLAlchemy 2.0 changes and migration patterns.
