"""
Test schema validity - verify all models create tables successfully
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker


def test_models_importable():
    """Test that models.py exists and can be imported"""
    try:
        import models
        assert hasattr(models, 'Base'), "models.py must define a Base"
    except ImportError as e:
        pytest.fail(f"Cannot import models: {e}")


def test_all_models_defined():
    """Test that all required models are defined"""
    import models

    required_models = ['User', 'Article', 'Category', 'Tag', 'Comment', 'ArticleTag', 'UserFollow']

    for model_name in required_models:
        assert hasattr(models, model_name), f"Model {model_name} not found in models.py"


def test_schema_creates_successfully():
    """Test that schema creates all tables without errors"""
    import models

    # Create in-memory SQLite database
    engine = create_engine('sqlite:///:memory:')

    try:
        # Create all tables
        models.Base.metadata.create_all(engine)
    except Exception as e:
        pytest.fail(f"Failed to create schema: {e}")

    # Verify tables were created
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = ['users', 'articles', 'categories', 'tags', 'comments', 'article_tags', 'user_follows']

    for table in expected_tables:
        assert table in tables, f"Table {table} was not created"


def test_user_model_fields():
    """Test User model has required fields"""
    import models

    user_columns = [c.name for c in models.User.__table__.columns]

    required_fields = ['id', 'email', 'username', 'bio', 'avatar_url', 'created_at', 'status']
    for field in required_fields:
        assert field in user_columns, f"User model missing field: {field}"


def test_article_model_fields():
    """Test Article model has required fields"""
    import models

    article_columns = [c.name for c in models.Article.__table__.columns]

    required_fields = ['id', 'title', 'slug', 'content', 'excerpt', 'status',
                      'published_at', 'updated_at', 'view_count', 'author_id', 'category_id']
    for field in required_fields:
        assert field in article_columns, f"Article model missing field: {field}"


def test_category_model_fields():
    """Test Category model has required fields"""
    import models

    category_columns = [c.name for c in models.Category.__table__.columns]

    required_fields = ['id', 'name', 'slug', 'description', 'parent_id', 'display_order']
    for field in required_fields:
        assert field in category_columns, f"Category model missing field: {field}"


def test_tag_model_fields():
    """Test Tag model has required fields"""
    import models

    tag_columns = [c.name for c in models.Tag.__table__.columns]

    required_fields = ['id', 'name', 'usage_count']
    for field in required_fields:
        assert field in tag_columns, f"Tag model missing field: {field}"


def test_comment_model_fields():
    """Test Comment model has required fields"""
    import models

    comment_columns = [c.name for c in models.Comment.__table__.columns]

    required_fields = ['id', 'content', 'status', 'created_at', 'edited_at',
                      'article_id', 'user_id', 'parent_id']
    for field in required_fields:
        assert field in comment_columns, f"Comment model missing field: {field}"


def test_article_tag_model_fields():
    """Test ArticleTag junction model has required fields"""
    import models

    article_tag_columns = [c.name for c in models.ArticleTag.__table__.columns]

    required_fields = ['article_id', 'tag_id', 'created_at']
    for field in required_fields:
        assert field in article_tag_columns, f"ArticleTag model missing field: {field}"


def test_user_follow_model_fields():
    """Test UserFollow junction model has required fields"""
    import models

    user_follow_columns = [c.name for c in models.UserFollow.__table__.columns]

    required_fields = ['follower_id', 'followed_id', 'created_at']
    for field in required_fields:
        assert field in user_follow_columns, f"UserFollow model missing field: {field}"


def test_foreign_keys_defined():
    """Test that foreign key relationships are defined"""
    import models

    engine = create_engine('sqlite:///:memory:')
    models.Base.metadata.create_all(engine)
    inspector = inspect(engine)

    # Check Article foreign keys
    article_fks = inspector.get_foreign_keys('articles')
    fk_columns = [fk['constrained_columns'][0] for fk in article_fks]
    assert 'author_id' in fk_columns, "Article missing foreign key to User"
    assert 'category_id' in fk_columns, "Article missing foreign key to Category"

    # Check Comment foreign keys
    comment_fks = inspector.get_foreign_keys('comments')
    fk_columns = [fk['constrained_columns'][0] for fk in comment_fks]
    assert 'article_id' in fk_columns, "Comment missing foreign key to Article"
    assert 'user_id' in fk_columns, "Comment missing foreign key to User"

    # Check Category self-reference
    category_fks = inspector.get_foreign_keys('categories')
    fk_columns = [fk['constrained_columns'][0] for fk in category_fks]
    assert 'parent_id' in fk_columns, "Category missing self-referential foreign key"
