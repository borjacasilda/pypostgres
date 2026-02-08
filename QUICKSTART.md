# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running
- A PostgreSQL database and user created

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pypostgres.git
cd pypostgres

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration (IMPORTANT!)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with YOUR PostgreSQL credentials
# Replace:
#   DB_HOST - Your database server (usually localhost)
#   DB_PORT - Your PostgreSQL port (usually 5432)
#   DB_NAME - Your database name
#   DB_USER - Your database username
#   DB_PASSWORD - Your database password
```

**For detailed setup instructions, see [SETUP.md](SETUP.md)**

## Running Examples

The project includes example code in `examples/basic_examples.py`.

**IMPORTANT:** Before running examples:
1. Ensure PostgreSQL is running
2. Configure `.env` with YOUR database credentials
3. Uncomment the examples you want to run

Example code structure:
```python
if __name__ == "__main__":
    # Uncomment the examples you want to run:
    # example_basic_operations()
    # example_from_csv()
    # example_from_dataframe()
    # example_from_json()
    # example_from_sql_file()
```

Run examples:
```bash
python examples/basic_examples.py
```

Each example includes comments indicating where to add YOUR OWN DATA.

## Common Operations

### Create a Table

```python
from src.postgres_manager import PostgresManager

with PostgresManager() as manager:
    columns = {
        'id': 'SERIAL',
        'name': 'VARCHAR(100)',
        'email': 'VARCHAR(100)',
    }
    manager.create_table('users', columns, primary_key='id')
```

### Insert Records

```python
with PostgresManager() as manager:
    # Single record
    manager.insert('users', {'name': 'Your Name', 'email': 'your@email.com'})
    
    # Multiple records
    data = [
        {'name': 'Alice', 'email': 'alice@example.com'},
        {'name': 'Bob', 'email': 'bob@example.com'},
    ]
    manager.insert_batch('users', data)
```

### Query Data

```python
with PostgresManager() as manager:
    # Get all records
    results = manager.query('SELECT * FROM users')
    
    # Get as DataFrame
    df = manager.query('SELECT * FROM users WHERE age > 25', return_df=True)
    print(df)
```

### Update Records

```python
with PostgresManager() as manager:
    manager.update(
        'users',
        {'age': 31},
        'name = %s',
        ('John Doe',)
    )
```

### Delete Records

```python
with PostgresManager() as manager:
    manager.delete('users', 'age < %s', (18,))
```

## Working With Your Data

### CSV Files
1. Create your CSV file in `data/` directory
2. Use it in code:
```python
with PostgresManager() as manager:
    count = manager.insert_from_csv('users', 'data/your_file.csv')
```

### JSON Files
1. Create your JSON file in `data/` directory
2. Use it in code:
```python
with PostgresManager() as manager:
    count = manager.insert_from_json('users', 'data/your_file.json')
```

### Excel Files
1. Create your Excel file in `data/` directory
2. Use it in code:
```python
with PostgresManager() as manager:
    count = manager.insert_from_excel('users', 'data/your_file.xlsx')
```

### SQL Files
1. Create your SQL file in `data/` directory
2. Use it in code:
```python
with PostgresManager() as manager:
    manager.execute_from_sql_file('data/your_file.sql')
```

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src
```

## Code Quality

```bash
# Install dev tools
pip install black flake8 isort mypy

# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/
```

## Documentation

- **README.md**: Project overview and features
- **docs/API.md**: Detailed API reference
- **docs/ARCHITECTURE.md**: Architecture and design decisions
- **CONTRIBUTING.md**: Contribution guidelines
- **SECURITY.md**: Security best practices
- **examples/basic_examples.py**: Working examples

## Troubleshooting

### Connection Error
- Check if PostgreSQL is running
- Verify credentials in .env
- Check if database exists

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version is 3.8+

### Test Failures
- Start a PostgreSQL database locally
- Or configure test database in pytest configuration

## Next Steps

1. Read the full [README.md](README.md)
2. Explore [examples/basic_examples.py](examples/basic_examples.py)
3. Review [docs/API.md](docs/API.md) for detailed API reference
4. Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Getting Help

- 📖 Read the documentation in `docs/`
- 🐛 Report issues on GitHub
- 💬 Email: [your-email@example.com](mailto:your-email@example.com)

---

Happy coding! 🚀
