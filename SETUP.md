# Setup Guide - PyPostgres Configuration

## Prerequisites

Before you can use PyPostgres, ensure you have:
- Python 3.8 or higher
- PostgreSQL 10 or higher installed and running
- pip (Python package manager)

---

## Step 1: PostgreSQL Setup

### On macOS (using Homebrew)
```bash
brew install postgresql
brew services start postgresql
createuser -P myuser          # Create a user (you'll be prompted for password)
createdb -O myuser mydatabase # Create a database
```

### On Linux (Ubuntu/Debian)
```bash
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql
```

Then in PostgreSQL prompt:
```sql
CREATE USER myuser WITH PASSWORD 'mypassword';
CREATE DATABASE mydatabase OWNER myuser;
```

### On Windows
- Download PostgreSQL from https://www.postgresql.org/download/windows/
- Run the installer
- Remember the password you set for the postgres user
- Use pgAdmin to create a new database and user

---

## Step 2: Clone and Install PyPostgres

```bash
# Clone the repository
git clone https://github.com/yourusername/pypostgres.git
cd pypostgres

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Optional: Run Setup Script
```bash
# On macOS/Linux:
bash setup.sh

# This script will:
# - Upgrade pip
# - Install all dependencies
# - Install dev dependencies
# - Create logs directory
```

---

## Step 3: Configure Database Connection

### Create .env file from template
```bash
cp .env.example .env
```

### Edit .env with your credentials
```env
# YOUR DATABASE CREDENTIALS
DB_HOST=localhost           # or your database server address
DB_PORT=5432               # PostgreSQL default port
DB_NAME=mydatabase          # Database name you created
DB_USER=myuser             # User you created
DB_PASSWORD=mypassword     # Password you set

# LOGGING
LOG_LEVEL=INFO             # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/app.log      # Log file location
```

### Example configurations for different scenarios

**Local Development:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=development_db
DB_USER=dev_user
DB_PASSWORD=dev_password
LOG_LEVEL=DEBUG
```

**Production (Remote Server):**
```env
DB_HOST=db.example.com
DB_PORT=5432
DB_NAME=prod_database
DB_USER=prod_user
DB_PASSWORD=secure_password_here
LOG_LEVEL=WARNING
```

**Docker PostgreSQL:**
```env
DB_HOST=postgres  # Container name if using docker-compose
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
LOG_LEVEL=INFO
```

---

## Step 4: Test Your Configuration

### Test connection
```bash
python3 -c "
from src.postgres_manager import PostgresManager

try:
    with PostgresManager() as manager:
        print('✓ Connection successful!')
except Exception as e:
    print(f'✗ Connection failed: {e}')
"
```

### Or create a simple test script (`test_connection.py`):
```python
from src.postgres_manager import PostgresManager

def test_connection():
    try:
        with PostgresManager() as manager:
            # Test basic query
            result = manager.query("SELECT version()")
            print("✓ Connection successful!")
            print(f"PostgreSQL version: {result[0][0]}")
            return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
```

Run it:
```bash
python3 test_connection.py
```

---

## Step 5: Create Your First Table

Create a file `my_first_example.py`:

```python
from src.postgres_manager import PostgresManager

# Define your table structure
columns = {
    'id': 'SERIAL',
    'name': 'VARCHAR(100) NOT NULL',
    'email': 'VARCHAR(100) UNIQUE',
    'age': 'INTEGER'
}

# Create table and insert data
with PostgresManager() as manager:
    # Create table
    manager.create_table('users', columns, primary_key='id')
    print("✓ Table created!")
    
    # Insert a record
    manager.insert('users', {
        'name': 'Your Name',
        'email': 'your.email@example.com',
        'age': 30
    })
    print("✓ Record inserted!")
    
    # Query data
    results = manager.query('SELECT * FROM users')
    print(f"✓ Retrieved {len(results)} records")
```

Run it:
```bash
python3 my_first_example.py
```

---

## Step 6: Working with Your Data Files

### CSV Files
1. Create your CSV file in `data/` directory:
```csv
name,email,age
John Doe,john@example.com,30
Jane Smith,jane@example.com,28
```

2. Use it in your code:
```python
from src.postgres_manager import PostgresManager

with PostgresManager() as manager:
    # First create the table structure
    columns = {
        'id': 'SERIAL',
        'name': 'VARCHAR(100)',
        'email': 'VARCHAR(100)',
        'age': 'INTEGER'
    }
    manager.create_table('users', columns, primary_key='id')
    
    # Then import CSV
    count = manager.insert_from_csv('users', 'data/your_file.csv')
    print(f"Imported {count} records")
```

### JSON Files
1. Create your JSON file in `data/` directory:
```json
[
    {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    },
    {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "age": 28
    }
]
```

2. Use it in your code:
```python
with PostgresManager() as manager:
    count = manager.insert_from_json('users', 'data/your_file.json')
    print(f"Imported {count} records")
```

### Excel Files
1. Create your Excel file in `data/` directory with your data

2. Use it in your code:
```python
with PostgresManager() as manager:
    count = manager.insert_from_excel(
        'users',
        'data/your_file.xlsx',
        sheet_name='Sheet1'
    )
    print(f"Imported {count} records")
```

### SQL Files
1. Create your SQL file in `data/` directory:
```sql
-- Create table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2)
);

-- Insert data
INSERT INTO products (name, price) VALUES
    ('Laptop', 999.99),
    ('Mouse', 29.99);

-- Query data
SELECT * FROM products;
```

2. Execute it:
```python
with PostgresManager() as manager:
    manager.execute_from_sql_file('data/your_file.sql')
```

---

## Step 7: Use Examples

### Modify provided examples
1. Open `examples/basic_examples.py`
2. Uncomment the examples you want to run:
```python
if __name__ == "__main__":
    # example_basic_operations()        # Uncomment to run
    # example_from_csv()                # Uncomment to run
    # example_from_dataframe()          # Uncomment to run
    # example_from_json()               # Uncomment to run
    # example_from_sql_file()           # Uncomment to run
```

3. Ensure your data files exist in `data/` directory

4. Run examples:
```bash
python3 examples/basic_examples.py
```

---

## Step 8: Running Tests

```bash
# Install pytest if not already installed
pip install pytest pytest-cov

# Run all tests
python3 -m pytest tests/ -v

# Run with coverage report
python3 -m pytest tests/ --cov=src

# Run specific test
python3 -m pytest tests/test_postgres_manager.py::TestPostgresManager::test_manager_initialization -v
```

---

## Troubleshooting

### "Connection refused" error
**Problem:** PostgreSQL is not running
```bash
# Check if PostgreSQL is running
# macOS:
brew services list | grep postgresql

# Start PostgreSQL if needed:
# macOS:
brew services start postgresql

# Linux:
sudo service postgresql start
```

### "FATAL: password authentication failed"
**Problem:** Wrong credentials in .env
```bash
# Reset PostgreSQL user password (macOS):
sudo -u _postgres psql

# Or create a new user:
createuser -P newuser
createdb -O newuser newdatabase
```

### "database does not exist"
**Problem:** Database specified in .env doesn't exist
```bash
# Create database:
# macOS/Linux:
createdb -U myuser mydatabase

# Or in PostgreSQL prompt:
# CREATE DATABASE mydatabase OWNER myuser;
```

### "ModuleNotFoundError: No module named 'psycopg2'"
**Problem:** Dependencies not installed
```bash
pip install -r requirements.txt
```

### ".env file not found"
**Problem:** Missing .env file
```bash
cp .env.example .env
# Then edit .env with your values
```

---

## Next Steps

1. **Read the documentation:**
   - See [README.md](README.md) for full project overview
   - See [docs/API.md](docs/API.md) for detailed API reference
   - See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for architecture

2. **Try different examples:**
   - Basic CRUD operations
   - CSV import
   - DataFrame operations
   - JSON import
   - SQL file execution

3. **Explore the code:**
   - `src/postgres_manager.py` - Main class
   - `src/readers.py` - Data readers
   - `config/settings.py` - Configuration

4. **Create your own project:**
   - Create a new Python file
   - Import PostgresManager
   - Start building!

---

## Getting Help

- 📖 Read documentation in `docs/` directory
- 🐛 Check error messages in `logs/app.log`
- 💬 Email: your-email@example.com
- 🔗 GitHub: https://github.com/yourusername/pypostgres

---

**Happy coding!** 🚀

For any issues, ensure you're following the setup steps and your .env file is correctly configured.
