# Building the .exe File

This guide explains how to build a standalone .exe file for the DuckDB Importer application using PyInstaller.

## Prerequisites
- Python 3.8 or higher
- All dependencies installed (see requirements.txt)
- PyInstaller installed (`pip install pyinstaller`)

## Steps
1. Navigate to the project directory:
   ```bash
   cd path/to/duckdb-importer
   ```

2. Run PyInstaller to create the .exe:
   ```bash
   pyinstaller --onefile --windowed --name DuckDBImporter src/main.py
   ```

3. Find the executable:
   - The .exe file will be located in the `dist` folder as `DuckDBImporter.exe`.

## Notes
- The `--onefile` flag creates a single executable.
- The `--windowed` flag prevents a console window from appearing.
- The database will be created in a `database` folder relative to the .exe location.
- Ensure all dependencies are installed before building.

## Troubleshooting
- If the .exe fails to run, check that all dependencies are correctly installed.
- For large dependencies, ensure your system has sufficient memory during the build process.