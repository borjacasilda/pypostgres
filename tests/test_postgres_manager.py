"""
Unit tests for PyPostgres library.

Run tests with: python -m pytest tests/
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd

from src.postgres_manager import PostgresManager
from src.readers import (
    CSVReader,
    JSONReader,
    SQLReader,
    PDFReader,
    ExcelReader,
    ReaderFactory,
)


class TestPostgresManager:
    """Test PostgresManager class"""

    @pytest.fixture
    def manager(self):
        """Create a PostgresManager instance for testing"""
        return PostgresManager(
            config={
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
                "user": "test_user",
                "password": "test_pass",
            }
        )

    def test_manager_initialization(self, manager):
        """Test manager initialization"""
        assert manager.config["database"] == "test_db"
        assert manager.connection is None

    def test_manager_context_manager(self, manager):
        """Test context manager functionality"""
        with patch.object(manager, "connect"):
            with patch.object(manager, "disconnect"):
                with manager as mgr:
                    assert mgr is manager


class TestReaders:
    """Test data reader classes"""

    def test_csv_reader(self, tmp_path):
        """Test CSV reader"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("name,age\nJohn,30\nJane,25\n")

        reader = CSVReader()
        df = reader.read(csv_file)

        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]

    def test_json_reader(self, tmp_path):
        """Test JSON reader"""
        json_file = tmp_path / "test.json"
        json_file.write_text('{"name": "John", "age": 30}')

        reader = JSONReader()
        data = reader.read(json_file)

        assert data["name"] == "John"
        assert data["age"] == 30

    def test_sql_reader(self, tmp_path):
        """Test SQL reader"""
        sql_file = tmp_path / "test.sql"
        sql_file.write_text("SELECT * FROM users; SELECT COUNT(*) FROM orders;")

        reader = SQLReader()
        statements = reader.read(sql_file)

        assert len(statements) == 2
        assert "SELECT * FROM users" in statements[0]

    def test_reader_factory_csv(self, tmp_path):
        """Test ReaderFactory with CSV file"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("id,name\n1,John\n")

        reader = ReaderFactory.get_reader(csv_file)
        assert isinstance(reader, CSVReader)

    def test_reader_factory_json(self, tmp_path):
        """Test ReaderFactory with JSON file"""
        json_file = tmp_path / "test.json"
        json_file.write_text("{}")

        reader = ReaderFactory.get_reader(json_file)
        assert isinstance(reader, JSONReader)

    def test_reader_factory_sql(self, tmp_path):
        """Test ReaderFactory with SQL file"""
        sql_file = tmp_path / "test.sql"
        sql_file.write_text("SELECT 1;")

        reader = ReaderFactory.get_reader(sql_file)
        assert isinstance(reader, SQLReader)

    def test_reader_factory_unsupported_format(self, tmp_path):
        """Test ReaderFactory with unsupported file format"""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("test")

        with pytest.raises(ValueError):
            ReaderFactory.get_reader(txt_file)


class TestDataFrameIntegration:
    """Test DataFrame-related functionality"""

    def test_dataframe_creation(self):
        """Test DataFrame creation and manipulation"""
        data = {"name": ["John", "Jane"], "age": [30, 25]}
        df = pd.DataFrame(data)

        assert len(df) == 2
        assert list(df.columns) == ["name", "age"]
        assert df.loc[0, "name"] == "John"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
