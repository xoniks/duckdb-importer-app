from setuptools import setup, find_packages

setup(
    name="duckdb-importer",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt5==5.15.11",
        "duckdb==1.1.2",
        "pandas==2.2.3",
        "openpyxl==3.1.5",
        "pyinstaller==6.10.0",
    ],
    entry_points={
        "console_scripts": [
            "duckdb-importer=main:main",
        ],
    },
    author="Egezon Baruti",
    description="A desktop app for importing CSV/Excel files to DuckDB",
    license="MIT",
    keywords="duckdb csv excel importer",
)