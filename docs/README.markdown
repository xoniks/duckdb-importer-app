# DuckDB Importer

A user-friendly desktop application for importing CSV and Excel files into a DuckDB database with automatic schema validation and metadata tracking.

## Description

DuckDB Importer is a PyQt5-based GUI application that simplifies the process of importing structured data from CSV and Excel files into DuckDB databases. The application provides an intuitive interface for data professionals who need to quickly load data while maintaining data integrity through schema validation.

The application automatically creates a local DuckDB database and allows users to either create new tables or append data to existing ones. Each import automatically adds tracking metadata including the source filename and import timestamp, making it easy to audit data lineage.

## Key Features

- **Multi-format Support**: Import both CSV and Excel files (.csv, .xlsx, .xls)
- **Excel Sheet Selection**: Choose specific sheets from Excel workbooks
- **Schema Validation**: Automatic validation ensures data consistency when appending to existing tables
- **Metadata Tracking**: Automatically adds `file_name` and `import_date_time` columns to track data source and import time
- **Table Management**: Create new tables or append to existing ones with schema compatibility checks
- **User-friendly GUI**: Clean PyQt5 interface for easy operation
- **Database Integration**: Uses DuckDB for fast, efficient data storage and querying

## Quick Start - Download Ready-to-Use Executable

**For Windows users who want to use the application immediately:**

1. Navigate to the `download/` folder in this repository
2. Download `DuckDBImporter.exe`
3. Double-click the executable to run the application
4. No installation or Python setup required!

The executable includes all dependencies and creates a `database/` folder in the same directory for storing your DuckDB files.

## Installation from Source

If you prefer to run from source or are on non-Windows platforms:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/duckdb-importer.git
   cd duckdb-importer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python src/main.py
   ```

## How to Use the Application

1. **Launch the Application**
   - Run the executable or use `python src/main.py`
   - The application will create a `database/data.db` file automatically

2. **Import Your Data**
   - Click the import button to select your CSV or Excel file
   - For Excel files, choose the specific sheet you want to import
   - Preview your data in the application interface

3. **Choose Import Options**
   - **Create New Table**: Enter a table name to create a new table
   - **Append to Existing**: Select an existing table from the dropdown

4. **Schema Validation**
   - When appending, the application validates that your data matches the existing table schema
   - Any schema mismatches will be reported with detailed error messages

5. **Complete Import**
   - Click import to load your data
   - The application automatically adds metadata columns tracking the source file and import timestamp

6. **Access Your Data**
   - Your data is stored in the DuckDB database
   - Use any DuckDB-compatible tool or the DuckDB CLI to query your imported data

## Building the .exe
See [BUILD.md](docs/BUILD.md) for instructions on building the executable.

## License
MIT License. See [LICENSE](LICENSE) for details.