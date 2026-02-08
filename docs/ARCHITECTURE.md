# PyPostgres Architecture

## Overview

PyPostgres is designed as a lightweight, professional wrapper around psycopg2 with focus on usability, flexibility, and maintainability.

## Design Principles

1. **Simplicity**: Provide a clean, Pythonic API
2. **Flexibility**: Support multiple data formats and use cases
3. **Reliability**: Comprehensive error handling and logging
4. **Performance**: Efficient batch operations and connection management
5. **Maintainability**: Well-documented, type-hinted code

## Component Architecture

```
┌─────────────────────────────────────────────┐
│         Application Layer                   │
│  (User Code, Examples, Tests)               │
└────────────┬────────────────────────────────┘
             │
┌────────────▼────────────────────────────────┐
│      PostgresManager (Main Interface)       │
│  - CRUD Operations                          │
│  - Table Management                         │
│  - Data Import/Export                       │
└────────────┬──────────────┬─────────────────┘
             │              │
    ┌────────▼──────────┐   │
    │  Data Readers     │   │
    │  - CSVReader      │   │
    │  - JSONReader     │   │
    │  - SQLReader      │   │
    │  - PDFReader      │   │
    │  - ExcelReader    │   │
    └───────────────────┘   │
                            │
                    ┌───────▼──────────┐
                    │  Logger Module   │
                    │  (Logging Setup) │
                    └──────────────────┘
                            │
┌───────────────────────────▼──────────────┐
│  Configuration Module                    │
│  - Database Settings                     │
│  - Logging Configuration                 │
│  - Environment Variables                 │
└────────────────────────────┬─────────────┘
                             │
                    ┌────────▼──────────┐
                    │   psycopg2        │
                    │  (Database Driver)│
                    └───────────────────┘
                             │
                    ┌────────▼──────────┐
                    │  PostgreSQL DB    │
                    │  (Database Server)│
                    └───────────────────┘
```

## Module Descriptions

### `src/postgres_manager.py`

**Purpose**: Main interface for database operations

**Key Classes**:
- `PostgresManager`: Main manager class for all database operations

**Key Methods**:
- Connection management: `connect()`, `disconnect()`
- Table operations: `create_table()`, `drop_table()`, `table_exists()`
- CRUD operations: `insert()`, `update()`, `delete()`, `query()`
- Batch operations: `insert_batch()`
- Data import: `insert_from_csv()`, `insert_from_dataframe()`, `insert_from_json()`, `insert_from_excel()`
- Query execution: `execute_from_sql_file()`
- Inspection: `get_table_columns()`

### `src/readers.py`

**Purpose**: Handle reading data from multiple formats

**Key Classes**:
- `BaseReader`: Abstract base class for all readers
- `CSVReader`: Read CSV files using pandas
- `JSONReader`: Read JSON files
- `SQLReader`: Parse SQL files into individual statements
- `PDFReader`: Extract text from PDF files
- `ExcelReader`: Read Excel spreadsheets
- `DataFrameReader`: Handle pandas DataFrames
- `ReaderFactory`: Factory pattern for reader selection

**Design Pattern**: Factory pattern for automatic reader selection based on file extension

### `src/logger.py`

**Purpose**: Configure and manage application logging

**Key Functions**:
- `setup_logging()`: Initialize logging system based on configuration

**Features**:
- Console and file output
- Rotating file handler
- Configurable log levels
- Detailed formatting with timestamps

### `config/settings.py`

**Purpose**: Centralized configuration management

**Key Components**:
- Environment variable loading via `.env`
- Database configuration dictionary
- Logging configuration (Python logging dict format)
- Application settings (batch size, timeout, etc.)

### `src/__init__.py`

**Purpose**: Package initialization and public API

**Exports**:
- `PostgresManager`: Main class

## Data Flow

### Insert from CSV Flow

```
CSV File
    │
    ▼
CSVReader (reads file)
    │
    ▼
pandas DataFrame
    │
    ▼
PostgresManager.insert_batch()
    │
    ▼
Batch Processing (split into chunks)
    │
    ▼
psycopg2 cursor.executemany()
    │
    ▼
PostgreSQL Database
    │
    ▼
Logging & Return count
```

### CRUD Operation Flow

```
User Code
    │
    ▼
PostgresManager.method()
    │
    ▼
Connection Check
    │
    ▼
_execute_query() helper
    │
    ▼
psycopg2 cursor
    │
    ▼
PostgreSQL Database
    │
    ▼
Error Handling & Logging
    │
    ▼
Return Results
```

## Connection Management

The library uses context manager pattern for safe connection handling:

```python
with PostgresManager(config) as manager:
    # Connection opened
    manager.insert('table', data)
    # Connection closed automatically
```

This ensures:
- Automatic connection opening
- Automatic connection closing
- Proper error handling and rollback
- Resource cleanup

## Error Handling Strategy

1. **Connection Errors**: Caught and logged, then re-raised for user handling
2. **Query Errors**: Rolled back, logged with details, then re-raised
3. **Data Format Errors**: Caught during reading, logged, then re-raised
4. **Validation Errors**: Type checking and validation at entry points

All errors are logged with sufficient context for debugging.

## Batch Processing

For large datasets, the library processes data in configurable batches:

- **Default batch size**: 1000 records
- **Configurable**: Via `batch_size` parameter
- **Efficient**: Uses `executemany()` for bulk inserts
- **Memory-safe**: Processes chunks sequentially

## Configuration Hierarchy

1. **Environment Variables (.env file)**
2. **Default values in settings.py**
3. **Runtime parameters in method calls**

This hierarchy allows flexibility from most specific (runtime) to most general (defaults).

## Testing Strategy

- **Unit Tests**: Test individual methods with mocked dependencies
- **Integration Tests**: Test with real database (optional)
- **Fixtures**: Reusable test data and objects

## Performance Considerations

1. **Batch Operations**: Use `insert_batch()` for multiple records
2. **Connection Pooling**: Consider external pool for high-concurrency applications
3. **Query Optimization**: User responsible for SQL efficiency
4. **Logging Level**: Set to WARNING or ERROR in production
5. **Indexes**: Users should create appropriate database indexes

## Security Considerations

1. **SQL Injection Prevention**: All queries use parameterized statements
2. **Connection Security**: Support for SSL/TLS via psycopg2
3. **Credential Management**: Via environment variables
4. **Error Messages**: Controlled logging prevents credential leaks

## Future Enhancement Possibilities

1. Connection pooling
2. Query result caching
3. Migration support
4. ORM-like query builder
5. Async support
6. Multiple database support

---

**Version**: 1.0.0
**Last Updated**: 2026-02-08
