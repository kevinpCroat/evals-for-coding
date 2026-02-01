# SQLAlchemy 1.4 to 2.0 Migration Guide

This guide documents the breaking changes between SQLAlchemy 1.4 and 2.0 that affect this codebase.

## Overview

SQLAlchemy 2.0 represents a major modernization of the library with several breaking changes. The primary focus is on removing legacy query patterns and introducing a more explicit, type-safe API.

## Major Breaking Changes

### 1. Declarative Base Import

**SQLAlchemy 1.4 (Deprecated):**
```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

**SQLAlchemy 2.0:**
```python
from sqlalchemy.orm import declarative_base

Base = declarative_base()
```

**Alternative (2.0 style with type annotations):**
```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

### 2. Column Definitions

**SQLAlchemy 1.4:**
```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
```

**SQLAlchemy 2.0 (Modern approach with mapped_column):**
```python
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
```

**Note:** The old `Column()` syntax still works in 2.0 but is not the recommended approach for new code.

### 3. Query API Removal

This is the most significant breaking change. The `session.query()` API is removed in SQLAlchemy 2.0.

**SQLAlchemy 1.4:**
```python
# Get all records
users = session.query(User).all()

# Filter with where clause
user = session.query(User).filter(User.id == 1).first()

# Filter with keyword arguments
user = session.query(User).filter_by(username='john').first()

# Complex queries with joins
posts = session.query(Post).join(User).all()
```

**SQLAlchemy 2.0:**
```python
from sqlalchemy import select

# Get all records
users = session.scalars(select(User)).all()

# Filter with where clause
user = session.scalars(select(User).where(User.id == 1)).first()

# Filter (no direct filter_by replacement)
user = session.scalars(select(User).where(User.username == 'john')).first()

# Complex queries with joins
posts = session.scalars(select(Post).join(User)).all()
```

### 4. Session.scalars() vs Session.execute()

- `session.scalars()` - Returns scalar values (ORM objects directly)
- `session.execute()` - Returns `Row` objects that need to be unpacked

**For most ORM queries, use `session.scalars()`:**
```python
# Returns User objects directly
users = session.scalars(select(User)).all()
```

**Use `session.execute()` for custom projections:**
```python
# Returns Row objects
results = session.execute(select(User.id, User.username)).all()
for row in results:
    print(row.id, row.username)
```

### 5. Sessionmaker

**SQLAlchemy 1.4:**
```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```

**SQLAlchemy 2.0 (still works, but consider alternatives):**
```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(engine)  # No 'bind' parameter
session = Session()
```

**Modern approach with context managers:**
```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    # use session
    session.commit()
```

### 6. Engine Creation

**SQLAlchemy 1.4:**
```python
from sqlalchemy import create_engine

engine = create_engine('sqlite:///test.db')
```

**SQLAlchemy 2.0 (same, but can add echo parameter):**
```python
from sqlalchemy import create_engine

engine = create_engine('sqlite:///test.db', echo=False)
```

### 7. Relationship Definitions

Relationships remain mostly the same, but the `back_populates` parameter is now preferred over `backref`.

**Recommended approach (works in both versions):**
```python
class User(Base):
    posts = relationship("Post", back_populates="author")

class Post(Base):
    author = relationship("User", back_populates="posts")
```

## Common Migration Patterns

### Pattern 1: Get Single Record by ID

**Before:**
```python
user = session.query(User).filter(User.id == user_id).first()
```

**After:**
```python
from sqlalchemy import select

user = session.scalars(select(User).where(User.id == user_id)).first()
```

### Pattern 2: Get All Records

**Before:**
```python
users = session.query(User).all()
```

**After:**
```python
from sqlalchemy import select

users = session.scalars(select(User)).all()
```

### Pattern 3: Filter with Multiple Conditions

**Before:**
```python
users = session.query(User).filter(
    (User.username.like('%john%')) | (User.email.like('%john%'))
).all()
```

**After:**
```python
from sqlalchemy import select

users = session.scalars(
    select(User).where(
        (User.username.like('%john%')) | (User.email.like('%john%'))
    )
).all()
```

### Pattern 4: Joins

**Before:**
```python
posts = session.query(Post).join(User).all()
```

**After:**
```python
from sqlalchemy import select

posts = session.scalars(select(Post).join(User)).all()
```

### Pattern 5: Count

**Before:**
```python
count = session.query(User).count()
```

**After:**
```python
from sqlalchemy import select, func

count = session.scalar(select(func.count()).select_from(User))
```

## Deprecation Warnings

When running tests with SQLAlchemy 1.4 code on 2.0, you may see warnings like:

```
RemovedIn20Warning: The ``declarative_base()`` function is now available as
sqlalchemy.orm.declarative_base(). (deprecated since: 2.0)
```

```
RemovedIn20Warning: The Query.get() method is considered legacy as of the
1.x series of SQLAlchemy and becomes a legacy construct in 2.0.
```

All of these warnings indicate code that needs to be updated for 2.0 compatibility.

## Testing for Deprecation Warnings

To ensure your code has no deprecation warnings:

```bash
# Show all deprecation warnings
pytest -W default::DeprecationWarning

# Treat warnings as errors
pytest -W error::DeprecationWarning
```

## Resources

- [SQLAlchemy 2.0 Migration Guide](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [What's New in SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)

## Quick Reference: API Changes

| 1.4 API | 2.0 API |
|---------|---------|
| `from sqlalchemy.ext.declarative import declarative_base` | `from sqlalchemy.orm import declarative_base` |
| `session.query(Model)` | `session.scalars(select(Model))` |
| `session.query(Model).filter()` | `session.scalars(select(Model).where())` |
| `session.query(Model).filter_by()` | `session.scalars(select(Model).where())` |
| `session.query(Model).first()` | `session.scalars(select(Model)).first()` |
| `session.query(Model).all()` | `session.scalars(select(Model)).all()` |
| `session.query(Model).get(id)` | `session.get(Model, id)` |
| `sessionmaker(bind=engine)` | `sessionmaker(engine)` or `Session(engine)` |
