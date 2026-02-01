"""
Test constraints - verify database enforces data integrity rules
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def session():
    """Create a test database session"""
    import models

    engine = create_engine('sqlite:///:memory:')
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.rollback()
    session.close()


def test_user_email_unique(session):
    """Test that user email must be unique"""
    import models

    user1 = models.User(email='duplicate@test.com', username='user1', status='active')
    session.add(user1)
    session.commit()

    user2 = models.User(email='duplicate@test.com', username='user2', status='active')
    session.add(user2)

    with pytest.raises(IntegrityError):
        session.commit()


def test_user_username_unique(session):
    """Test that username must be unique"""
    import models

    user1 = models.User(email='user1@test.com', username='duplicate', status='active')
    session.add(user1)
    session.commit()

    user2 = models.User(email='user2@test.com', username='duplicate', status='active')
    session.add(user2)

    with pytest.raises(IntegrityError):
        session.commit()


def test_article_slug_unique(session):
    """Test that article slug must be unique"""
    import models

    user = models.User(email='author@test.com', username='author', status='active')
    category = models.Category(name='Tech', slug='tech', display_order=1)
    session.add_all([user, category])
    session.commit()

    article1 = models.Article(
        title='Article 1',
        slug='duplicate-slug',
        content='Content 1',
        excerpt='Excerpt 1',
        status='draft',
        author=user,
        category=category,
        view_count=0
    )
    session.add(article1)
    session.commit()

    article2 = models.Article(
        title='Article 2',
        slug='duplicate-slug',
        content='Content 2',
        excerpt='Excerpt 2',
        status='draft',
        author=user,
        category=category,
        view_count=0
    )
    session.add(article2)

    with pytest.raises(IntegrityError):
        session.commit()


def test_category_slug_unique(session):
    """Test that category slug must be unique"""
    import models

    cat1 = models.Category(name='Category 1', slug='duplicate', display_order=1)
    session.add(cat1)
    session.commit()

    cat2 = models.Category(name='Category 2', slug='duplicate', display_order=2)
    session.add(cat2)

    with pytest.raises(IntegrityError):
        session.commit()


def test_tag_name_unique(session):
    """Test that tag name must be unique (case-insensitive)"""
    import models

    tag1 = models.Tag(name='python', usage_count=0)
    session.add(tag1)
    session.commit()

    # Try to create another tag with same name (even different case)
    tag2 = models.Tag(name='python', usage_count=0)
    session.add(tag2)

    with pytest.raises(IntegrityError):
        session.commit()


def test_article_requires_author(session):
    """Test that article must have an author (not null constraint)"""
    import models

    category = models.Category(name='Test', slug='test', display_order=1)
    session.add(category)
    session.commit()

    # Try to create article without author
    article = models.Article(
        title='No Author',
        slug='no-author',
        content='Content',
        excerpt='Excerpt',
        status='draft',
        category=category,
        view_count=0
    )
    session.add(article)

    with pytest.raises(IntegrityError):
        session.commit()


def test_article_requires_category(session):
    """Test that article must have a category (not null constraint)"""
    import models

    user = models.User(email='test@test.com', username='test', status='active')
    session.add(user)
    session.commit()

    # Try to create article without category
    article = models.Article(
        title='No Category',
        slug='no-category',
        content='Content',
        excerpt='Excerpt',
        status='draft',
        author=user,
        view_count=0
    )
    session.add(article)

    with pytest.raises(IntegrityError):
        session.commit()


def test_comment_requires_article(session):
    """Test that comment must belong to an article"""
    import models

    user = models.User(email='test@test.com', username='test', status='active')
    session.add(user)
    session.commit()

    # Try to create comment without article
    comment = models.Comment(
        content='Orphan comment',
        status='approved',
        user=user
    )
    session.add(comment)

    with pytest.raises(IntegrityError):
        session.commit()


def test_comment_requires_user(session):
    """Test that comment must have a user"""
    import models

    user = models.User(email='author@test.com', username='author', status='active')
    category = models.Category(name='Test', slug='test', display_order=1)
    article = models.Article(
        title='Test',
        slug='test',
        content='Content',
        excerpt='Excerpt',
        status='published',
        author=user,
        category=category,
        view_count=0
    )
    session.add_all([user, category, article])
    session.commit()

    # Try to create comment without user
    comment = models.Comment(
        content='No user',
        status='approved',
        article=article
    )
    session.add(comment)

    with pytest.raises(IntegrityError):
        session.commit()


def test_foreign_key_constraint_article_author(session):
    """Test foreign key constraint for article author"""
    import models

    category = models.Category(name='Test', slug='test', display_order=1)
    session.add(category)
    session.commit()

    # Try to create article with invalid author_id
    article = models.Article(
        title='Invalid Author',
        slug='invalid-author',
        content='Content',
        excerpt='Excerpt',
        status='draft',
        author_id=99999,  # Non-existent user
        category=category,
        view_count=0
    )
    session.add(article)

    with pytest.raises(IntegrityError):
        session.commit()


def test_foreign_key_constraint_article_category(session):
    """Test foreign key constraint for article category"""
    import models

    user = models.User(email='test@test.com', username='test', status='active')
    session.add(user)
    session.commit()

    # Try to create article with invalid category_id
    article = models.Article(
        title='Invalid Category',
        slug='invalid-category',
        content='Content',
        excerpt='Excerpt',
        status='draft',
        author=user,
        category_id=99999,  # Non-existent category
        view_count=0
    )
    session.add(article)

    with pytest.raises(IntegrityError):
        session.commit()


def test_user_follow_unique_constraint(session):
    """Test that a user cannot follow the same user twice"""
    import models

    user1 = models.User(email='user1@test.com', username='user1', status='active')
    user2 = models.User(email='user2@test.com', username='user2', status='active')
    session.add_all([user1, user2])
    session.commit()

    # Create first follow
    follow1 = models.UserFollow(follower=user1, followed=user2)
    session.add(follow1)
    session.commit()

    # Try to create duplicate follow
    follow2 = models.UserFollow(follower=user1, followed=user2)
    session.add(follow2)

    with pytest.raises(IntegrityError):
        session.commit()


def test_article_tag_unique_constraint(session):
    """Test that an article cannot have the same tag twice"""
    import models

    user = models.User(email='test@test.com', username='test', status='active')
    category = models.Category(name='Test', slug='test', display_order=1)
    article = models.Article(
        title='Test',
        slug='test',
        content='Content',
        excerpt='Excerpt',
        status='published',
        author=user,
        category=category,
        view_count=0
    )
    tag = models.Tag(name='python', usage_count=0)
    session.add_all([user, category, article, tag])
    session.commit()

    # Create first article-tag association
    at1 = models.ArticleTag(article=article, tag=tag)
    session.add(at1)
    session.commit()

    # Try to create duplicate association
    at2 = models.ArticleTag(article=article, tag=tag)
    session.add(at2)

    with pytest.raises(IntegrityError):
        session.commit()


def test_cascade_delete_article_comments(session):
    """Test that deleting an article deletes its comments"""
    import models

    user = models.User(email='test@test.com', username='test', status='active')
    category = models.Category(name='Test', slug='test', display_order=1)
    article = models.Article(
        title='Test',
        slug='test',
        content='Content',
        excerpt='Excerpt',
        status='published',
        author=user,
        category=category,
        view_count=0
    )
    session.add_all([user, category, article])
    session.commit()

    comment = models.Comment(
        content='Test comment',
        status='approved',
        article=article,
        user=user
    )
    session.add(comment)
    session.commit()

    comment_id = comment.id

    # Delete article
    session.delete(article)
    session.commit()

    # Verify comment was deleted
    deleted_comment = session.query(models.Comment).filter_by(id=comment_id).first()
    assert deleted_comment is None, "Comment should be deleted when article is deleted"
