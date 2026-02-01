# Data Modelling - Blog Platform Database Schema

## Overview

This benchmark tests an AI's ability to design a complete database schema from business requirements using SQLAlchemy ORM. The AI must translate domain requirements into a well-structured relational database with proper relationships, constraints, indexes, and migrations.

## Challenge

Design and implement a database schema for a multi-author blog platform with the following features:
- User management (authors, commenters, followers)
- Content management (articles with categories and tags)
- Engagement features (comments with threading)
- Hierarchical categories
- Many-to-many relationships (tags, user follows)

## What This Tests

### Core Skills
- **Database Design**: Translating business requirements into normalized schema
- **ORM Usage**: Proper use of SQLAlchemy declarative syntax and relationships
- **Data Integrity**: Implementing constraints (unique, not null, foreign keys, checks)
- **Query Optimization**: Adding indexes for common query patterns
- **Migrations**: Creating Alembic migration scripts

### Key Concepts
- One-to-many relationships (User→Article, Category→Article, Article→Comment)
- Many-to-many relationships (Article↔Tag, User↔User follows)
- Self-referential relationships (Category→Category hierarchy, Comment→Comment threading)
- Cascade delete behaviors
- Composite unique constraints
- Database indexes for performance

## Difficulty: Medium

This benchmark requires:
- Understanding of relational database concepts
- Familiarity with SQLAlchemy ORM
- Knowledge of database constraints and indexes
- Experience with Alembic migrations
- Ability to read and translate business requirements

Expected time: 60-90 minutes

## Scoring Breakdown

The implementation is scored on 5 components (100 points total):

1. **Schema Validity (30%)** - All models create tables successfully
   - All 7 models defined (User, Article, Category, Tag, Comment, ArticleTag, UserFollow)
   - Proper field types and columns
   - Tables create without errors

2. **Relationships (25%)** - All relationships work bidirectionally
   - One-to-many: User→Article, Category→Article, User→Comment, Article→Comment
   - Self-referential: Category→Category, Comment→Comment
   - Many-to-many: Article↔Tag, User↔User (follows)
   - Proper back_populates/backref configuration

3. **Constraints (20%)** - Database enforces data integrity
   - Unique constraints (email, username, slugs, tag names)
   - Not null constraints on required fields
   - Foreign key constraints with proper ondelete
   - Composite unique constraints on junction tables
   - Cascade delete behaviors

4. **Migrations (15%)** - Alembic migration runs successfully
   - Alembic configuration files present
   - Initial migration script creates all tables
   - Migration runs without errors
   - Proper upgrade/downgrade functions

5. **Query Performance (10%)** - Required indexes present
   - Unique indexes for lookups (email, username, slugs)
   - Foreign key indexes for joins
   - Composite indexes where appropriate
   - See requirements.md for query patterns

**Passing Score**: 70/100

## Files Structure

```
data-modelling-001/
├── requirements.md          # Business requirements (READ THIS FIRST)
├── spec.md                  # Technical specification
├── prompts.txt              # Task prompt for AI
├── README.md                # This file
├── models.py                # YOUR IMPLEMENTATION - SQLAlchemy models
├── alembic.ini              # YOUR IMPLEMENTATION - Alembic config
├── alembic/                 # YOUR IMPLEMENTATION - Migration files
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial_schema.py
├── requirements.txt         # YOUR IMPLEMENTATION - Dependencies
└── verification/
    ├── tests/               # Automated tests
    │   ├── test_schema.py
    │   ├── test_relationships.py
    │   ├── test_constraints.py
    │   ├── test_migrations.py
    │   └── test_indexes.py
    └── verify.sh            # Scoring script
```

## How to Solve

1. **Read Requirements** (`requirements.md`)
   - Understand the domain (blog platform)
   - Identify all 7 entities and their attributes
   - Note relationships and their cardinality
   - Pay attention to business rules and constraints
   - Review query requirements for indexing

2. **Read Specification** (`spec.md`)
   - Understand deliverables
   - Note technical constraints (SQLAlchemy 2.0+, Alembic)
   - Review success criteria

3. **Design Schema** (`models.py`)
   - Create all 7 model classes
   - Add proper field types with constraints
   - Define all relationships with back_populates
   - Add indexes for common queries
   - Configure cascade delete behaviors
   - Add __repr__ methods for debugging

4. **Setup Alembic**
   - Create `alembic.ini` configuration
   - Initialize alembic directory structure
   - Configure `env.py` to import models
   - Create initial migration script

5. **Test Locally**
   - Create test database
   - Run migration
   - Test creating and querying models
   - Verify constraints work

6. **Verify**
   ```bash
   ./verification/verify.sh
   ```

## Common Pitfalls

1. **Missing Relationships**: Forgetting to add back_populates/backref
2. **No Constraints**: Not adding unique, not null, or foreign key constraints
3. **Missing Indexes**: Forgetting indexes for common query patterns
4. **Wrong Cascade**: Incorrect ondelete behavior (should cascade for article→comments)
5. **Self-References**: Incorrectly implementing Category→Category or Comment→Comment
6. **No Migration**: Forgetting to create Alembic migration script
7. **Junction Tables**: Missing composite unique constraints on many-to-many tables

## Example Success

A successful implementation will:
- Define all 7 models with correct field types
- Implement all relationships bidirectionally
- Enforce all constraints from requirements
- Have indexes on email, username, slugs, and foreign keys
- Include working Alembic migration that creates schema
- Pass all verification tests with score ≥70

## Verification

Run the verification script to get your score:

```bash
cd /Users/kperko/code/evals-for-coding/benchmarks/data-modelling-001
./verification/verify.sh
```

The script will:
1. Test schema validity (can tables be created?)
2. Test relationships (do joins work both ways?)
3. Test constraints (are violations caught?)
4. Test migrations (does Alembic work?)
5. Test indexes (are required indexes present?)

Output is JSON with detailed scoring and feedback.

## Domain Reference

### Blog Platform Entities

**User**: Authors and commenters with profiles and follow relationships

**Article**: Blog posts with title, content, status (draft/published/archived)

**Category**: Hierarchical organization (e.g., Technology → Python → Django)

**Tag**: Cross-cutting labels (e.g., #tutorial, #beginner)

**Comment**: Threaded discussions on articles

**ArticleTag**: Junction for article-tag many-to-many

**UserFollow**: Junction for user-user follow relationships

### Key Relationships

- User writes many Articles (1:N)
- Article belongs to one Category (N:1)
- Category can have subcategories (1:N self-reference)
- Article has many Comments (1:N cascade delete)
- Comment can have reply Comments (1:N self-reference cascade delete)
- Article has many Tags (M:N via ArticleTag)
- User follows many Users (M:N via UserFollow)

## Tips

- Start with the simplest models (User, Category, Tag) then build up
- Define foreign keys before relationships
- Use SQLAlchemy's automatic back_populates where possible
- Test each relationship in isolation
- Pay attention to cascade delete requirements
- Don't forget timezone-aware datetime fields
- Add __repr__ methods to make debugging easier

## Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Database Normalization](https://en.wikipedia.org/wiki/Database_normalization)
- requirements.md - Complete business requirements
- spec.md - Technical specification
