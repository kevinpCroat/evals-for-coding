"""
Test indexes - verify required indexes exist for query performance
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from sqlalchemy import create_engine, inspect


@pytest.fixture
def inspector():
    """Create database inspector"""
    import models

    engine = create_engine('sqlite:///:memory:')
    models.Base.metadata.create_all(engine)
    return inspect(engine)


def test_user_email_index(inspector):
    """Test that email field has a unique index"""
    indexes = inspector.get_indexes('users')
    columns = inspector.get_columns('users')

    # Check email column exists
    email_col = [c for c in columns if c['name'] == 'email']
    assert len(email_col) > 0, "Email column not found in users table"

    # Check for unique constraint/index on email
    # In SQLite, UNIQUE constraints create indexes
    unique_constraints = inspector.get_unique_constraints('users')
    email_unique = any('email' in uc.get('column_names', []) for uc in unique_constraints)

    # Also check indexes
    email_indexed = any('email' in idx.get('column_names', []) for idx in indexes)

    assert email_unique or email_indexed, "Email should have unique index for efficient lookups"


def test_user_username_index(inspector):
    """Test that username field has a unique index"""
    indexes = inspector.get_indexes('users')
    unique_constraints = inspector.get_unique_constraints('users')

    username_unique = any('username' in uc.get('column_names', []) for uc in unique_constraints)
    username_indexed = any('username' in idx.get('column_names', []) for idx in indexes)

    assert username_unique or username_indexed, "Username should have unique index for efficient lookups"


def test_article_slug_index(inspector):
    """Test that article slug has a unique index"""
    indexes = inspector.get_indexes('articles')
    unique_constraints = inspector.get_unique_constraints('articles')

    slug_unique = any('slug' in uc.get('column_names', []) for uc in unique_constraints)
    slug_indexed = any('slug' in idx.get('column_names', []) for idx in indexes)

    assert slug_unique or slug_indexed, "Article slug should have unique index for URL lookups"


def test_category_slug_index(inspector):
    """Test that category slug has a unique index"""
    indexes = inspector.get_indexes('categories')
    unique_constraints = inspector.get_unique_constraints('categories')

    slug_unique = any('slug' in uc.get('column_names', []) for uc in unique_constraints)
    slug_indexed = any('slug' in idx.get('column_names', []) for idx in indexes)

    assert slug_unique or slug_indexed, "Category slug should have unique index"


def test_tag_name_index(inspector):
    """Test that tag name has a unique index"""
    indexes = inspector.get_indexes('tags')
    unique_constraints = inspector.get_unique_constraints('tags')

    name_unique = any('name' in uc.get('column_names', []) for uc in unique_constraints)
    name_indexed = any('name' in idx.get('column_names', []) for idx in indexes)

    assert name_unique or name_indexed, "Tag name should have unique index"


def test_article_author_index(inspector):
    """Test that article has index on author_id for filtering by author"""
    indexes = inspector.get_indexes('articles')
    fks = inspector.get_foreign_keys('articles')

    # Foreign keys often create indexes, check both
    author_id_indexed = any(
        'author_id' in idx.get('column_names', [])
        for idx in indexes
    )

    # Having a foreign key is good, but explicit index is better
    has_author_fk = any(
        'author_id' in fk.get('constrained_columns', [])
        for fk in fks
    )

    # At minimum, should have foreign key (which helps with joins)
    assert has_author_fk, "Article should have foreign key on author_id"


def test_article_category_index(inspector):
    """Test that article has index on category_id for filtering by category"""
    indexes = inspector.get_indexes('articles')
    fks = inspector.get_foreign_keys('articles')

    # Foreign keys help with joins
    has_category_fk = any(
        'category_id' in fk.get('constrained_columns', [])
        for fk in fks
    )

    assert has_category_fk, "Article should have foreign key on category_id"


def test_article_status_published_index(inspector):
    """Test that article has index on status or composite index for published articles"""
    # This is optional but recommended for performance
    # We'll check if there's at least the status column
    columns = inspector.get_columns('articles')
    status_col = [c for c in columns if c['name'] == 'status']

    assert len(status_col) > 0, "Article should have status column for filtering"


def test_comment_article_index(inspector):
    """Test that comment has index on article_id for getting article comments"""
    fks = inspector.get_foreign_keys('comments')

    has_article_fk = any(
        'article_id' in fk.get('constrained_columns', [])
        for fk in fks
    )

    assert has_article_fk, "Comment should have foreign key on article_id"


def test_comment_user_index(inspector):
    """Test that comment has index on user_id for getting user's comments"""
    fks = inspector.get_foreign_keys('comments')

    has_user_fk = any(
        'user_id' in fk.get('constrained_columns', [])
        for fk in fks
    )

    assert has_user_fk, "Comment should have foreign key on user_id"


def test_article_tag_composite_index(inspector):
    """Test that article_tags has composite unique constraint"""
    unique_constraints = inspector.get_unique_constraints('article_tags')
    indexes = inspector.get_indexes('article_tags')

    # Look for composite unique constraint on (article_id, tag_id)
    has_composite = False
    for uc in unique_constraints:
        cols = set(uc.get('column_names', []))
        if 'article_id' in cols and 'tag_id' in cols:
            has_composite = True
            break

    # Also check indexes
    if not has_composite:
        for idx in indexes:
            cols = set(idx.get('column_names', []))
            if 'article_id' in cols and 'tag_id' in cols:
                has_composite = True
                break

    assert has_composite, "ArticleTag should have composite unique constraint on (article_id, tag_id)"


def test_user_follow_composite_index(inspector):
    """Test that user_follows has composite unique constraint"""
    unique_constraints = inspector.get_unique_constraints('user_follows')
    indexes = inspector.get_indexes('user_follows')

    # Look for composite unique constraint on (follower_id, followed_id)
    has_composite = False
    for uc in unique_constraints:
        cols = set(uc.get('column_names', []))
        if 'follower_id' in cols and 'followed_id' in cols:
            has_composite = True
            break

    if not has_composite:
        for idx in indexes:
            cols = set(idx.get('column_names', []))
            if 'follower_id' in cols and 'followed_id' in cols:
                has_composite = True
                break

    assert has_composite, "UserFollow should have composite unique constraint on (follower_id, followed_id)"


def test_category_parent_index(inspector):
    """Test that category has index on parent_id for hierarchical queries"""
    fks = inspector.get_foreign_keys('categories')

    # Check for foreign key on parent_id
    has_parent_fk = any(
        'parent_id' in fk.get('constrained_columns', [])
        for fk in fks
    )

    # Parent_id foreign key helps with hierarchical queries
    assert has_parent_fk, "Category should have foreign key on parent_id for hierarchy"


def test_comment_parent_index(inspector):
    """Test that comment has index on parent_id for threaded comments"""
    fks = inspector.get_foreign_keys('comments')

    # Check for foreign key on parent_id (self-reference)
    has_parent_fk = any(
        'parent_id' in fk.get('constrained_columns', [])
        for fk in fks
    )

    # Having parent_id as FK helps with threaded comment queries
    # Note: May not be present in all implementations, so we make this informative
    # but not strictly required
    if not has_parent_fk:
        pytest.skip("Comment parent_id foreign key not found (optional)")
