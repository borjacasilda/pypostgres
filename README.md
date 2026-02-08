# PyPostgres: Professional PostgreSQL Wrapper

A production-ready Python library for interacting with PostgreSQL databases. Supports multiple data formats (CSV, JSON, Excel, PDF, SQL files) and provides a clean, Pythonic interface for common database operations.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ⚠️ IMPORTANT - Before You Start

This project requires user configuration. **Do not run code immediately after cloning.**

### Required Setup Steps:
1. **PostgreSQL must be installed** - [Download here](https://www.postgresql.org/download/)
2. **Create a database and user** in PostgreSQL
3. **Configure `.env` file** with YOUR credentials (see below)
4. **Read [SETUP.md](SETUP.md)** for detailed setup instructions

### Quick Configuration:
```bash
cp .env.example .env
# Edit .env with YOUR database credentials
```

**See [SETUP.md](SETUP.md) for complete setup instructions for your operating system.**

---

## Features

- **Simple CRUD Operations**: Insert, update, delete, and query records with ease
- **Batch Operations**: Efficiently insert large datasets with batch processing
- **Multiple Data Formats**: Support for CSV, JSON, Excel, SQL files, and pandas DataFrames
- **Table Management**: Create, drop, and inspect tables programmatically
- **Context Manager Support**: Automatic connection management using Python's context manager
- **Comprehensive Logging**: Built-in logging system for debugging and monitoring
- **Type Hints**: Full type annotations for better IDE support and code reliability
- **Error Handling**: Robust error handling with detailed logging
- **Professional Documentation**: Extensive docstrings and examples

## Requirements

- Python 3.8 or higher
- PostgreSQL 10 or higher
- psycopg2 (PostgreSQL adapter for Python)
- pandas (Data manipulation and analysis)
- PyPDF2 (PDF text extraction)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pypostgres.git
cd pypostgres
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your database credentials:
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### Configuration

For detailed setup instructions, see [SETUP.md](SETUP.md)

**Quick Configuration:**

1. Ensure PostgreSQL is installed and running
2. Copy and edit `.env`:
```bash
cp .env.example .env
```

3. Update `.env` with YOUR credentials:
```env
DB_HOST=localhost           # Your PostgreSQL server
DB_PORT=5432               # PostgreSQL port
DB_NAME=your_database      # Your database name
DB_USER=your_user         # Your username
DB_PASSWORD=your_password # Your password
LOG_LEVEL=INFO            # Logging level
```

4. Test the connection:
```bash
python3 -c "from src.postgres_manager import PostgresManager; PostgresManager().connect(); print('✓ Connected!')"
```

**Important Notes:**
- Replace `your_database`, `your_user`, and `your_password` with YOUR actual values
- `.env` is in `.gitignore` - never commit it to version control
- For local development, use the values you set when installing PostgreSQL
- For production, use strong passwords and secure credentials
- See [SETUP.md](SETUP.md) for detailed setup instructions for different environments

## Quick Start

**BEFORE PROCEEDING: Complete the setup steps above and ensure `.env` is configured.**

### Basic Usage

```python
from src.postgres_manager import PostgresManager

# Using context manager (recommended)
with PostgresManager() as manager:
    # Create a table
    columns = {
        'id': 'SERIAL',
        'name': 'VARCHAR(100)',
        'email': 'VARCHAR(100)',
        'age': 'INTEGER'
    }
    manager.create_table('users', columns, primary_key='id')
    
    # Insert a record
    user_data = {'name': 'Your Name', 'email': 'your.email@example.com', 'age': 30}
    manager.insert('users', user_data)
    
    # Query records
    results = manager.query('SELECT * FROM users')
    print(results)
```

### Insert from CSV

```python
with PostgresManager() as manager:
    # First, create your CSV file in data/ directory
    count = manager.insert_from_csv('users', 'data/your_file.csv')
    print(f"Inserted {count} records from CSV")
```

### Insert from DataFrame

```python
import pandas as pd
from src.postgres_manager import PostgresManager

# Create your own DataFrame with your data
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol'],
    'email': ['alice@example.com', 'bob@example.com', 'carol@example.com'],
    'age': [25, 30, 28]
})

with PostgresManager() as manager:
    count = manager.insert_from_dataframe('users', df)
    print(f"Inserted {count} records from DataFrame")
```

### Insert from JSON

```python
with PostgresManager() as manager:
    # Create your JSON file in data/ directory first
    count = manager.insert_from_json('employees', 'data/your_file.json')
    print(f"Inserted {count} records from JSON")
```

### Execute SQL File

```python
with PostgresManager() as manager:
    # Create your SQL file in data/ directory first
    results = manager.execute_from_sql_file('data/your_queries.sql')
    print(results)
```

### Batch Insert

```python
with PostgresManager() as manager:
    data = [
        {'name': 'Alice', 'email': 'alice@example.com', 'age': 25},
        {'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
        {'name': 'Carol', 'email': 'carol@example.com', 'age': 28},
    ]
    count = manager.insert_batch('users', data, batch_size=1000)
    print(f"Inserted {count} records")
```

### Update Records

```python
with PostgresManager() as manager:
    rows_affected = manager.update(
        'users',
        {'age': 31},
        'name = %s',
        ('John Doe',)
    )
    print(f"Updated {rows_affected} records")
```

### Delete Records

```python
with PostgresManager() as manager:
    rows_deleted = manager.delete(
        'users',
        'age < %s',
        (18,)
    )
    print(f"Deleted {rows_deleted} records")
```

### Query with DataFrame Result

```python
with PostgresManager() as manager:
    df = manager.query(
        'SELECT * FROM users WHERE age > %s ORDER BY age DESC',
        params=(25,),
        return_df=True
    )
    print(df)
```

## API Reference

### PostgresManager

Main class for PostgreSQL operations.

#### Methods

- **`__init__(config=None)`**: Initialize manager with optional database config
- **`connect()`**: Establish database connection
- **`disconnect()`**: Close database connection
- **`create_table(table_name, columns, primary_key=None, if_not_exists=True)`**: Create a new table
- **`drop_table(table_name, if_exists=True)`**: Drop a table
- **`insert(table_name, data, return_id=False)`**: Insert a single record
- **`insert_batch(table_name, data_list, batch_size=None)`**: Insert multiple records
- **`update(table_name, data, where_clause, where_params=None)`**: Update records
- **`delete(table_name, where_clause, where_params=None)`**: Delete records
- **`query(query_str, params=None, return_df=False)`**: Execute SELECT query
- **`insert_from_csv(table_name, csv_path, batch_size=None)`**: Insert from CSV file
- **`insert_from_dataframe(table_name, df, batch_size=None)`**: Insert from DataFrame
- **`insert_from_json(table_name, json_path, batch_size=None)`**: Insert from JSON file
- **`insert_from_excel(table_name, excel_path, sheet_name=0, batch_size=None)`**: Insert from Excel
- **`execute_from_sql_file(file_path)`**: Execute SQL statements from file
- **`table_exists(table_name)`**: Check if table exists
- **`get_table_columns(table_name)`**: Get table column information

## Data Readers

The library includes readers for multiple data formats:

- **CSVReader**: Read CSV files
- **JSONReader**: Read JSON files
- **SQLReader**: Read and parse SQL files
- **PDFReader**: Extract text from PDF files
- **ExcelReader**: Read Excel spreadsheets
- **DataFrameReader**: Handle pandas DataFrames
- **ReaderFactory**: Automatically select appropriate reader based on file extension

## Project Structure

```
pypostgres/
├── src/
│   ├── __init__.py
│   ├── postgres_manager.py      # Main PostgreSQL manager class
│   ├── readers.py               # Data readers for various formats
│   └── logger.py                # Logging configuration
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration management
├── tests/
│   ├── __init__.py
│   └── test_postgres_manager.py # Unit tests
├── examples/
│   └── basic_examples.py        # Usage examples
├── docs/
│   ├── API.md                   # API documentation
│   └── ARCHITECTURE.md          # Architecture documentation
├── data/                        # Sample data files
├── logs/                        # Application logs
├── .env.example                 # Example environment file
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup file
└── README.md                    # This file
```

## Examples

See the [examples/](examples/) directory for complete working examples:

- `basic_examples.py`: Comprehensive examples of all major features

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=src
```

## Logging

The library uses Python's built-in logging module. Logs are written to both console and file.

### Log Configuration

Configure logging in `.env`:
```env
LOG_LEVEL=INFO        # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/app.log
```

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical messages for very serious problems

## Error Handling

The library provides comprehensive error handling:

```python
from psycopg2 import Error
from src.postgres_manager import PostgresManager

try:
    with PostgresManager() as manager:
        manager.insert('users', {'name': 'John', 'email': 'john@example.com'})
except Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Always use context manager** for automatic connection handling:
   ```python
   with PostgresManager() as manager:
       # Your code here
   ```

2. **Use parameterized queries** to prevent SQL injection:
   ```python
   manager.query('SELECT * FROM users WHERE id = %s', params=(1,))
   ```

3. **Batch insert large datasets** for better performance:
   ```python
   manager.insert_batch('users', large_data_list, batch_size=1000)
   ```

4. **Check table existence** before operations:
   ```python
   if manager.table_exists('users'):
       # Your code here
   ```

5. **Monitor logs** for debugging and monitoring:
   ```bash
   tail -f logs/app.log
   ```

## Performance Tips

- Use `batch_size` parameter for large inserts (default: 1000)
- Create indexes on frequently queried columns
- Use DataFrame operations for complex data transformations
- Set appropriate `LOG_LEVEL` in production (use WARNING or ERROR)

## Troubleshooting

### Connection Issues

**Problem**: `psycopg2.OperationalError: could not connect to server`

**Solution**: 
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists
- Check network connectivity

### Permission Errors

**Problem**: `psycopg2.ProgrammingError: permission denied`

**Solution**:
- Ensure user has appropriate permissions
- Use a user with required privileges

### Memory Issues

**Problem**: Out of memory when inserting large datasets

**Solution**:
- Reduce `batch_size`
- Process data in smaller chunks
- Increase server memory

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**Your Name** - [your-email@example.com](mailto:your-email@example.com)

## Acknowledgments

- PostgreSQL for the amazing database system
- psycopg2 for the excellent Python adapter
- pandas for powerful data manipulation
- The Python community for great tools and libraries

## Support

For support, please:
- Open an issue on GitHub
- Email: [your-email@example.com](mailto:your-email@example.com)
- Check the documentation in the `docs/` directory

---

**Last Updated**: 2026-02-08
**Version**: 1.0.0
