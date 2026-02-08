"""
Main PostgreSQL Manager class for PyPostgres.

This module provides the PostgresManager class which handles all PostgreSQL
database operations including CRUD operations, table management, and bulk imports.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple

import pandas as pd
import psycopg2
from psycopg2 import sql, Error

from src.readers import ReaderFactory, SQLReader
from config.settings import DB_CONFIG, MAX_BATCH_SIZE

logger = logging.getLogger(__name__)


class PostgresManager:
    """
    A professional PostgreSQL database manager.

    Provides methods for common database operations:
    - CRUD operations (Create, Read, Update, Delete)
    - Table management (create, drop, alter)
    - Bulk operations from various data sources
    - Query execution from multiple formats

    Attributes:
        config (dict): Database connection configuration
        connection: Active database connection
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize PostgresManager.

        Args:
            config: Database configuration dict. If None, uses settings from config/settings.py

        Raises:
            TypeError: If config is not a dict or None
        """
        if config is None:
            config = DB_CONFIG
        if not isinstance(config, dict):
            raise TypeError("Configuration must be a dictionary")

        self.config = config
        self.connection = None
        logger.info("PostgresManager initialized")

    def connect(self) -> bool:
        """
        Establish connection to PostgreSQL database.

        Returns:
            True if connection successful, False otherwise

        Raises:
            Error: If connection fails
        """
        try:
            self.connection = psycopg2.connect(**self.config)
            logger.info(f"Connected to database: {self.config.get('database')}")
            return True
        except Error as e:
            logger.error(f"Connection failed: {str(e)}")
            raise

    def disconnect(self) -> bool:
        """
        Close database connection.

        Returns:
            True if disconnection successful
        """
        try:
            if self.connection:
                self.connection.close()
                logger.info("Disconnected from database")
                return True
        except Error as e:
            logger.error(f"Disconnection error: {str(e)}")
            raise

    def _execute_query(
        self,
        query: str,
        params: Optional[Tuple] = None,
        fetch: bool = False,
        fetch_one: bool = False,
        commit: bool = True,
    ) -> Optional[Union[List, Dict, Any]]:
        """
        Execute a query against the database.

        Args:
            query: SQL query string
            params: Query parameters for parameterized queries
            fetch: Whether to fetch all results
            fetch_one: Whether to fetch only one result
            commit: Whether to commit changes

        Returns:
            Query results or None

        Raises:
            Error: If query execution fails
        """
        cursor = None
        try:
            if not self.connection:
                raise Error("Not connected to database")

            cursor = self.connection.cursor()
            cursor.execute(query, params)

            if fetch:
                results = cursor.fetchall()
                logger.debug(f"Fetched {len(results) if results else 0} rows")
                return results
            elif fetch_one:
                return cursor.fetchone()

            if commit:
                self.connection.commit()
                logger.debug("Query executed and committed")

            return None

        except Error as e:
            if self.connection:
                self.connection.rollback()
            logger.error(f"Query execution failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()

    def create_table(
        self,
        table_name: str,
        columns: Dict[str, str],
        primary_key: Optional[str] = None,
        if_not_exists: bool = True,
    ) -> bool:
        """
        Create a new table in the database.

        Args:
            table_name: Name of the table to create
            columns: Dictionary of column_name: data_type pairs
            primary_key: Optional primary key column name
            if_not_exists: If True, only create if table doesn't exist

        Returns:
            True if table created successfully

        Example:
            columns = {
                'id': 'SERIAL',
                'name': 'VARCHAR(100)',
                'email': 'VARCHAR(100)',
                'created_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
            }
            manager.create_table('users', columns, primary_key='id')
        """
        try:
            column_defs = []
            for col_name, col_type in columns.items():
                col_def = f"{col_name} {col_type}"
                if primary_key and col_name == primary_key:
                    col_def += " PRIMARY KEY"
                column_defs.append(col_def)

            columns_str = ", ".join(column_defs)
            if_not_exists_str = "IF NOT EXISTS" if if_not_exists else ""

            query = f"CREATE TABLE {if_not_exists_str} {table_name} ({columns_str})"

            self._execute_query(query, commit=True)
            logger.info(f"Table '{table_name}' created successfully")
            return True

        except Error as e:
            logger.error(f"Failed to create table '{table_name}': {str(e)}")
            raise

    def drop_table(self, table_name: str, if_exists: bool = True) -> bool:
        """
        Drop a table from the database.

        Args:
            table_name: Name of the table to drop
            if_exists: If True, only drop if table exists

        Returns:
            True if table dropped successfully
        """
        try:
            if_exists_str = "IF EXISTS" if if_exists else ""
            query = f"DROP TABLE {if_exists_str} {table_name}"
            self._execute_query(query, commit=True)
            logger.info(f"Table '{table_name}' dropped successfully")
            return True

        except Error as e:
            logger.error(f"Failed to drop table '{table_name}': {str(e)}")
            raise

    def insert(
        self,
        table_name: str,
        data: Dict[str, Any],
        return_id: bool = False,
    ) -> Optional[int]:
        """
        Insert a single record into a table.

        Args:
            table_name: Name of the target table
            data: Dictionary of column_name: value pairs
            return_id: If True, return the inserted record's ID

        Returns:
            The ID of inserted record if return_id=True, else None

        Example:
            data = {'name': 'John', 'email': 'john@example.com'}
            manager.insert('users', data)
        """
        try:
            columns = list(data.keys())
            values = list(data.values())
            placeholders = ", ".join(["%s"] * len(values))
            cols_str = ", ".join(columns)

            query = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"
            if return_id:
                query += " RETURNING id"

            result = self._execute_query(
                query, params=tuple(values), fetch_one=return_id, commit=True
            )

            if return_id and result:
                logger.info(f"Record inserted into '{table_name}' with ID: {result[0]}")
                return result[0]
            else:
                logger.info(f"Record inserted into '{table_name}'")
                return None

        except Error as e:
            logger.error(f"Failed to insert into '{table_name}': {str(e)}")
            raise

    def insert_batch(
        self,
        table_name: str,
        data_list: List[Dict[str, Any]],
        batch_size: Optional[int] = None,
    ) -> int:
        """
        Insert multiple records in batches.

        Args:
            table_name: Name of the target table
            data_list: List of dictionaries containing row data
            batch_size: Number of records per batch (default: MAX_BATCH_SIZE)

        Returns:
            Total number of records inserted

        Example:
            data = [
                {'name': 'John', 'email': 'john@example.com'},
                {'name': 'Jane', 'email': 'jane@example.com'}
            ]
            manager.insert_batch('users', data)
        """
        if not data_list:
            logger.warning("Empty data list provided for batch insert")
            return 0

        if batch_size is None:
            batch_size = MAX_BATCH_SIZE

        try:
            total_inserted = 0

            for i in range(0, len(data_list), batch_size):
                batch = data_list[i : i + batch_size]

                columns = list(batch[0].keys())
                placeholders = ", ".join(["%s"] * len(columns))
                cols_str = ", ".join(columns)

                query = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"

                cursor = self.connection.cursor()
                values = [tuple(row[col] for col in columns) for row in batch]
                cursor.executemany(query, values)
                self.connection.commit()

                total_inserted += len(batch)
                logger.info(
                    f"Batch inserted: {len(batch)} records into '{table_name}'"
                )
                cursor.close()

            logger.info(
                f"Batch insert completed: {total_inserted} total records into '{table_name}'"
            )
            return total_inserted

        except Error as e:
            logger.error(f"Batch insert failed for '{table_name}': {str(e)}")
            raise

    def update(
        self,
        table_name: str,
        data: Dict[str, Any],
        where_clause: str,
        where_params: Optional[Tuple] = None,
    ) -> int:
        """
        Update records in a table.

        Args:
            table_name: Name of the target table
            data: Dictionary of column_name: new_value pairs
            where_clause: WHERE clause for filtering records
            where_params: Parameters for the WHERE clause

        Returns:
            Number of records updated

        Example:
            manager.update(
                'users',
                {'email': 'newemail@example.com'},
                'id = %s',
                (1,)
            )
        """
        try:
            set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
            values = list(data.values())
            if where_params:
                values.extend(where_params)

            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            cursor = self.connection.cursor()
            cursor.execute(query, tuple(values))
            self.connection.commit()
            rows_affected = cursor.rowcount
            cursor.close()

            logger.info(f"Updated {rows_affected} records in '{table_name}'")
            return rows_affected

        except Error as e:
            logger.error(f"Update failed for '{table_name}': {str(e)}")
            raise

    def delete(
        self,
        table_name: str,
        where_clause: str,
        where_params: Optional[Tuple] = None,
    ) -> int:
        """
        Delete records from a table.

        Args:
            table_name: Name of the target table
            where_clause: WHERE clause for filtering records
            where_params: Parameters for the WHERE clause

        Returns:
            Number of records deleted

        Example:
            manager.delete('users', 'id = %s', (1,))
        """
        try:
            query = f"DELETE FROM {table_name} WHERE {where_clause}"

            cursor = self.connection.cursor()
            cursor.execute(query, where_params)
            self.connection.commit()
            rows_affected = cursor.rowcount
            cursor.close()

            logger.info(f"Deleted {rows_affected} records from '{table_name}'")
            return rows_affected

        except Error as e:
            logger.error(f"Delete failed for '{table_name}': {str(e)}")
            raise

    def query(
        self,
        query_str: str,
        params: Optional[Tuple] = None,
        return_df: bool = False,
    ) -> Union[List[Tuple], pd.DataFrame]:
        """
        Execute a SELECT query and fetch results.

        Args:
            query_str: SQL SELECT query
            params: Query parameters
            return_df: If True, return results as DataFrame

        Returns:
            Query results as list of tuples or DataFrame

        Example:
            results = manager.query('SELECT * FROM users WHERE id = %s', (1,))
        """
        try:
            results = self._execute_query(
                query_str, params=params, fetch=True, commit=False
            )

            if return_df:
                columns = [desc[0] for desc in self.connection.cursor().description] if results else []
                df = pd.DataFrame(results, columns=columns)
                logger.info(f"Query returned {len(df)} rows as DataFrame")
                return df
            else:
                logger.info(f"Query returned {len(results) if results else 0} rows")
                return results or []

        except Error as e:
            logger.error(f"Query failed: {str(e)}")
            raise

    def execute_from_sql_file(self, file_path: Union[str, Path]) -> List[Any]:
        """
        Execute SQL statements from a file.

        Args:
            file_path: Path to SQL file

        Returns:
            Results from the last SELECT statement

        Example:
            manager.execute_from_sql_file('scripts/init.sql')
        """
        try:
            reader = SQLReader()
            statements = reader.read(file_path)

            results = None
            for statement in statements:
                if statement.upper().startswith("SELECT"):
                    results = self._execute_query(
                        statement, fetch=True, commit=False
                    )
                else:
                    self._execute_query(statement, commit=True)

            logger.info(f"Executed SQL file: {file_path}")
            return results or []

        except Exception as e:
            logger.error(f"Failed to execute SQL file '{file_path}': {str(e)}")
            raise

    def insert_from_csv(
        self,
        table_name: str,
        csv_path: Union[str, Path],
        batch_size: Optional[int] = None,
    ) -> int:
        """
        Insert data from a CSV file.

        Args:
            table_name: Target table name
            csv_path: Path to CSV file
            batch_size: Batch size for insertion

        Returns:
            Number of records inserted

        Example:
            manager.insert_from_csv('users', 'data/users.csv')
        """
        try:
            df = ReaderFactory.read_file(csv_path)
            data_list = df.to_dict("records")
            count = self.insert_batch(table_name, data_list, batch_size)
            logger.info(f"Inserted {count} records from CSV: {csv_path}")
            return count

        except Exception as e:
            logger.error(
                f"Failed to insert from CSV '{csv_path}' to '{table_name}': {str(e)}"
            )
            raise

    def insert_from_dataframe(
        self,
        table_name: str,
        df: pd.DataFrame,
        batch_size: Optional[int] = None,
    ) -> int:
        """
        Insert data from a pandas DataFrame.

        Args:
            table_name: Target table name
            df: DataFrame to insert
            batch_size: Batch size for insertion

        Returns:
            Number of records inserted

        Example:
            df = pd.read_csv('data.csv')
            manager.insert_from_dataframe('users', df)
        """
        try:
            if df.empty:
                logger.warning("Empty DataFrame provided")
                return 0

            data_list = df.to_dict("records")
            count = self.insert_batch(table_name, data_list, batch_size)
            logger.info(f"Inserted {count} records from DataFrame into '{table_name}'")
            return count

        except Exception as e:
            logger.error(
                f"Failed to insert from DataFrame to '{table_name}': {str(e)}"
            )
            raise

    def insert_from_json(
        self,
        table_name: str,
        json_path: Union[str, Path],
        batch_size: Optional[int] = None,
    ) -> int:
        """
        Insert data from a JSON file.

        Args:
            table_name: Target table name
            json_path: Path to JSON file
            batch_size: Batch size for insertion

        Returns:
            Number of records inserted

        Example:
            manager.insert_from_json('users', 'data/users.json')
        """
        try:
            from src.readers import JSONReader

            reader = JSONReader()
            data = reader.read(json_path)

            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                raise ValueError("JSON must contain a list or dict")

            count = self.insert_batch(table_name, data, batch_size)
            logger.info(f"Inserted {count} records from JSON: {json_path}")
            return count

        except Exception as e:
            logger.error(
                f"Failed to insert from JSON '{json_path}' to '{table_name}': {str(e)}"
            )
            raise

    def insert_from_excel(
        self,
        table_name: str,
        excel_path: Union[str, Path],
        sheet_name: Union[str, int] = 0,
        batch_size: Optional[int] = None,
    ) -> int:
        """
        Insert data from an Excel file.

        Args:
            table_name: Target table name
            excel_path: Path to Excel file
            sheet_name: Sheet name or index
            batch_size: Batch size for insertion

        Returns:
            Number of records inserted

        Example:
            manager.insert_from_excel('users', 'data/users.xlsx', sheet_name='Sheet1')
        """
        try:
            from src.readers import ExcelReader

            reader = ExcelReader()
            df = reader.read(excel_path, sheet_name=sheet_name)
            count = self.insert_batch(table_name, df.to_dict("records"), batch_size)
            logger.info(
                f"Inserted {count} records from Excel: {excel_path} (sheet: {sheet_name})"
            )
            return count

        except Exception as e:
            logger.error(
                f"Failed to insert from Excel '{excel_path}' to '{table_name}': {str(e)}"
            )
            raise

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.

        Args:
            table_name: Name of the table

        Returns:
            True if table exists, False otherwise
        """
        try:
            query = """
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables 
                    WHERE table_name = %s
                )
            """
            result = self._execute_query(
                query, params=(table_name,), fetch_one=True, commit=False
            )
            exists = result[0] if result else False
            logger.debug(f"Table '{table_name}' exists: {exists}")
            return exists

        except Error as e:
            logger.error(f"Failed to check table existence: {str(e)}")
            raise

    def get_table_columns(self, table_name: str) -> List[Dict[str, str]]:
        """
        Get information about table columns.

        Args:
            table_name: Name of the table

        Returns:
            List of column information dictionaries

        Example:
            columns = manager.get_table_columns('users')
        """
        try:
            query = """
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """
            results = self._execute_query(
                query, params=(table_name,), fetch=True, commit=False
            )

            columns = [
                {
                    "name": row[0],
                    "type": row[1],
                    "nullable": row[2] == "YES",
                }
                for row in results
            ]

            logger.info(f"Retrieved {len(columns)} columns for table '{table_name}'")
            return columns

        except Error as e:
            logger.error(f"Failed to get table columns: {str(e)}")
            raise

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
