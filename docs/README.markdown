# DuckDB Importer

A desktop application for importing CSV and Excel files into a DuckDB database.

## Features
- Import CSV and Excel files
- Create new tables or append to existing ones
- Schema validation before data import
- Adds `file_name` and `import_date_time` columns
- Excel sheet selection
- GUI built with PyQt5
- Credits: Egezon Baruti

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/duckdb-importer.git
   cd duckdb-importer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Download
- If you dont want to build the app, you can download .exe and use it in your Windows-Desktop from download folder.

## Usage
Run the application:
```bash
python src/main.py
```

## Building the .exe
See [BUILD.md](docs/BUILD.md) for instructions on building the executable.

## License
MIT License. See [LICENSE](LICENSE) for details.