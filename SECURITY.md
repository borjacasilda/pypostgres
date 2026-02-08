# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in PyPostgres, please email [your-email@example.com](mailto:your-email@example.com) instead of using the public issue tracker.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

We will acknowledge receipt of your report within 48 hours and provide regular updates on our progress.

## Security Best Practices

When using PyPostgres:

1. **Always use parameterized queries** to prevent SQL injection:
   ```python
   # Good
   manager.query('SELECT * FROM users WHERE id = %s', params=(user_id,))
   
   # Bad - vulnerable to SQL injection
   manager.query(f'SELECT * FROM users WHERE id = {user_id}')
   ```

2. **Secure your credentials**:
   - Store database credentials in `.env` file
   - Never commit `.env` to version control
   - Use strong passwords

3. **Use environment variables** for sensitive data:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   password = os.getenv('DB_PASSWORD')
   ```

4. **Keep dependencies updated**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

5. **Use SSL/TLS for database connections** in production:
   ```python
   config = {
       'host': 'localhost',
       'sslmode': 'require',
       'sslcert': '/path/to/cert',
       # ... other config
   }
   ```

6. **Validate user input** before using in queries
7. **Review logs regularly** for suspicious activity
8. **Implement proper access controls** on database level

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✓ Yes     |

## Security Updates

We will release security updates for:
- Critical vulnerabilities
- SQL injection vulnerabilities
- Authentication/authorization issues
- Data exposure issues

---

Last Updated: 2026-02-08
