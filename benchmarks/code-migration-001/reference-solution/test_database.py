"""
Comprehensive test suite for database operations.
These tests should pass with both SQLAlchemy 1.4 and 2.0 (after migration).
"""
import pytest
import os
from sqlalchemy import create_engine
from models import Base, User, Post, get_engine, get_session
from database import UserRepository, PostRepository


@pytest.fixture
def engine():
    """Create test database engine."""
    test_db = 'sqlite:///test_temp.db'
    engine = get_engine(test_db)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()
    # Clean up test database
    if os.path.exists('test_temp.db'):
        os.remove('test_temp.db')


@pytest.fixture
def session(engine):
    """Create test session."""
    session = get_session(engine)
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def user_repo(session):
    """Create UserRepository instance."""
    return UserRepository(session)


@pytest.fixture
def post_repo(session):
    """Create PostRepository instance."""
    return PostRepository(session)


class TestUserRepository:
    def test_create_user(self, user_repo):
        """Test creating a new user."""
        user = user_repo.create_user(
            username='testuser',
            email='test@example.com',
            full_name='Test User'
        )
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.full_name == 'Test User'

    def test_get_all_users(self, user_repo):
        """Test getting all users."""
        user_repo.create_user('user1', 'user1@example.com')
        user_repo.create_user('user2', 'user2@example.com')

        users = user_repo.get_all_users()
        assert len(users) == 2
        assert users[0].username == 'user1'
        assert users[1].username == 'user2'

    def test_get_user_by_id(self, user_repo):
        """Test getting user by ID."""
        created_user = user_repo.create_user('testuser', 'test@example.com')

        user = user_repo.get_user_by_id(created_user.id)
        assert user is not None
        assert user.username == 'testuser'

    def test_get_user_by_username(self, user_repo):
        """Test getting user by username."""
        user_repo.create_user('testuser', 'test@example.com')

        user = user_repo.get_user_by_username('testuser')
        assert user is not None
        assert user.email == 'test@example.com'

    def test_update_user_email(self, user_repo):
        """Test updating user email."""
        user = user_repo.create_user('testuser', 'old@example.com')

        updated_user = user_repo.update_user_email(user.id, 'new@example.com')
        assert updated_user.email == 'new@example.com'

    def test_delete_user(self, user_repo):
        """Test deleting a user."""
        user = user_repo.create_user('testuser', 'test@example.com')

        result = user_repo.delete_user(user.id)
        assert result is True

        deleted_user = user_repo.get_user_by_id(user.id)
        assert deleted_user is None

    def test_search_users(self, user_repo):
        """Test searching users."""
        user_repo.create_user('alice', 'alice@example.com')
        user_repo.create_user('bob', 'bob@test.com')
        user_repo.create_user('charlie', 'charlie@example.com')

        # Search by username
        results = user_repo.search_users('ali')
        assert len(results) == 1
        assert results[0].username == 'alice'

        # Search by email domain
        results = user_repo.search_users('example.com')
        assert len(results) == 2


class TestPostRepository:
    def test_create_post(self, user_repo, post_repo):
        """Test creating a new post."""
        user = user_repo.create_user('author', 'author@example.com')

        post = post_repo.create_post(
            title='Test Post',
            content='This is test content',
            author_id=user.id
        )
        assert post.id is not None
        assert post.title == 'Test Post'
        assert post.content == 'This is test content'
        assert post.author_id == user.id

    def test_get_all_posts(self, user_repo, post_repo):
        """Test getting all posts."""
        user = user_repo.create_user('author', 'author@example.com')
        post_repo.create_post('Post 1', 'Content 1', user.id)
        post_repo.create_post('Post 2', 'Content 2', user.id)

        posts = post_repo.get_all_posts()
        assert len(posts) == 2

    def test_get_post_by_id(self, user_repo, post_repo):
        """Test getting post by ID."""
        user = user_repo.create_user('author', 'author@example.com')
        created_post = post_repo.create_post('Test', 'Content', user.id)

        post = post_repo.get_post_by_id(created_post.id)
        assert post is not None
        assert post.title == 'Test'

    def test_get_posts_by_user(self, user_repo, post_repo):
        """Test getting posts by user."""
        user1 = user_repo.create_user('user1', 'user1@example.com')
        user2 = user_repo.create_user('user2', 'user2@example.com')

        post_repo.create_post('User1 Post', 'Content', user1.id)
        post_repo.create_post('User2 Post', 'Content', user2.id)

        posts = post_repo.get_posts_by_user(user1.id)
        assert len(posts) == 1
        assert posts[0].title == 'User1 Post'

    def test_update_post(self, user_repo, post_repo):
        """Test updating a post."""
        user = user_repo.create_user('author', 'author@example.com')
        post = post_repo.create_post('Old Title', 'Old Content', user.id)

        updated_post = post_repo.update_post(
            post.id,
            title='New Title',
            content='New Content'
        )
        assert updated_post.title == 'New Title'
        assert updated_post.content == 'New Content'

    def test_delete_post(self, user_repo, post_repo):
        """Test deleting a post."""
        user = user_repo.create_user('author', 'author@example.com')
        post = post_repo.create_post('Test', 'Content', user.id)

        result = post_repo.delete_post(post.id)
        assert result is True

        deleted_post = post_repo.get_post_by_id(post.id)
        assert deleted_post is None

    def test_get_posts_with_authors(self, user_repo, post_repo):
        """Test getting posts with joined author data."""
        user = user_repo.create_user('author', 'author@example.com', 'Author Name')
        post_repo.create_post('Test Post', 'Content', user.id)

        posts = post_repo.get_posts_with_authors()
        assert len(posts) == 1
        assert posts[0].author.username == 'author'
        assert posts[0].author.full_name == 'Author Name'


class TestRelationships:
    def test_user_posts_relationship(self, user_repo, post_repo):
        """Test that user.posts relationship works correctly."""
        user = user_repo.create_user('author', 'author@example.com')
        post_repo.create_post('Post 1', 'Content 1', user.id)
        post_repo.create_post('Post 2', 'Content 2', user.id)

        # Refresh user to load relationships
        retrieved_user = user_repo.get_user_by_id(user.id)
        assert len(retrieved_user.posts) == 2

    def test_post_author_relationship(self, user_repo, post_repo):
        """Test that post.author relationship works correctly."""
        user = user_repo.create_user('author', 'author@example.com', 'Author Name')
        post = post_repo.create_post('Test Post', 'Content', user.id)

        retrieved_post = post_repo.get_post_by_id(post.id)
        assert retrieved_post.author.username == 'author'
        assert retrieved_post.author.full_name == 'Author Name'
