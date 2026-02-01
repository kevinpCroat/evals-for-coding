"""
Database models using SQLAlchemy 1.4 patterns.
This code uses deprecated APIs that need migration to SQLAlchemy 2.0.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False)
    full_name = Column(String(100))

    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String(5000))
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(title='{self.title}')>"


def get_engine(database_url='sqlite:///test.db'):
    """Create database engine using old-style create_engine."""
    return create_engine(database_url)


def get_session(engine):
    """Create session using old sessionmaker pattern."""
    Session = sessionmaker(bind=engine)
    return Session()
