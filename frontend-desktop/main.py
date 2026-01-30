#Frontend desktop application
# Uses PyQt5 for UI, Matplotlib for charts, Requests for API calls
import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QFileDialog, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


API_BASE = "http://127.0.0.1:8000/api"


class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer - Desktop")
        self.setGeometry(100, 100, 1200, 700)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Info label
        self.label = QLabel("Upload CSV or fetch dataset from backend")
        self.layout.addWidget(self.label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        btn_layout.addWidget(self.upload_btn)

        self.fetch_btn = QPushButton("Fetch Latest Dataset")
        self.fetch_btn.clicked.connect(self.fetch_latest_dataset)
        btn_layout.addWidget(self.fetch_btn)
        self.layout.addLayout(btn_layout)

        # Table
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Charts
        self.fig = Figure(figsize=(10, 4))
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        self.latest_dataset_id = None
        self.df = None
        
   #CSV upload
    def upload_csv(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options
        )
        if file_path:
            
            try:
                df = pd.read_csv(file_path)
                required_cols = ["Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"]
                if any(col not in df.columns for col in required_cols):
                    self.label.setText(f"Invalid CSV. Required columns: {required_cols}")
                    return
                if df.empty:
                    self.label.setText("Error: CSV file is empty")
                    return
            except Exception as e:
                self.label.setText(f"Error reading CSV: {e}")
                return

          
            self.upload_to_backend(file_path)

    def upload_to_backend(self, file_path):
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                res = requests.post(f"{API_BASE}/upload-csv/", files=files, timeout=5)

                if res.status_code != 200:
                    self.label.setText(f"Upload failed: {res.text}")
                    return

                data = res.json()
                if "error" in data:
                    self.label.setText(f"Upload error: {data['error']}")
                    return

                self.latest_dataset_id = data.get("dataset_id")
                self.label.setText(f"Uploaded: {file_path} | Dataset ID: {self.latest_dataset_id}")
                self.load_dataset_table(self.latest_dataset_id)

        except requests.exceptions.Timeout:
            self.label.setText("Error: Backend timed out. Is it running?")
        except requests.exceptions.ConnectionError:
            self.label.setText("Error: Cannot connect to backend. Is it online?")
        except Exception as e:
            self.label.setText(f"Unexpected error: {e}")

   #fetches dataset
    def fetch_latest_dataset(self):
        if not self.latest_dataset_id:
            self.label.setText("No dataset uploaded yet!")
            return
        self.load_dataset_table(self.latest_dataset_id)

    def load_dataset_table(self, dataset_id):
        try:
            res = requests.get(f"{API_BASE}/dataset/{dataset_id}/data/", timeout=5)
            res.raise_for_status()
            data = res.json().get("data", [])
            if not data:
                self.label.setText("Dataset is empty")
                self.df = pd.DataFrame()
                self.table.setRowCount(0)
                self.table.setColumnCount(0)
                self.fig.clear()
                self.canvas.draw()
                return

            self.df = pd.DataFrame(data)
            self.table.setRowCount(len(self.df))
            self.table.setColumnCount(len(self.df.columns))
            self.table.setHorizontalHeaderLabels(self.df.columns)

            for i, row in enumerate(data):
                for j, key in enumerate(row.keys()):
                    self.table.setItem(i, j, QTableWidgetItem(str(row[key])))

            self.label.setText(f"Dataset {dataset_id} loaded successfully")
            self.update_charts()

        except requests.exceptions.Timeout:
            self.label.setText("Error: Backend timed out. Cannot fetch dataset.")
        except requests.exceptions.ConnectionError:
            self.label.setText("Error: Backend offline. Please start the server.")
        except Exception as e:
            self.label.setText(f"Unexpected error: {e}")

   #charts
    def update_charts(self):
        if self.df is None or self.df.empty:
            self.fig.clear()
            self.canvas.draw()
            return

        self.fig.clear()
        ax1 = self.fig.add_subplot(131)  # Flowrate Bar
        ax2 = self.fig.add_subplot(132)  # Temperature Line
        ax3 = self.fig.add_subplot(133)  # Equipment Type Pie

        # Bar
        ax1.bar(self.df["Equipment Name"], self.df["Flowrate"], color="skyblue")
        ax1.set_title("Flowrate")
        ax1.set_xticklabels(self.df["Equipment Name"], rotation=90, fontsize=8)

        # Line
        ax2.plot(self.df["Equipment Name"], self.df["Temperature"], marker="o", color="orange")
        ax2.set_title("Temperature")
        ax2.set_xticklabels(self.df["Equipment Name"], rotation=90, fontsize=8)

        # Pie
        type_counts = self.df["Type"].value_counts()
        ax3.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%", startangle=140)
        ax3.set_title("Equipment Types")

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
