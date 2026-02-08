# CONTRIBUTING

Thank you for your interest in contributing to PyPostgres! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/pypostgres.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install dev dependencies: `pip install -e ".[dev]"`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write tests for new functionality
4. Run tests: `python -m pytest tests/ -v`
5. Run code quality checks:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   isort src/ tests/
   mypy src/
   ```
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Code Style

- Follow PEP 8
- Use type hints for all function parameters and returns
- Maximum line length: 100 characters
- Use black for formatting
- Use isort for import sorting

## Testing

- Write tests for all new features
- Maintain >80% code coverage
- Use pytest for testing
- Test both happy paths and error cases

Example test:
```python
def test_insert_single_record(self):
    """Test inserting a single record"""
    with PostgresManager() as manager:
        manager.insert('users', {'name': 'John', 'age': 30})
        # Assertions here
```

## Documentation

- Update docstrings for all public methods
- Use Google-style docstrings
- Update README.md if adding features
- Update API.md for public API changes

Example docstring:
```python
def insert(self, table_name: str, data: Dict[str, Any]) -> None:
    """
    Insert a single record into a table.
    
    Args:
        table_name: Name of the target table
        data: Dictionary of column_name: value pairs
        
    Raises:
        psycopg2.Error: If insertion fails
        
    Example:
        manager.insert('users', {'name': 'John', 'age': 30})
    """
```

## Commit Messages

- Use present tense: "Add feature" not "Added feature"
- Be descriptive and concise
- Reference issues: "Fix #123"
- Format: `Type: Description`
  - `feat:` New feature
  - `fix:` Bug fix
  - `docs:` Documentation
  - `test:` Test additions
  - `refactor:` Code refactoring
  - `perf:` Performance improvement

## Pull Request Guidelines

- Fill out the PR template
- Reference related issues
- Include test coverage
- Describe changes clearly
- Update documentation

## Reporting Issues

Use GitHub Issues to report bugs. Include:
- Python version
- PostgreSQL version
- Relevant environment details
- Steps to reproduce
- Expected vs actual behavior
- Error logs

## Questions?

Open an issue or email [your-email@example.com](mailto:your-email@example.com)

---

Thank you for contributing! 🎉
