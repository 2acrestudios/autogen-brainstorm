# Code Review Skill

Perform comprehensive code reviews with focus on quality, security, and best practices.

## When to Use This Skill

- Reviewing pull requests
- Auditing existing codebase
- Ensuring code quality standards
- Identifying security vulnerabilities
- Optimizing performance

## How This Skill Works

This skill performs multi-layered code analysis:

1. **Functional Review**
   - Does the code do what it's supposed to?
   - Are edge cases handled?
   - Is error handling appropriate?

2. **Quality Review**
   - Code readability and clarity
   - Naming conventions
   - Code organization and structure
   - DRY principle adherence

3. **Security Review**
   - Input validation
   - SQL injection prevention
   - XSS vulnerabilities
   - Authentication/authorization
   - Sensitive data handling

4. **Performance Review**
   - Algorithm efficiency
   - Database query optimization
   - Memory usage
   - Caching opportunities

5. **Best Practices**
   - Language-specific conventions
   - Design patterns
   - Documentation
   - Testing coverage

## Example Usage

**User:** "Review this authentication function"

```python
def login(username, password):
    user = db.query("SELECT * FROM users WHERE username = '" + username + "'")
    if user and user.password == password:
        return True
    return False
```

**Code Review Skill Response:**

### Critical Issues 🚨

1. **SQL Injection Vulnerability**
   - Current: String concatenation creates SQL injection risk
   - Fix: Use parameterized queries
   ```python
   user = db.query("SELECT * FROM users WHERE username = ?", (username,))
   ```

2. **Plain Text Password Comparison**
   - Current: Passwords stored/compared in plain text
   - Fix: Use password hashing (bcrypt, argon2)
   ```python
   import bcrypt
   if user and bcrypt.checkpw(password.encode(), user.password_hash):
   ```

### Recommendations 💡

1. **Add Input Validation**
   ```python
   if not username or not password:
       raise ValueError("Username and password required")
   ```

2. **Implement Rate Limiting**
   - Prevent brute force attacks
   - Track failed login attempts

3. **Enhanced Error Handling**
   - Don't reveal whether username or password was wrong
   - Log failed attempts for security monitoring

### Improved Version

```python
import bcrypt
from typing import Optional

def login(username: str, password: str) -> bool:
    """
    Authenticate user with secure password verification.

    Args:
        username: User's username
        password: User's password (plain text)

    Returns:
        True if authentication successful, False otherwise

    Raises:
        ValueError: If username or password is empty
    """
    if not username or not password:
        raise ValueError("Username and password required")

    try:
        # Use parameterized query to prevent SQL injection
        user = db.query(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,)
        )

        if not user:
            # Don't reveal whether user exists
            return False

        # Verify password using bcrypt
        return bcrypt.checkpw(
            password.encode('utf-8'),
            user.password_hash
        )

    except Exception as e:
        # Log error for monitoring
        logger.error(f"Login error: {e}")
        return False
```

## Review Checklist

- [ ] Functionality works as intended
- [ ] Edge cases handled
- [ ] Error handling implemented
- [ ] Security vulnerabilities addressed
- [ ] Code is readable and maintainable
- [ ] Performance optimized
- [ ] Tests included
- [ ] Documentation updated
