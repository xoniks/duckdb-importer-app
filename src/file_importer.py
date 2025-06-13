import pandas as pd
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class FileImporter:
    @staticmethod
    def import_file(parent):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                parent, "Select File", "", "CSV/Excel Files (*.csv *.xlsx *.xls)"
            )
            if not file_path:
                return None, None, None

            file_name = file_path.split("/")[-1]
            if file_path.endswith(".csv"):
                try:
                    df = pd.read_csv(file_path)
                    return df, file_name, None
                except Exception as e:
                    QMessageBox.critical(
                        parent, "Error", f"Failed to read CSV file: {str(e)}"
                    )
                    return None, None, None
            else:
                try:
                    # Get Excel sheet names
                    xl = pd.ExcelFile(file_path)
                    sheet_names = xl.sheet_names
                    return xl, file_name, sheet_names
                except Exception as e:
                    QMessageBox.critical(
                        parent, "Error", f"Failed to read Excel file: {str(e)}"
                    )
                    return None, None, None
        except Exception as e:
            QMessageBox.critical(
                parent, "Error", f"Unexpected error during file import: {str(e)}"
            )
            return None, None, None
