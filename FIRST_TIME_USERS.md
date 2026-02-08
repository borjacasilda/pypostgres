# FIRST TIME USERS - READ THIS!

Welcome to PyPostgres! This guide will help you get started.

## Step 1: What You Need

- ✓ Python 3.8+ installed
- ✓ PostgreSQL installed and running
- ✓ A PostgreSQL database created
- ✓ A database user created

If you don't have these, see the installation section below.

## Step 2: Get the Code

```bash
git clone https://github.com/yourusername/pypostgres.git
cd pypostgres
pip install -r requirements.txt
```

## Step 3: Configure Your Database (IMPORTANT!)

```bash
cp .env.example .env
```

Edit `.env` and change these values to YOUR database credentials:

```env
DB_HOST=localhost          # Your database server
DB_PORT=5432              # Your database port
DB_NAME=your_database     # <-- CHANGE THIS
DB_USER=your_user         # <-- CHANGE THIS
DB_PASSWORD=your_password # <-- CHANGE THIS
```

**Example if you just installed PostgreSQL:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres  # Or whatever password you set
```

## Step 4: Test Your Setup

Create a file called `test_setup.py`:

```python
from src.postgres_manager import PostgresManager

try:
    with PostgresManager() as manager:
        print("✓ Connection successful!")
        print("✓ You're ready to use PyPostgres!")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    print("✗ Check your .env file and PostgreSQL settings")
```

Run it:
```bash
python3 test_setup.py
```

You should see: `✓ Connection successful!`

## Step 5: Try a Simple Example

Create a file called `my_first_app.py`:

```python
from src.postgres_manager import PostgresManager

# Create a table
columns = {
    'id': 'SERIAL',
    'name': 'VARCHAR(100)',
    'age': 'INTEGER'
}

with PostgresManager() as manager:
    # Create table
    manager.create_table('people', columns, primary_key='id')
    print("✓ Table created")
    
    # Insert data
    manager.insert('people', {'name': 'Alice', 'age': 25})
    manager.insert('people', {'name': 'Bob', 'age': 30})
    print("✓ Data inserted")
    
    # Read data
    results = manager.query('SELECT * FROM people')
    print(f"✓ Found {len(results)} people:")
    for row in results:
        print(f"  - {row}")
```

Run it:
```bash
python3 my_first_app.py
```

## Step 6: Explore Examples

Look at `examples/basic_examples.py` for more examples.

Each example shows how to:
- Create tables
- Insert data (single, batch, from CSV/JSON)
- Query data
- Update/delete records

## Need Help?

### Issue: "Connection refused"
- Check if PostgreSQL is running
- On macOS: `brew services start postgresql`
- On Linux: `sudo service postgresql start`

### Issue: "password authentication failed"
- Check the password in .env is correct
- Reset it with: `sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'newpassword';"`

### Issue: "database does not exist"
- Create it: `createdb -U postgres mydatabase`
- Or use PostgreSQL admin tool (pgAdmin)

### Issue: "ModuleNotFoundError"
- Install dependencies: `pip install -r requirements.txt`

### Issue: "No module named 'psycopg2'"
- Install it: `pip install psycopg2-binary`

## Understanding the Project Structure

```
pypostgres/
├── src/
│   ├── postgres_manager.py    ← Main class
│   ├── readers.py             ← Read CSV/JSON/Excel
│   └── logger.py              ← Logging setup
├── examples/
│   └── basic_examples.py      ← Example code
├── data/                      ← Put your CSV/JSON files here
├── docs/
│   ├── API.md                 ← All methods explained
│   └── ARCHITECTURE.md        ← How it works
├── .env                       ← YOUR config (don't share this!)
├── .env.example               ← Template (safe to share)
├── README.md                  ← Full documentation
├── SETUP.md                   ← Detailed setup guide
└── QUICKSTART.md              ← Quick reference
```

## Common Tasks

### Task 1: Insert data from a CSV file

1. Create a CSV file in `data/` directory (e.g., `data/products.csv`):
   ```
   name,price
   Laptop,999.99
   Mouse,29.99
   ```

2. Create a Python script:
   ```python
   from src.postgres_manager import PostgresManager
   
   with PostgresManager() as manager:
       # Create table
       columns = {
           'id': 'SERIAL',
           'name': 'VARCHAR(100)',
           'price': 'DECIMAL(10, 2)'
       }
       manager.create_table('products', columns, primary_key='id')
       
       # Insert from CSV
       count = manager.insert_from_csv('products', 'data/products.csv')
       print(f"Inserted {count} products")
   ```

### Task 2: Query data as a DataFrame

```python
from src.postgres_manager import PostgresManager
import pandas as pd

with PostgresManager() as manager:
    df = manager.query(
        'SELECT * FROM products WHERE price > %s',
        params=(100,),
        return_df=True
    )
    print(df)
    # You can now use pandas to analyze the data
    print(f"Average price: {df['price'].mean()}")
```

### Task 3: Update existing records

```python
with PostgresManager() as manager:
    manager.update(
        'products',
        {'price': 899.99},
        'name = %s',
        ('Laptop',)
    )
    print("Price updated!")
```

### Task 4: Delete old records

```python
with PostgresManager() as manager:
    deleted = manager.delete(
        'products',
        'price < %s',
        (50,)
    )
    print(f"Deleted {deleted} cheap products")
```

## Next Steps

1. **Read [SETUP.md](SETUP.md)** for detailed setup instructions
2. **Read [QUICKSTART.md](QUICKSTART.md)** for quick reference
3. **Check [docs/API.md](docs/API.md)** for all available methods
4. **Explore [examples/basic_examples.py](examples/basic_examples.py)** for more examples

## Key Points to Remember

✓ Always use context manager: `with PostgresManager() as manager:`
✓ Use parameterized queries: `query('WHERE id = %s', params=(1,))`
✓ Never put your .env in git (it's in .gitignore)
✓ Check logs: `tail -f logs/app.log` for debugging
✓ Read error messages carefully - they usually tell you what's wrong

## Questions?

- 📖 Read the docs in `docs/` directory
- 🐛 Check the logs: `logs/app.log`
- 💬 Email: your-email@example.com
- 🔗 GitHub: https://github.com/yourusername/pypostgres

---

**You're all set! Start building!** 🚀
