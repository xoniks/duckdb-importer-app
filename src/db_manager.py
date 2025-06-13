import duckdb
import os
import pandas as pd
from datetime import datetime
from src.schema_validator import SchemaValidator


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = duckdb.connect(db_path)
        self.validator = SchemaValidator()

    def get_tables(self):
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
        return [row[0] for row in self.conn.execute(query).fetchall()]

    def create_table(self, table_name, df, file_name):
        # Create a copy to avoid modifying the original DataFrame
        df_with_metadata = df.copy()

        # Add file_name and import_date_time columns
        df_with_metadata["file_name"] = file_name
        df_with_metadata["import_date_time"] = datetime.now()

        # Create table with the full dataframe schema
        self.conn.register("temp_table", df_with_metadata)
        self.conn.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM temp_table"
        )
        self.conn.unregister("temp_table")

    def append_data(self, table_name, df, file_name):
        # Validate schema BEFORE adding custom columns
        if self.validator.validate_schema(self.conn, table_name, df):
            # Create a copy to avoid modifying the original DataFrame
            df_with_metadata = df.copy()

            # Add file_name and import_date_time columns after validation
            df_with_metadata["file_name"] = file_name
            df_with_metadata["import_date_time"] = datetime.now()

            # Insert the data with metadata
            self.conn.register("temp_table", df_with_metadata)
            self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM temp_table")
            self.conn.unregister("temp_table")
            return True, None
        else:
            # Return False and the validation errors
            return False, self.validator.get_validation_summary()

    def get_table_schema(self, table_name):
        return self.conn.execute(f"DESCRIBE {table_name}").fetchall()

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
