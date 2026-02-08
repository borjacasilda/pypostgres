# GitHub Copilot Instructions

This project uses GitHub Copilot for development assistance.

## Project Overview

**PyPostgres** is a professional PostgreSQL wrapper library for Python with support for multiple data formats and comprehensive database operations.

## Project Structure

- `src/`: Source code
  - `postgres_manager.py`: Main PostgreSQL manager class
  - `readers.py`: Data format readers (CSV, JSON, Excel, PDF, SQL)
  - `logger.py`: Logging configuration
- `config/`: Configuration management
- `tests/`: Unit tests
- `examples/`: Usage examples
- `docs/`: Documentation (API, Architecture)

## Development Guidelines

1. **Type Hints**: All functions must have type hints
2. **Docstrings**: Use Google-style docstrings for all public methods
3. **Logging**: Use the configured logger for all operations
4. **Error Handling**: Catch and log all exceptions properly
5. **Testing**: Write tests for all new features
6. **Documentation**: Update docs when adding features

## Key Classes and Methods

### PostgresManager
- `connect()`, `disconnect()`
- `create_table()`, `drop_table()`, `table_exists()`
- `insert()`, `insert_batch()`, `update()`, `delete()`
- `query()`
- `insert_from_csv()`, `insert_from_dataframe()`, `insert_from_json()`, `insert_from_excel()`
- `execute_from_sql_file()`

### Readers
- `CSVReader`, `JSONReader`, `SQLReader`, `PDFReader`, `ExcelReader`
- `ReaderFactory`: Factory for automatic reader selection

## Coding Standards

- Follow PEP 8
- Maximum line length: 100 characters
- Use context managers for resource management
- Parameterize all SQL queries (prevent SQL injection)
- Use logging instead of print statements

## Before Committing

1. Run tests: `pytest tests/ -v`
2. Format code: `black src/ tests/`
3. Check style: `flake8 src/ tests/`
4. Check types: `mypy src/`
5. Update documentation if needed
