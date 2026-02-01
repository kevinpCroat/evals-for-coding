"""
Test relationships - verify all relationships work bidirectionally
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def session():
    """Create a test database session"""
    import models

    engine = create_engine('sqlite:///:memory:')
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


def test_user_articles_relationship(session):
    """Test User -> Article one-to-many relationship"""
    import models

    user = models.User(email='author@test.com', username='author', status='active')
    session.add(user)
    session.commit()

    # Check that articles relationship exists
    assert hasattr(user, 'articles'), "User model missing 'articles' relationship"

    # Create article through relationship
    category = models.Category(name='Tech', slug='tech', display_order=1)
    article = models.Article(
        title='Test Article',
        slug='test-article',
        content='Content',
        excerpt='Excerpt',
        status='draft',
        author=user,
        category=category,
        view_count=0
    )
    session.add(article)
    session.commit()

    # Verify bidirectional relationship
    assert article in user.articles
    assert article.author == user


def test_category_articles_relationship(session):
    """Test Category -> Article one-to-many relationship"""
    import models

    user = models.User(email='user@test.com', username='user', status='active')
    category = models.Category(name='News', slug='news', display_order=1)
    session.add_all([user, category])
    session.commit()

    article = models.Article(
        title='News Article',
        slug='news-article',
        content='Content',
        excerpt='Excerpt',
        status='draft',
        author=user,
        category=category,
        view_count=0
    )
    session.add(article)
    session.commit()

    # Check relationship exists
    assert hasattr(category, 'articles'), "Category model missing 'articles' relationship"
    assert article in category.articles
    assert article.category == category


def test_article_comments_relationship(session):
    """Test Article -> Comment one-to-many relationship"""
    import models

    user = models.User(email='commenter@test.com', username='commenter', status='active')
    category = models.Category(name='Blog', slug='blog', display_order=1)
    article = models.Article(
        title='Article',
        slug='article',
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
        content='Great article!',
        status='approved',
        article=article,
        user=user
    )
    session.add(comment)
    session.commit()

    # Check relationship
    assert hasattr(article, 'comments'), "Article model missing 'comments' relationship"
    assert comment in article.comments
    assert comment.article == article


def test_user_comments_relationship(session):
    """Test User -> Comment one-to-many relationship"""
    import models

    user = models.User(email='test@test.com', username='testuser', status='active')
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
    session.add_all([user, article])
    session.commit()

    comment = models.Comment(
        content='Comment',
        status='approved',
        article=article,
        user=user
    )
    session.add(comment)
    session.commit()

    # Check relationship
    assert hasattr(user, 'comments'), "User model missing 'comments' relationship"
    assert comment in user.comments


def test_comment_replies_relationship(session):
    """Test Comment -> Comment (self-referential) relationship"""
    import models

    user = models.User(email='reply@test.com', username='replyuser', status='active')
    category = models.Category(name='Discussion', slug='discussion', display_order=1)
    article = models.Article(
        title='Discussion',
        slug='discussion',
        content='Content',
        excerpt='Excerpt',
        status='published',
        author=user,
        category=category,
        view_count=0
    )
    session.add_all([user, article])
    session.commit()

    parent_comment = models.Comment(
        content='Parent comment',
        status='approved',
        article=article,
        user=user
    )
    session.add(parent_comment)
    session.commit()

    reply = models.Comment(
        content='Reply comment',
        status='approved',
        article=article,
        user=user,
        parent=parent_comment
    )
    session.add(reply)
    session.commit()

    # Check relationship
    assert hasattr(parent_comment, 'replies'), "Comment model missing 'replies' relationship"
    assert reply in parent_comment.replies
    assert reply.parent == parent_comment


def test_category_subcategories_relationship(session):
    """Test Category -> Category (self-referential) relationship"""
    import models

    parent = models.Category(name='Programming', slug='programming', display_order=1)
    session.add(parent)
    session.commit()

    child = models.Category(
        name='Python',
        slug='python',
        display_order=1,
        parent=parent
    )
    session.add(child)
    session.commit()

    # Check relationship
    assert hasattr(parent, 'subcategories'), "Category model missing 'subcategories' relationship"
    assert child in parent.subcategories
    assert child.parent == parent


def test_article_tags_many_to_many(session):
    """Test Article <-> Tag many-to-many relationship"""
    import models

    user = models.User(email='tagger@test.com', username='tagger', status='active')
    category = models.Category(name='Tech', slug='tech-cat', display_order=1)
    article = models.Article(
        title='Tagged Article',
        slug='tagged-article',
        content='Content',
        excerpt='Excerpt',
        status='published',
        author=user,
        category=category,
        view_count=0
    )
    tag1 = models.Tag(name='python', usage_count=0)
    tag2 = models.Tag(name='sqlalchemy', usage_count=0)
    session.add_all([user, category, article, tag1, tag2])
    session.commit()

    # Add tags to article
    article_tag1 = models.ArticleTag(article=article, tag=tag1)
    article_tag2 = models.ArticleTag(article=article, tag=tag2)
    session.add_all([article_tag1, article_tag2])
    session.commit()

    # Check many-to-many works through junction table
    assert hasattr(article, 'article_tags'), "Article model missing 'article_tags' relationship"
    assert hasattr(tag1, 'article_tags'), "Tag model missing 'article_tags' relationship"

    # Verify associations
    assert len(article.article_tags) == 2
    tag_ids = [at.tag_id for at in article.article_tags]
    assert tag1.id in tag_ids
    assert tag2.id in tag_ids


def test_user_follows_many_to_many(session):
    """Test User <-> User (self-referential many-to-many) relationship"""
    import models

    user1 = models.User(email='user1@test.com', username='user1', status='active')
    user2 = models.User(email='user2@test.com', username='user2', status='active')
    session.add_all([user1, user2])
    session.commit()

    # User1 follows User2
    follow = models.UserFollow(follower=user1, followed=user2)
    session.add(follow)
    session.commit()

    # Check relationships exist
    assert hasattr(user1, 'following'), "User model missing 'following' relationship"
    assert hasattr(user2, 'followers'), "User model missing 'followers' relationship"

    # Verify bidirectional relationship
    assert len(user1.following) == 1
    assert user1.following[0].followed == user2

    assert len(user2.followers) == 1
    assert user2.followers[0].follower == user1
