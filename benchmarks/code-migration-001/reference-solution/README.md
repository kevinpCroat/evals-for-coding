# Reference Solution - SQLAlchemy 2.0 Migration

This directory contains a reference implementation of the SQLAlchemy 1.4 to 2.0 migration.

## Changes Made

### 1. requirements.txt
- Updated SQLAlchemy from 1.4.48 to 2.0.25

### 2. models.py
- Changed import: `from sqlalchemy.ext.declarative import declarative_base` → `from sqlalchemy.orm import declarative_base`
- Updated `sessionmaker(bind=engine)` → `sessionmaker(engine)`
- All other model definitions remain the same (Column definitions are still supported in 2.0)

### 3. database.py
- Added import: `from sqlalchemy import select`
- Replaced all `session.query()` calls with `session.scalars(select())`
- Pattern transformations:
  - `session.query(Model).all()` → `session.scalars(select(Model)).all()`
  - `session.query(Model).filter(condition).first()` → `session.scalars(select(Model).where(condition)).first()`
  - `session.query(Model).filter_by(attr=value)` → `session.scalars(select(Model).where(Model.attr == value))`

### 4. test_database.py
- No changes - tests pass as-is

## Key Migration Patterns

### Query All Records
**Before:**
```python
users = session.query(User).all()
```

**After:**
```python
users = session.scalars(select(User)).all()
```

### Query with Filter
**Before:**
```python
user = session.query(User).filter(User.id == user_id).first()
```

**After:**
```python
user = session.scalars(select(User).where(User.id == user_id)).first()
```

### Query with Complex Conditions
**Before:**
```python
results = session.query(User).filter(
    (User.username.like('%term%')) | (User.email.like('%term%'))
).all()
```

**After:**
```python
results = session.scalars(
    select(User).where(
        (User.username.like('%term%')) | (User.email.like('%term%'))
    )
).all()
```

### Query with Join
**Before:**
```python
posts = session.query(Post).join(User).all()
```

**After:**
```python
posts = session.scalars(select(Post).join(User)).all()
```

## Verification

All 16 tests pass with SQLAlchemy 2.0.25 and no deprecation warnings:

```bash
pytest test_database.py -v -W default::DeprecationWarning
```

Result: 16 passed, no warnings

## Score

This reference solution achieves:
- Tests: 100/100 (all tests pass)
- Deprecation Warnings: 100/100 (no warnings)
- Build: 100/100 (SQLAlchemy 2.0.25 installed)
- **Final Score: 100/100**
