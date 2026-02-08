"""
Setup script for PyPostgres package.

Install with: pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
long_description = Path("README.md").read_text(encoding="utf-8")

# Read requirements from requirements.txt
requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()

setup(
    name="pypostgres",
    version="1.0.0",
    description="A professional PostgreSQL wrapper library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/pypostgres",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/pypostgres/issues",
        "Documentation": "https://github.com/yourusername/pypostgres/docs",
        "Source Code": "https://github.com/yourusername/pypostgres",
    },
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.12.0",
            "black>=21.0",
            "flake8>=3.9.0",
            "isort>=5.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="postgresql postgres database orm wrapper sql python",
    license="MIT",
    zip_safe=False,
    include_package_data=True,
)
