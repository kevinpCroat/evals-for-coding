# Data Modelling - Specification

## Objective

Design and implement a complete database schema for a blog platform using SQLAlchemy ORM with proper relationships, constraints, and migrations.

## Background

Database schema design is a critical skill for backend developers. This benchmark tests your ability to translate business requirements into a well-structured relational database schema that is normalized, performant, and maintainable.

You will design a schema for a multi-author blog platform with users, articles, categories, tags, and comments. The schema must properly model relationships, enforce data integrity, and support efficient queries.

## Requirements

### Functional Requirements

1. **Create SQLAlchemy Models** - Define all 7 entities as SQLAlchemy ORM models
   - User (authors and commenters)
   - Article (blog posts)
   - Category (hierarchical organization)
   - Tag (cross-cutting labels)
   - Comment (threaded discussions)
   - ArticleTag (many-to-many junction)
   - UserFollow (many-to-many junction)

2. **Define Relationships** - Implement all relationships with proper foreign keys
   - One-to-many: User→Article, Category→Article, User→Comment, Article→Comment, Comment→Comment, Category→Category
   - Many-to-many: Article↔Tag (via ArticleTag), User↔User (via UserFollow)
   - Use SQLAlchemy relationship() with appropriate back_populates/backref

3. **Enforce Constraints** - Add all necessary constraints
   - Unique constraints (email, username, slugs, tag names)
   - Not null constraints (required fields)
   - Foreign key constraints (with proper ondelete behavior)
   - Check constraints (prevent self-follows, validate enums)

4. **Add Indexes** - Create indexes for common query patterns
   - Unique indexes for lookups (email, username, slugs)
   - Foreign key indexes for joins
   - Composite indexes for common filter combinations
   - See requirements.md for high-priority queries to optimize

5. **Create Migration Script** - Write an Alembic migration to create all tables
   - Initial migration that creates the complete schema
   - Use proper Alembic conventions
   - Include all indexes and constraints

### Technical Constraints

- Use **SQLAlchemy 2.0+** declarative syntax
- Use **Alembic** for migrations
- Use **PostgreSQL** as target database (but SQLite for testing)
- Follow SQLAlchemy best practices for relationships and lazy loading
- Use timezone-aware datetime fields (UTC)
- Use Integer primary keys (not UUIDs)
- Use Enum types for status fields where appropriate

### Quality Requirements

- All verification tests must pass
- Schema must create successfully without errors
- Relationships must be bidirectional and queryable
- Constraints must be enforced at database level
- Migrations must run without errors
- Code must follow PEP 8 style guidelines

## Success Criteria

The implementation will be considered successful when:

1. **Schema Validity (30%)** - All models create tables successfully without errors
2. **Relationships Work (25%)** - Can query across all relationships in both directions
3. **Constraints Enforced (20%)** - Database rejects invalid data (duplicates, nulls, bad FKs)
4. **Migration Success (15%)** - Alembic migration runs and creates all tables
5. **Query Performance (10%)** - Required indexes exist for high-priority queries

## Deliverables

You must create the following files in the benchmark directory:

1. **models.py** - All SQLAlchemy model definitions
   - Import necessary SQLAlchemy components
   - Define declarative base
   - Create all 7 model classes with fields, relationships, and constraints
   - Add __repr__ methods for debugging

2. **alembic.ini** - Alembic configuration file
   - Standard Alembic configuration
   - Configure for SQLite (for testing)

3. **alembic/** - Alembic directory structure
   - env.py - Environment configuration
   - script.py.mako - Migration template
   - versions/001_initial_schema.py - Initial migration script

4. **requirements.txt** - Python dependencies
   - SQLAlchemy>=2.0
   - Alembic>=1.12
   - psycopg2-binary (for PostgreSQL)

## File Structure

```
data-modelling-001/
├── requirements.md          # Business requirements (provided)
├── spec.md                  # This file
├── prompts.txt              # Task prompt for AI
├── models.py                # Your SQLAlchemy models (CREATE THIS)
├── alembic.ini              # Alembic config (CREATE THIS)
├── alembic/                 # Alembic directory (CREATE THIS)
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial_schema.py
├── requirements.txt         # Dependencies (CREATE THIS)
└── verification/
    ├── tests/               # Test files
    └── verify.sh            # Scoring script
```

## Evaluation

Your submission will be scored on:

- **Schema Validity**: 30% - Models create tables without errors, proper field types
- **Relationships**: 25% - All relationships work bidirectionally, can join and query
- **Constraints**: 20% - Unique, not null, FK, and check constraints enforced
- **Migrations**: 15% - Alembic migration runs successfully and creates schema
- **Performance**: 10% - Required indexes present for high-priority queries

See verification/verify.sh for automated scoring implementation.

## Notes

- Read requirements.md carefully for all business rules and constraints
- Pay attention to cascading delete behavior
- Consider query patterns when adding indexes
- Test your schema locally before submission
- Use proper SQLAlchemy type hints for better IDE support
