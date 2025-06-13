import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from src.ui_manager import ImportUI
from src.db_manager import DatabaseManager


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV/Excel to DuckDB Importer")

        # Better path handling for both development and compiled executable
        if getattr(sys, "frozen", False):
            # Running as compiled executable
            exe_dir = os.path.dirname(sys.executable)
        else:
            # Running in development environment
            exe_dir = os.path.dirname(os.path.abspath(__file__))

        try:
            db_path = os.path.join(exe_dir, "database", "data.db")
            self.db_manager = DatabaseManager(db_path)
            self.ui = ImportUI(self, self.db_manager)
            self.setCentralWidget(self.ui)
            self.setGeometry(100, 100, 800, 600)
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to initialize database: {str(e)}"
            )
            sys.exit(1)

    def closeEvent(self, event):
        """Handle window close event to properly close database connection"""
        try:
            if hasattr(self, "db_manager") and self.db_manager:
                self.db_manager.close()
        except Exception as e:
            print(f"Error closing database: {e}")
        event.accept()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)
