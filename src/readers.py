"""
Data readers module for PyPostgres.

Provides functionality to read and parse data from various formats.
"""

import csv
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Union

import pandas as pd
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


class BaseReader:
    """Base class for all data readers."""

    def read(self, source: Union[str, Path]) -> Union[List[Dict], pd.DataFrame]:
        """Read data from source."""
        raise NotImplementedError


class CSVReader(BaseReader):
    """Reader for CSV files."""

    def read(
        self, source: Union[str, Path], encoding: str = "utf-8"
    ) -> pd.DataFrame:
        """
        Read CSV file and return as DataFrame.

        Args:
            source: Path to CSV file
            encoding: File encoding (default: utf-8)

        Returns:
            DataFrame containing CSV data
        """
        try:
            df = pd.read_csv(source, encoding=encoding)
            logger.info(f"Successfully read CSV file: {source}")
            return df
        except Exception as e:
            logger.error(f"Error reading CSV file {source}: {str(e)}")
            raise


class JSONReader(BaseReader):
    """Reader for JSON files."""

    def read(self, source: Union[str, Path]) -> Union[List[Dict], Dict]:
        """
        Read JSON file.

        Args:
            source: Path to JSON file

        Returns:
            Parsed JSON data
        """
        try:
            with open(source, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Successfully read JSON file: {source}")
            return data
        except Exception as e:
            logger.error(f"Error reading JSON file {source}: {str(e)}")
            raise


class SQLReader(BaseReader):
    """Reader for SQL files."""

    def read(self, source: Union[str, Path]) -> List[str]:
        """
        Read SQL file and return statements.

        Args:
            source: Path to SQL file

        Returns:
            List of SQL statements
        """
        try:
            with open(source, "r", encoding="utf-8") as f:
                content = f.read()
            # Split statements by semicolon
            statements = [
                stmt.strip()
                for stmt in content.split(";")
                if stmt.strip()
            ]
            logger.info(f"Successfully read SQL file: {source}")
            return statements
        except Exception as e:
            logger.error(f"Error reading SQL file {source}: {str(e)}")
            raise


class PDFReader(BaseReader):
    """Reader for PDF files."""

    def read(self, source: Union[str, Path]) -> str:
        """
        Extract text from PDF file.

        Args:
            source: Path to PDF file

        Returns:
            Extracted text from PDF
        """
        try:
            reader = PdfReader(source)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            logger.info(f"Successfully read PDF file: {source}")
            return text
        except Exception as e:
            logger.error(f"Error reading PDF file {source}: {str(e)}")
            raise


class ExcelReader(BaseReader):
    """Reader for Excel files."""

    def read(
        self,
        source: Union[str, Path],
        sheet_name: Union[str, int] = 0,
    ) -> pd.DataFrame:
        """
        Read Excel file.

        Args:
            source: Path to Excel file
            sheet_name: Sheet name or index (default: 0)

        Returns:
            DataFrame containing Excel data
        """
        try:
            df = pd.read_excel(source, sheet_name=sheet_name)
            logger.info(f"Successfully read Excel file: {source}")
            return df
        except Exception as e:
            logger.error(f"Error reading Excel file {source}: {str(e)}")
            raise


class DataFrameReader(BaseReader):
    """Reader for pandas DataFrames."""

    def read(self, source: pd.DataFrame) -> pd.DataFrame:
        """
        Accept and return DataFrame.

        Args:
            source: DataFrame object

        Returns:
            DataFrame
        """
        logger.info("Successfully processed DataFrame")
        return source


class ReaderFactory:
    """Factory for creating appropriate data readers."""

    _readers = {
        ".csv": CSVReader,
        ".json": JSONReader,
        ".sql": SQLReader,
        ".pdf": PDFReader,
        ".xlsx": ExcelReader,
        ".xls": ExcelReader,
    }

    @staticmethod
    def get_reader(file_path: Union[str, Path]) -> BaseReader:
        """
        Get appropriate reader for file type.

        Args:
            file_path: Path to file

        Returns:
            Appropriate reader instance

        Raises:
            ValueError: If file type is not supported
        """
        ext = Path(file_path).suffix.lower()
        reader_class = ReaderFactory._readers.get(ext)

        if not reader_class:
            raise ValueError(
                f"Unsupported file format: {ext}. "
                f"Supported formats: {list(ReaderFactory._readers.keys())}"
            )

        return reader_class()

    @staticmethod
    def read_file(file_path: Union[str, Path]) -> Union[pd.DataFrame, str, List]:
        """
        Read file with appropriate reader.

        Args:
            file_path: Path to file

        Returns:
            Parsed data
        """
        reader = ReaderFactory.get_reader(file_path)
        return reader.read(file_path)
