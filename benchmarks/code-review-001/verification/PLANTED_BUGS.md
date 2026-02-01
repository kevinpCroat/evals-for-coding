# Planted Bugs Reference

This document lists all intentional bugs planted in the code for verification purposes.

## Bug List

### Bug 1: Hardcoded API Key
- **Line**: 15
- **Severity**: CRITICAL
- **Description**: API key hardcoded in source code
- **Code**: `API_KEY = "sk-prod-a8f9d2e1c4b7a3f6"`
- **Issue**: Hardcoded secrets in source code is a critical security vulnerability

### Bug 2: SQL Injection in authenticate_user
- **Line**: 26
- **Severity**: CRITICAL
- **Description**: SQL injection vulnerability in authentication
- **Code**: `query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"`
- **Issue**: User input directly interpolated into SQL query without sanitization

### Bug 3: Off-by-One Error in get_active_users
- **Line**: 49
- **Severity**: HIGH
- **Description**: Loop starts at index 1 instead of 0, skipping first user
- **Code**: `for i in range(1, len(users)):`
- **Issue**: First active user in result set will be skipped

### Bug 4: Resource Leak in update_user_status
- **Line**: 63
- **Severity**: HIGH
- **Description**: Database cursor not closed after use
- **Code**: Missing `cursor.close()` after commit
- **Issue**: Can lead to resource exhaustion over time

### Bug 5: Performance Issue - N+1 Query
- **Line**: 71
- **Severity**: MEDIUM
- **Description**: Inefficient batch processing with N+1 queries
- **Code**: Loop creating separate cursor and query for each user_id
- **Issue**: Should use single query with IN clause for better performance

### Bug 6: File Handle Leak in export_user_data
- **Line**: 84
- **Severity**: HIGH
- **Description**: File handle opened but never closed
- **Code**: `file = open(filename, 'w')` with no corresponding `file.close()`
- **Issue**: File handle leak can cause resource exhaustion

### Bug 7: Wrong Operator in calculate_user_score
- **Line**: 99
- **Severity**: HIGH
- **Description**: Addition used instead of multiplication for score calculation
- **Code**: `base_score = login_count + activity_days`
- **Issue**: Logic error - based on variable names, should multiply not add

### Bug 8: Division by Zero in calculate_user_score
- **Line**: 102
- **Severity**: MEDIUM
- **Description**: No check for zero login_count before division
- **Code**: `engagement_ratio = activity_days / login_count`
- **Issue**: Will crash with ZeroDivisionError if login_count is 0

### Bug 9: Race Condition in process_async_task
- **Line**: 109
- **Severity**: HIGH
- **Description**: Shared cache accessed without synchronization
- **Code**: Multiple threads accessing `self.cache` without locking
- **Issue**: Race condition can lead to data corruption or inconsistent state

### Bug 10: Missing Error Handling in get_user_permissions
- **Line**: 133
- **Severity**: MEDIUM
- **Description**: No null check before accessing result
- **Code**: `return result[0].split(',')`
- **Issue**: Will raise TypeError/AttributeError if user not found (result is None)

### Bug 11: SQL Injection in search_users
- **Line**: 148
- **Severity**: CRITICAL
- **Description**: SQL injection vulnerability in search functionality
- **Code**: `query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"`
- **Issue**: User input directly interpolated into SQL query without sanitization

## Correct Code (Should NOT be flagged)

The following are intentionally correct implementations to test false positive rate:

### Correct 1: get_user_by_id (Lines 30-34)
- Properly uses parameterized query
- Correctly returns result

### Correct 2: hash_password (Lines 46-48)
- Properly uses SHA-256 hashing
- Good implementation

### Correct 3: validate_email (Lines 106-108)
- Simple but functional email validation
- Correct logic

### Correct 4: cleanup_old_sessions (Lines 123-129)
- Proper date handling
- Correct parameterized query
- Properly closes cursor

### Correct 5: __del__ method (Lines 138-141)
- Properly checks for attribute existence
- Correctly closes connection

### Correct 6: Thread creation in process_async_task (Line 101)
- Thread is started properly (though the function it runs has a race condition)

## Summary

- **Total Bugs**: 11
- **CRITICAL**: 3 (Bugs 1, 2, 11)
- **HIGH**: 5 (Bugs 3, 4, 6, 7, 9)
- **MEDIUM**: 3 (Bugs 5, 8, 10)
- **LOW**: 0

- **Correct Implementations**: 6 items that should NOT be flagged
