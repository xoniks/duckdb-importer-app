import pandas as pd
import duckdb


class SchemaValidator:
    def __init__(self):
        self.validation_errors = []

    def normalize_column_name(self, col_name):
        """Normalize column names for comparison (handle spaces, case, etc.)"""
        if isinstance(col_name, str):
            # Convert to lowercase and replace spaces with underscores
            return col_name.lower().strip().replace(" ", "_")
        return str(col_name).lower().strip().replace(" ", "_")

    def normalize_type_name(self, type_name):
        """Normalize type names for comparison"""
        type_str = str(type_name).lower().strip()

        # Handle common type variations
        type_mapping = {
            # Pandas to DuckDB mappings
            "int64": "bigint",
            "int32": "integer",
            "int16": "smallint",
            "int8": "tinyint",
            "float64": "double",
            "float32": "real",
            "object": "varchar",
            "string": "varchar",
            "datetime64": "timestamp",
            "datetime64[ns]": "timestamp",
            "bool": "boolean",
            # Common variations
            "integer": "integer",
            "bigint": "bigint",
            "varchar": "varchar",
            "text": "varchar",
            "double": "double",
            "timestamp": "timestamp",
        }

        return type_mapping.get(type_str, type_str)

    def validate_schema(self, conn, table_name, df):
        try:
            # Clear previous errors
            self.validation_errors = []

            # Fetch existing schema
            existing_schema = conn.execute(f"DESCRIBE {table_name}").fetchall()
            existing_columns = {row[0]: row[1] for row in existing_schema}

            # Remove custom columns from existing schema for comparison
            existing_columns_filtered = existing_columns.copy()
            existing_columns_filtered.pop("file_name", None)
            existing_columns_filtered.pop("import_date_time", None)

            # Get raw data types from pandas
            raw_df_columns = {col: str(dtype) for col, dtype in df.dtypes.items()}
            # Remove custom columns for validation
            df_columns = raw_df_columns.copy()
            df_columns.pop("file_name", None)
            df_columns.pop("import_date_time", None)

            # Normalize column names for comparison
            normalized_existing = {}
            existing_col_mapping = {}  # Map normalized -> original
            for col, dtype in existing_columns_filtered.items():
                normalized_col = self.normalize_column_name(col)
                normalized_existing[normalized_col] = self.normalize_type_name(dtype)
                existing_col_mapping[normalized_col] = col

            normalized_new = {}
            new_col_mapping = {}  # Map normalized -> original
            for col, dtype in df_columns.items():
                normalized_col = self.normalize_column_name(col)
                normalized_new[normalized_col] = self.normalize_type_name(dtype)
                new_col_mapping[normalized_col] = col

            # Check if column counts match
            if len(normalized_existing) != len(normalized_new):
                missing_in_new = set(normalized_existing.keys()) - set(
                    normalized_new.keys()
                )
                extra_in_new = set(normalized_new.keys()) - set(
                    normalized_existing.keys()
                )

                if missing_in_new:
                    missing_original = [
                        existing_col_mapping[col] for col in missing_in_new
                    ]
                    self.validation_errors.append(
                        f"Missing columns in new data: {', '.join(missing_original)}"
                    )

                if extra_in_new:
                    extra_original = [new_col_mapping[col] for col in extra_in_new]
                    self.validation_errors.append(
                        f"Extra columns in new data: {', '.join(extra_original)}"
                    )

                return False

            # Check each column for type mismatches
            type_mismatches = []
            for norm_col in normalized_existing:
                if norm_col in normalized_new:
                    existing_type = normalized_existing[norm_col]
                    new_type = normalized_new[norm_col]

                    if existing_type != new_type:
                        original_existing_col = existing_col_mapping[norm_col]
                        original_new_col = new_col_mapping[norm_col]
                        type_mismatches.append(
                            f"'{original_existing_col}': Expected {existing_type}, got {new_type}"
                        )
                else:
                    original_col = existing_col_mapping[norm_col]
                    self.validation_errors.append(
                        f"Missing column in new data: '{original_col}'"
                    )
                    return False

            if type_mismatches:
                self.validation_errors.append("Data type mismatches:")
                self.validation_errors.extend(
                    [f"  - {mismatch}" for mismatch in type_mismatches]
                )
                return False

            # Check for extra columns in new data
            extra_columns = []
            for norm_col in normalized_new:
                if norm_col not in normalized_existing:
                    original_col = new_col_mapping[norm_col]
                    extra_columns.append(original_col)

            if extra_columns:
                self.validation_errors.append(
                    f"Extra columns in new data not found in existing table: {', '.join(extra_columns)}"
                )
                return False

            return True

        except Exception as e:
            self.validation_errors.append(f"Error during schema validation: {str(e)}")
            return False

    def get_validation_errors(self):
        """Get the list of validation errors"""
        return self.validation_errors

    def get_validation_summary(self):
        """Get a formatted summary of validation errors"""
        if not self.validation_errors:
            return "No validation errors found."

        return "\n".join(self.validation_errors)
