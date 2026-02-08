"""
Example usage of PyPostgres library.

This module demonstrates how to use the PostgresManager class for common operations.

IMPORTANT: Before running these examples, ensure:
1. PostgreSQL is installed and running
2. You have created a database and user
3. You have configured .env file with your credentials
4. You have uncommented the example functions you want to run in the __main__ block

For setup instructions, see SETUP.md
"""

import logging
import pandas as pd
from pathlib import Path

# Setup logging
from src.logger import setup_logging
setup_logging()

from src.postgres_manager import PostgresManager

logger = logging.getLogger(__name__)


def example_basic_operations():
    """
    Example 1: Basic CRUD operations
    
    BEFORE RUNNING THIS EXAMPLE:
    - Ensure PostgreSQL is running
    - Ensure .env is configured with your database credentials
    - The database specified in .env must exist
    """
    logger.info("=" * 50)
    logger.info("EXAMPLE 1: Basic CRUD Operations")
    logger.info("=" * 50)

    # Initialize manager using context manager (recommended)
    with PostgresManager() as manager:
        # Create table
        columns = {
            "id": "SERIAL",
            "name": "VARCHAR(100) NOT NULL",
            "email": "VARCHAR(100) UNIQUE",
            "age": "INTEGER",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        }
        manager.create_table("users", columns, primary_key="id")

        # Insert single record
        user_data = {"name": "John Doe", "email": "john@example.com", "age": 30}
        manager.insert("users", user_data)

        # Insert multiple records
        users_batch = [
            {"name": "Jane Smith", "email": "jane@example.com", "age": 28},
            {"name": "Bob Johnson", "email": "bob@example.com", "age": 35},
            {"name": "Alice Brown", "email": "alice@example.com", "age": 26},
        ]
        manager.insert_batch("users", users_batch)

        # Query all users
        results = manager.query("SELECT * FROM users")
        logger.info(f"All users: {results}")

        # Update a record
        manager.update("users", {"age": 31}, "name = %s", ("John Doe",))

        # Delete a record
        manager.delete("users", "name = %s", ("Bob Johnson",))

        # Query with DataFrame
        df = manager.query("SELECT * FROM users ORDER BY age", return_df=True)
        logger.info(f"\nUsers DataFrame:\n{df}")


def example_from_csv():
    """
    Example 2: Insert data from CSV file
    
    BEFORE RUNNING THIS EXAMPLE:
    - Create a CSV file in data/ directory with your own data
    - File format: columns should match your database table
    - Example CSV structure:
        product_name,price,stock
        Laptop,999.99,10
        Mouse,29.99,50
    """
    logger.info("=" * 50)
    logger.info("EXAMPLE 2: Insert from CSV")
    logger.info("=" * 50)

    with PostgresManager() as manager:
        # Path to your CSV file
        # TODO: Replace with your actual CSV file path
        sample_csv = Path("data/products.csv")
        
        # Check if file exists
        if not sample_csv.exists():
            logger.warning(f"CSV file not found: {sample_csv}")
            logger.info("To use this example, create a CSV file with your data")
            logger.info("CSV format: comma-separated values with header row")
            return

        # Create table for products
        columns = {
            "id": "SERIAL",
            "product_name": "VARCHAR(100)",
            "price": "DECIMAL(10, 2)",
            "stock": "INTEGER",
        }
        manager.create_table("products", columns, primary_key="id", if_not_exists=True)

        # Insert from CSV
        count = manager.insert_from_csv("products", sample_csv)
        logger.info(f"Inserted {count} products from CSV")

        # Verify
        products = manager.query("SELECT * FROM products", return_df=True)
        logger.info(f"\nProducts:\n{products}")


def example_from_dataframe():
    """
    Example 3: Insert data from DataFrame
    
    BEFORE RUNNING THIS EXAMPLE:
    - Create your own DataFrame with appropriate data
    - Ensure column names match your database table
    - Example:
        df = pd.DataFrame({
            'order_id': [1001, 1002, 1003],
            'customer_name': ['Alice', 'Bob', 'Carol'],
            'amount': [150.50, 200.00, 75.25]
        })
    """
    logger.info("=" * 50)
    logger.info("EXAMPLE 3: Insert from DataFrame")
    logger.info("=" * 50)

    with PostgresManager() as manager:
        # TODO: Replace with your own DataFrame data
        # Example: Load data from your own source
        df = pd.DataFrame(
            {
                "order_id": [1001, 1002, 1003, 1004],
                "customer_name": ["Alice", "Bob", "Carol", "David"],
                "amount": [150.50, 200.00, 75.25, 320.75],
            }
        )

        # Create table
        columns = {
            "id": "SERIAL",
            "order_id": "INTEGER",
            "customer_name": "VARCHAR(100)",
            "amount": "DECIMAL(10, 2)",
        }
        manager.create_table("orders", columns, primary_key="id", if_not_exists=True)

        # Insert from DataFrame
        count = manager.insert_from_dataframe("orders", df)
        logger.info(f"Inserted {count} orders from DataFrame")

        # Query and verify
        orders = manager.query(
            "SELECT * FROM orders WHERE amount > %s ORDER BY amount DESC",
            params=(100,),
            return_df=True,
        )
        logger.info(f"\nOrders over $100:\n{orders}")


def example_from_json():
    """
    Example 4: Insert data from JSON file
    
    BEFORE RUNNING THIS EXAMPLE:
    - Create your own JSON file in data/ directory
    - File must contain a list of objects or a single object
    - Example JSON format:
        [
            {
                "emp_id": 101,
                "name": "John Smith",
                "department": "IT",
                "salary": 75000
            },
            {
                "emp_id": 102,
                "name": "Sarah Johnson",
                "department": "HR",
                "salary": 65000
            }
        ]
    """
    logger.info("=" * 50)
    logger.info("EXAMPLE 4: Insert from JSON")
    logger.info("=" * 50)

    with PostgresManager() as manager:
        # TODO: Replace with your actual JSON file path
        sample_json = Path("data/employees.json")
        
        if not sample_json.exists():
            logger.warning(f"JSON file not found: {sample_json}")
            logger.info("To use this example, create a JSON file with your data")
            logger.info("JSON format: array of objects with matching column names")
            return

        # Create table
        columns = {
            "id": "SERIAL",
            "emp_id": "INTEGER",
            "name": "VARCHAR(100)",
            "department": "VARCHAR(50)",
            "salary": "DECIMAL(10, 2)",
        }
        manager.create_table(
            "employees", columns, primary_key="id", if_not_exists=True
        )

        # Insert from JSON
        count = manager.insert_from_json("employees", sample_json)
        logger.info(f"Inserted {count} employees from JSON")

        # Query
        result = manager.query(
            "SELECT * FROM employees ORDER BY salary DESC",
            return_df=True,
        )
        logger.info(f"\nEmployees:\n{result}")


def example_from_sql_file():
    """
    Example 5: Execute SQL from file
    
    BEFORE RUNNING THIS EXAMPLE:
    - Create your own SQL file in data/ directory
    - File should contain valid SQL statements
    - Example SQL file format:
        SELECT * FROM users WHERE age > 25;
        SELECT COUNT(*) as total_users FROM users;
        SELECT name, email FROM users ORDER BY name;
    """
    logger.info("=" * 50)
    logger.info("EXAMPLE 5: Execute from SQL File")
    logger.info("=" * 50)

    with PostgresManager() as manager:
        # TODO: Replace with your actual SQL file path
        sample_sql = Path("data/sample_queries.sql")
        
        if not sample_sql.exists():
            logger.warning(f"SQL file not found: {sample_sql}")
            logger.info("To use this example, create a SQL file with your queries")
            logger.info("SQL format: valid SQL statements separated by semicolons")
            return

        # Execute SQL file
        results = manager.execute_from_sql_file(sample_sql)
        logger.info(f"Executed SQL file, results: {results}")


def example_context_manager():
    """
    Example 6: Using context manager for automatic connection handling
    """
    logger.info("=" * 50)
    logger.info("EXAMPLE 6: Context Manager Usage")
    logger.info("=" * 50)

    # Connection and disconnection handled automatically
    with PostgresManager() as manager:
        # All operations here
        result = manager.query("SELECT version()")
        logger.info(f"Database version: {result}")


def example_table_inspection():
    """
    Example 7: Inspect table structure
    """
    logger.info("=" * 50)
    logger.info("EXAMPLE 7: Table Inspection")
    logger.info("=" * 50)

    with PostgresManager() as manager:
        # Check if table exists
        exists = manager.table_exists("users")
        logger.info(f"Table 'users' exists: {exists}")

        if exists:
            # Get column information
            columns = manager.get_table_columns("users")
            logger.info(f"\nTable 'users' columns:")
            for col in columns:
                logger.info(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")


if __name__ == "__main__":
    try:
        logger.info("Starting PyPostgres Examples")
        logger.info("=" * 50)
        logger.info("")
        logger.info("IMPORTANT: Before running any example:")
        logger.info("1. Ensure PostgreSQL is installed and running")
        logger.info("2. Edit .env with your database credentials")
        logger.info("3. The database specified in .env must exist")
        logger.info("4. For CSV/JSON/SQL examples: create your data files in data/")
        logger.info("")
        logger.info("See SETUP.md for detailed setup instructions")
        logger.info("=" * 50)
        logger.info("")

        # Uncomment the examples you want to run:
        # example_basic_operations()
        # example_from_csv()
        # example_from_dataframe()
        # example_from_json()
        # example_from_sql_file()
        # example_context_manager()
        # example_table_inspection()

        logger.info("")
        logger.info("=" * 50)
        logger.info("Example templates ready. Edit and uncomment to run.")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
