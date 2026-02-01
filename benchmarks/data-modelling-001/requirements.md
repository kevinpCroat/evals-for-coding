# Blog Platform - Business Requirements

## Overview
Design a database schema for a modern blog platform that supports multiple authors, content organization, and user engagement features.

## Domain Description
The platform is a multi-author blog system where users can publish articles, organize content with tags and categories, leave comments, and follow their favorite authors. The system needs to track engagement metrics and support content moderation workflows.

## Entities to Model

### 1. User
- Users can be authors, commenters, or both
- Each user has a unique email and username
- Users have profile information (bio, avatar URL, join date)
- Users can follow other users
- Track user status (active, suspended, deleted)

### 2. Article
- Articles are written by a single author (User)
- Each article belongs to exactly one Category
- Articles have title, slug (URL-friendly identifier), content, excerpt
- Track publication status (draft, published, archived)
- Store publication date, last modified date, view count
- Slugs must be unique across the platform

### 3. Category
- Hierarchical structure (categories can have parent categories)
- Each category has a unique name and slug
- Categories have description and display order
- Track number of articles in each category

### 4. Tag
- Simple tag system for cross-category organization
- Tags have unique names (case-insensitive)
- Track usage count for each tag

### 5. Comment
- Comments belong to an Article and are written by a User
- Support threaded comments (replies to other comments)
- Track comment status (pending, approved, spam, deleted)
- Store creation date and optional edit date
- Comments can be nested up to reasonable depth

### 6. ArticleTag (Junction)
- Many-to-many relationship between Articles and Tags
- Track when tag was added to article

### 7. UserFollow (Junction)
- Users can follow other users
- Track when the follow relationship was created
- Prevent users from following themselves

## Relationships

1. **User → Article**: One-to-many (author writes many articles)
2. **Category → Article**: One-to-many (category contains many articles)
3. **Category → Category**: One-to-many (parent category has child categories)
4. **User → Comment**: One-to-many (user writes many comments)
5. **Article → Comment**: One-to-many (article has many comments)
6. **Comment → Comment**: One-to-many (parent comment has reply comments)
7. **Article ↔ Tag**: Many-to-many (articles have multiple tags, tags apply to multiple articles)
8. **User ↔ User**: Many-to-many (users follow users)

## Business Rules and Constraints

### Data Integrity
1. Email addresses must be unique and valid format
2. Usernames must be unique and contain only alphanumeric characters and underscores
3. Article slugs must be unique across all articles
4. Category slugs must be unique across all categories
5. Tag names must be unique (case-insensitive)
6. Users cannot follow themselves
7. Comments must belong to an article
8. Deleted users' content should remain but be attributed to "deleted user"

### Validation Rules
1. Article titles must be between 1-200 characters
2. Article slugs must be URL-safe (lowercase, hyphens, alphanumeric)
3. User bio limited to 500 characters
4. Comment content limited to 2000 characters
5. Category names must be between 1-50 characters
6. Tag names must be between 1-30 characters
7. Published articles must have non-empty content

### Cascading Behavior
1. When an article is deleted, its comments should be deleted
2. When an article is deleted, its tag associations should be removed
3. When a category is deleted, articles should be moved to a default "Uncategorized" category
4. When a comment is deleted, its replies should also be deleted
5. When a user is deleted, their articles and comments should remain but show as "[Deleted User]"

### Default Values
1. New articles default to 'draft' status
2. New comments default to 'pending' status
3. View count defaults to 0
4. User status defaults to 'active'
5. Timestamps should be set automatically

## Query Requirements

The schema must efficiently support these common queries:

### High-Priority Queries (Must be indexed)
1. **Get published articles by author** - Filter by user_id and status='published', ordered by publication date
2. **Get articles in category** - Filter by category_id and status='published', ordered by publication date
3. **Get articles by tag** - Join through ArticleTag, filter by tag_id and status='published'
4. **Get recent comments for article** - Filter by article_id, ordered by creation date
5. **Find article by slug** - Filter by slug (unique lookup)
6. **Get user by email** - Filter by email (unique lookup for authentication)
7. **Get user by username** - Filter by username (unique lookup for profiles)
8. **Get followers of user** - Join through UserFollow, filter by followed_id
9. **Get users followed by user** - Join through UserFollow, filter by follower_id

### Secondary Queries (Should be efficient)
1. Get most viewed articles in category (last 30 days)
2. Get most commented articles
3. Get trending tags (by usage count)
4. Get comment thread (parent comment and all nested replies)
5. Get articles by multiple tags (intersection)
6. Get author's draft articles
7. Get pending comments for moderation

## Performance Considerations

1. Articles table will be the largest (millions of rows expected)
2. Comments table will have high write volume
3. Tag associations will have many-to-many joins
4. Category hierarchy should support efficient tree queries
5. User follows could grow to thousands per user

## Data Quality

1. All timestamps should be timezone-aware (UTC)
2. String fields should have appropriate length limits
3. Numeric IDs preferred for foreign keys (not UUIDs for this use case)
4. Enum fields should be properly constrained
5. Indexes should be added based on query patterns
