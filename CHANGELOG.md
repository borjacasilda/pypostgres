# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-08

### Added
- Initial release
- PostgreSQL wrapper with CRUD operations
- Support for multiple data formats (CSV, JSON, Excel, PDF, SQL files)
- Batch insert operations
- Table management (create, drop, inspect)
- Comprehensive logging system
- Full type hints and documentation
- Context manager support
- Examples and unit tests

### Features
- Single record insertion
- Batch insertion with configurable batch size
- Update and delete operations
- SELECT queries with optional DataFrame results
- Table creation with column definitions
- Table inspection (columns, existence check)
- Data import from CSV, JSON, Excel, SQL files, and DataFrames
- Parameterized queries for SQL injection prevention
- Automatic connection management
- Detailed error handling and logging

---

**Version**: 1.0.0
**Date**: February 8, 2026
