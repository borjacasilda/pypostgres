# PyPostgres API Documentation

## PostgresManager Class

### Overview

The `PostgresManager` class is the main interface for interacting with PostgreSQL databases.

### Initialization

```python
from src.postgres_manager import PostgresManager

# Using default configuration from .env
manager = PostgresManager()

# Using custom configuration
config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydb',
    'user': 'myuser',
    'password': 'mypassword'
}
manager = PostgresManager(config=config)
```

### Connection Management

#### `connect() -> bool`

Establish connection to PostgreSQL database.

**Returns**: `True` if connection successful

**Raises**: `psycopg2.Error` if connection fails

**Example**:
```python
manager = PostgresManager()
manager.connect()
# ... perform operations ...
manager.disconnect()
```

#### `disconnect() -> bool`

Close database connection.

**Returns**: `True` if disconnection successful

**Raises**: `psycopg2.Error` if disconnection fails

**Example**:
```python
manager.disconnect()
```

### Context Manager

Use as context manager for automatic connection handling:

```python
with PostgresManager() as manager:
    # Connection opened automatically
    manager.insert('users', {'name': 'John'})
    # Connection closed automatically
```

### Table Operations

#### `create_table(table_name, columns, primary_key=None, if_not_exists=True) -> bool`

Create a new table in the database.

**Parameters**:
- `table_name` (str): Name of the table to create
- `columns` (Dict[str, str]): Dictionary of column_name: data_type pairs
- `primary_key` (str, optional): Primary key column name
- `if_not_exists` (bool): Only create if table doesn't exist (default: True)

**Returns**: `True` if table created successfully

**Raises**: `psycopg2.Error` if table creation fails

**Example**:
```python
columns = {
    'id': 'SERIAL',
    'name': 'VARCHAR(100) NOT NULL',
    'email': 'VARCHAR(100) UNIQUE',
    'age': 'INTEGER',
    'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
}
manager.create_table('users', columns, primary_key='id')
```

#### `drop_table(table_name, if_exists=True) -> bool`

Drop a table from the database.

**Parameters**:
- `table_name` (str): Name of the table to drop
- `if_exists` (bool): Only drop if table exists (default: True)

**Returns**: `True` if table dropped successfully

**Raises**: `psycopg2.Error` if table drop fails

**Example**:
```python
manager.drop_table('users')
```

#### `table_exists(table_name) -> bool`

Check if a table exists in the database.

**Parameters**:
- `table_name` (str): Name of the table

**Returns**: `True` if table exists, `False` otherwise

**Raises**: `psycopg2.Error` if check fails

**Example**:
```python
if manager.table_exists('users'):
    print("Users table exists")
```

#### `get_table_columns(table_name) -> List[Dict[str, str]]`

Get information about table columns.

**Parameters**:
- `table_name` (str): Name of the table

**Returns**: List of column information dictionaries with keys:
- `name` (str): Column name
- `type` (str): Column data type
- `nullable` (bool): Whether column is nullable

**Raises**: `psycopg2.Error` if retrieval fails

**Example**:
```python
columns = manager.get_table_columns('users')
for col in columns:
    print(f"{col['name']}: {col['type']}")
```

### Insert Operations

#### `insert(table_name, data, return_id=False) -> Optional[int]`

Insert a single record into a table.

**Parameters**:
- `table_name` (str): Name of the target table
- `data` (Dict[str, Any]): Dictionary of column_name: value pairs
- `return_id` (bool): Return inserted record's ID (default: False)

**Returns**: The ID of inserted record if return_id=True, else None

**Raises**: `psycopg2.Error` if insertion fails

**Example**:
```python
user_data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': 30
}
manager.insert('users', user_data)

# Get inserted ID
user_id = manager.insert('users', user_data, return_id=True)
```

#### `insert_batch(table_name, data_list, batch_size=None) -> int`

Insert multiple records in batches.

**Parameters**:
- `table_name` (str): Name of the target table
- `data_list` (List[Dict[str, Any]]): List of dictionaries containing row data
- `batch_size` (int, optional): Records per batch (default: MAX_BATCH_SIZE=1000)

**Returns**: Total number of records inserted

**Raises**: `psycopg2.Error` if batch insertion fails

**Example**:
```python
users = [
    {'name': 'Alice', 'email': 'alice@example.com', 'age': 25},
    {'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
    {'name': 'Carol', 'email': 'carol@example.com', 'age': 28},
]
count = manager.insert_batch('users', users, batch_size=1000)
print(f"Inserted {count} records")
```

### Update and Delete Operations

#### `update(table_name, data, where_clause, where_params=None) -> int`

Update records in a table.

**Parameters**:
- `table_name` (str): Name of the target table
- `data` (Dict[str, Any]): Dictionary of column_name: new_value pairs
- `where_clause` (str): WHERE clause for filtering records
- `where_params` (Tuple, optional): Parameters for the WHERE clause

**Returns**: Number of records updated

**Raises**: `psycopg2.Error` if update fails

**Example**:
```python
# Update single record
rows = manager.update(
    'users',
    {'age': 31},
    'id = %s',
    (1,)
)

# Update multiple records
rows = manager.update(
    'users',
    {'status': 'inactive'},
    'age < %s',
    (18,)
)
```

#### `delete(table_name, where_clause, where_params=None) -> int`

Delete records from a table.

**Parameters**:
- `table_name` (str): Name of the target table
- `where_clause` (str): WHERE clause for filtering records
- `where_params` (Tuple, optional): Parameters for the WHERE clause

**Returns**: Number of records deleted

**Raises**: `psycopg2.Error` if delete fails

**Example**:
```python
rows = manager.delete(
    'users',
    'age < %s',
    (18,)
)
print(f"Deleted {rows} records")
```

### Query Operations

#### `query(query_str, params=None, return_df=False) -> Union[List[Tuple], pd.DataFrame]`

Execute a SELECT query and fetch results.

**Parameters**:
- `query_str` (str): SQL SELECT query
- `params` (Tuple, optional): Query parameters
- `return_df` (bool): Return results as DataFrame (default: False)

**Returns**: Query results as list of tuples or DataFrame

**Raises**: `psycopg2.Error` if query fails

**Example**:
```python
# Get results as list of tuples
results = manager.query('SELECT * FROM users WHERE age > %s', params=(25,))

# Get results as DataFrame
df = manager.query(
    'SELECT * FROM users ORDER BY age DESC',
    return_df=True
)
```

### Data Import Operations

#### `insert_from_csv(table_name, csv_path, batch_size=None) -> int`

Insert data from a CSV file.

**Parameters**:
- `table_name` (str): Target table name
- `csv_path` (Union[str, Path]): Path to CSV file
- `batch_size` (int, optional): Batch size for insertion

**Returns**: Number of records inserted

**Raises**: `Exception` if import fails

**Example**:
```python
count = manager.insert_from_csv('products', 'data/products.csv')
```

#### `insert_from_dataframe(table_name, df, batch_size=None) -> int`

Insert data from a pandas DataFrame.

**Parameters**:
- `table_name` (str): Target table name
- `df` (pd.DataFrame): DataFrame to insert
- `batch_size` (int, optional): Batch size for insertion

**Returns**: Number of records inserted

**Raises**: `Exception` if import fails

**Example**:
```python
import pandas as pd

df = pd.read_csv('data.csv')
count = manager.insert_from_dataframe('users', df)
```

#### `insert_from_json(table_name, json_path, batch_size=None) -> int`

Insert data from a JSON file.

**Parameters**:
- `table_name` (str): Target table name
- `json_path` (Union[str, Path]): Path to JSON file
- `batch_size` (int, optional): Batch size for insertion

**Returns**: Number of records inserted

**Raises**: `Exception` if import fails

**Example**:
```python
count = manager.insert_from_json('employees', 'data/employees.json')
```

#### `insert_from_excel(table_name, excel_path, sheet_name=0, batch_size=None) -> int`

Insert data from an Excel file.

**Parameters**:
- `table_name` (str): Target table name
- `excel_path` (Union[str, Path]): Path to Excel file
- `sheet_name` (Union[str, int]): Sheet name or index (default: 0)
- `batch_size` (int, optional): Batch size for insertion

**Returns**: Number of records inserted

**Raises**: `Exception` if import fails

**Example**:
```python
count = manager.insert_from_excel(
    'users',
    'data/users.xlsx',
    sheet_name='Sheet1'
)
```

#### `execute_from_sql_file(file_path) -> List[Any]`

Execute SQL statements from a file.

**Parameters**:
- `file_path` (Union[str, Path]): Path to SQL file

**Returns**: Results from the last SELECT statement

**Raises**: `Exception` if execution fails

**Example**:
```python
results = manager.execute_from_sql_file('scripts/init.sql')
```

## Data Readers

### ReaderFactory

Automatically selects the appropriate reader based on file extension.

#### `get_reader(file_path) -> BaseReader`

Get appropriate reader for file type.

**Parameters**:
- `file_path` (Union[str, Path]): Path to file

**Returns**: Appropriate reader instance

**Raises**: `ValueError` if file type is not supported

#### `read_file(file_path) -> Union[pd.DataFrame, str, List]`

Read file with appropriate reader.

**Parameters**:
- `file_path` (Union[str, Path]): Path to file

**Returns**: Parsed data

**Supported formats**:
- `.csv`: Returns pandas DataFrame
- `.json`: Returns dict or list
- `.sql`: Returns list of SQL statements
- `.pdf`: Returns extracted text
- `.xlsx`, `.xls`: Returns pandas DataFrame

**Example**:
```python
from src.readers import ReaderFactory

# Automatically determines reader type
data = ReaderFactory.read_file('data/users.csv')
```

## Logging

The logger is automatically configured on module import. Access it in your code:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("This is an info message")
logger.error("This is an error message")
```

### Configuration

Configure via `.env`:
```env
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Log Levels

- `DEBUG`: Detailed information for debugging
- `INFO`: General informational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical messages

---

**Version**: 1.0.0
**Last Updated**: 2026-02-08
