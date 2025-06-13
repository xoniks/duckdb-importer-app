from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QLineEdit,
    QLabel,
    QMessageBox,
    QInputDialog,
)
from src.file_importer import FileImporter
import pandas as pd
import os


class ImportUI(QWidget):
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        self.file_importer = FileImporter()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Database path display
        db_path = os.path.dirname(self.db_manager.db_path)
        self.db_path_label = QLabel(f"Database Location: {db_path}")
        layout.addWidget(self.db_path_label)

        # Table selection
        table_layout = QHBoxLayout()
        self.table_combo = QComboBox()
        self.refresh_table_list()
        table_layout.addWidget(QLabel("Select Table:"))
        table_layout.addWidget(self.table_combo)
        layout.addLayout(table_layout)

        # Import button
        self.import_btn = QPushButton("Import File")
        self.import_btn.clicked.connect(self.import_file)
        layout.addWidget(self.import_btn)

        # Credits
        credits_label = QLabel("Credits: Egezon Baruti")
        layout.addWidget(credits_label)

        layout.addStretch()
        self.setLayout(layout)

    def refresh_table_list(self):
        """Refresh the table list in the combo box"""
        try:
            self.table_combo.clear()
            self.table_combo.addItem("Create New Table")
            tables = self.db_manager.get_tables()
            if tables:
                self.table_combo.addItems(tables)
        except Exception as e:
            QMessageBox.warning(
                self, "Warning", f"Could not refresh table list: {str(e)}"
            )

    def import_file(self):
        try:
            # Disable the import button during processing
            self.import_btn.setEnabled(False)
            self.import_btn.setText("Processing...")

            data, file_name, sheet_names = self.file_importer.import_file(self)
            if data is None:
                return

            # Handle Excel sheet selection
            df = data
            if sheet_names:
                sheet, ok = QInputDialog.getItem(
                    self, "Select Sheet", "Choose Excel sheet:", sheet_names, 0, False
                )
                if not ok:
                    return
                try:
                    df = pd.read_excel(data, sheet_name=sheet)
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"Failed to read Excel sheet: {str(e)}"
                    )
                    return

            # Validate DataFrame
            if df.empty:
                QMessageBox.warning(
                    self, "Warning", "The selected file/sheet is empty."
                )
                return

            table_name = self.table_combo.currentText()
            if table_name == "Create New Table":
                table_name, ok = QInputDialog.getText(
                    self, "Table Name", "Enter new table name:"
                )
                if not ok or not table_name.strip():
                    return

                table_name = table_name.strip()

                # Validate table name (basic validation)
                if not table_name.replace("_", "").isalnum():
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Table name should contain only letters, numbers, and underscores.",
                    )
                    return

                # Check for duplicate table name
                if table_name in self.db_manager.get_tables():
                    QMessageBox.warning(
                        self, "Error", f"Table '{table_name}' already exists!"
                    )
                    return

                try:
                    self.db_manager.create_table(table_name, df, file_name)
                    self.refresh_table_list()  # Refresh the combo box
                    # Set the newly created table as selected
                    index = self.table_combo.findText(table_name)
                    if index >= 0:
                        self.table_combo.setCurrentIndex(index)
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Table '{table_name}' created and data imported successfully.\nRows imported: {len(df)}",
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"Failed to create table: {str(e)}"
                    )
            else:
                try:
                    success, error_message = self.db_manager.append_data(
                        table_name, df, file_name
                    )
                    if success:
                        QMessageBox.information(
                            self,
                            "Success",
                            f"Data appended to table '{table_name}' successfully.\nRows imported: {len(df)}",
                        )
                    else:
                        # Show detailed error message with column mismatches
                        msg_box = QMessageBox(self)
                        msg_box.setIcon(QMessageBox.Warning)
                        msg_box.setWindowTitle("Schema Validation Failed")
                        msg_box.setText(
                            "Schema mismatch detected. Data cannot be imported."
                        )
                        msg_box.setDetailedText(
                            f"Schema validation errors:\n\n{error_message}"
                        )
                        msg_box.setStandardButtons(QMessageBox.Ok)
                        msg_box.exec_()
                except Exception as e:
                    QMessageBox.critical(
                        self, "Error", f"Failed to append data: {str(e)}"
                    )

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Unexpected error during import: {str(e)}"
            )
        finally:
            # Re-enable the import button
            self.import_btn.setEnabled(True)
            self.import_btn.setText("Import File")
