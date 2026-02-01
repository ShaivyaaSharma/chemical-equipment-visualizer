from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QMessageBox, QFileDialog, QSizePolicy, QTextBrowser
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QTextDocument
from PyQt5.QtPrintSupport import QPrinter
import datetime
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import html
import tempfile

class ReportsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.dataset_id = None
        self.html_content = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(layout)

        
        header = QHBoxLayout()
        title = QLabel("Report Generation")
        title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title.setStyleSheet("color: white;")
        header.addWidget(title)
        
        header.addStretch()
        
        self.download_btn = QPushButton("Download PDF")
        self.download_btn.setCursor(Qt.PointingHandCursor)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 16px; 
            }
            QPushButton:hover { background-color: #2ea043; }
            QPushButton:disabled { background-color: #30363d; color: #8b949e; }
        """)
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_report)
        header.addWidget(self.download_btn)
        
        layout.addLayout(header)

        
        self.preview_area = QScrollArea()
        self.preview_area.setWidgetResizable(True)
        self.preview_area.setStyleSheet("background: transparent; border: none;")
        
        container = QWidget()
        clayout = QVBoxLayout(container)
        clayout.setAlignment(Qt.AlignCenter)
        
       
        self.paper = QFrame()
        self.paper.setFixedWidth(850)
        self.paper.setMinimumHeight(1200) 
        self.paper.setStyleSheet("background: white; border-radius: 2px; border: 1px solid #30363d;")
        
        self.paper_layout = QVBoxLayout(self.paper)
        self.paper_layout.setContentsMargins(60, 60, 60, 60)
        
        self.report_content = QTextBrowser()
        self.report_content.setOpenExternalLinks(False)
        self.report_content.setReadOnly(True)
        self.report_content.setFrameShape(QFrame.NoFrame)
        self.report_content.setStyleSheet("background: transparent; border: none;")
        self.report_content.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
        self.report_content.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.report_content.setHtml("<html><body><p>Select a dataset to view the report.</p></body></html>")
        self.report_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.paper_layout.addWidget(self.report_content)
        
        clayout.addWidget(self.paper)
        
        self.preview_area.setWidget(container)
        layout.addWidget(self.preview_area)

    def generate_charts_for_report(self, df):
        paths = {}
        
        
        with plt.style.context('default'):
            
            
            fig = plt.figure(figsize=(8, 3.5)) 
            counts = df['Type'].value_counts()
            colors = ["#3b82f6", "#ef4444", "#f59e0b", "#10b981", "#8b5cf6", "#ec4899"]
            
            
            ax = fig.add_subplot(111)
            wedges, texts = ax.pie(counts.values, colors=colors, startangle=90)
            ax.axis('equal') 
            ax.legend(wedges, counts.index, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            plt.tight_layout()
            
            
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                path = tmp.name
                
            fig.savefig(path, dpi=100, bbox_inches='tight', transparent=True)
            paths['dist'] = path
            plt.close(fig)

            
            def make_bar_chart(data_col, color, ylabel):
                fig = plt.figure(figsize=(10, 2.8)) 
                names = df['Equipment Name']
                values = df[data_col]
                
                plt.bar(names, values, color=color, alpha=0.7)
                plt.xticks(rotation=45, ha='right', fontsize=8)
                plt.yticks(fontsize=8)
                plt.grid(axis='y', linestyle='--', alpha=0.5)
                plt.tight_layout()
                
                with tempfile.NamedTemporaryFile(suffix=f"_{data_col.lower()}.png", delete=False) as tmp:
                    path = tmp.name
                    
                fig.savefig(path, dpi=100, bbox_inches='tight')
                plt.close(fig)
                return path

            
            paths['flow'] = make_bar_chart('Flowrate', '#3b82f6', 'Flowrate')
            
            paths['press'] = make_bar_chart('Pressure', '#8b5cf6', 'Pressure')
            
            paths['temp'] = make_bar_chart('Temperature', '#ef4444', 'Temperature')

        return paths

    def update_report(self, df, dataset_id):
        self.dataset_id = dataset_id
        self.download_btn.setEnabled(True)
        
        
        count = len(df)
        unique_types = df['Type'].nunique() if 'Type' in df else 0
        
        avg_flow = f"{df['Flowrate'].mean():.2f}"
        min_flow = f"{df['Flowrate'].min():.2f}"
        max_flow = f"{df['Flowrate'].max():.2f}"
        
        avg_press = f"{df['Pressure'].mean():.2f}"
        avg_temp = f"{df['Temperature'].mean():.2f}"
        
        now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        user = "admin"
        
        charts = self.generate_charts_for_report(df)
        
        
        table_rows = ""
        for i, row in df.iterrows():
            bg = "#f3f4f6" if i % 2 == 0 else "white"
            table_rows += f"""
            <tr style="background-color: {bg};">
                <td>{html.escape(str(row.get('Equipment Name', '')))}</td>
                <td>{html.escape(str(row.get('Type', '')))}</td>
                <td>{html.escape(str(row.get('Flowrate', '')))}</td>
                <td>{html.escape(str(row.get('Pressure', '')))}</td>
                <td>{html.escape(str(row.get('Temperature', '')))}</td>
            </tr>
            """

        
        self.html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Times New Roman', serif; color: #1f2937; margin: 0; padding: 0; line-height: 1.1; }} 
                
                .header {{ border-bottom: 2px solid #333; padding-bottom: 5px; margin-bottom: 10px; }}
                h1 {{ font-size: 28pt; margin: 0; margin-bottom: 5px; color: #111827; text-align: left; }}
                
                h2 {{ font-size: 20pt; color: #000000; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 15px; margin-bottom: 5px; font-weight: bold; text-align: left; }}
                h3 {{ font-size: 16pt; color: #000000; margin-top: 10px; margin-bottom: 2px; font-weight: bold; text-align: left; }}
                
                p {{ font-size: 12pt; line-height: 1.2; margin: 0; margin-bottom: 5px; color: #000; text-align: justify; }}
                
                .stats-line {{ font-size: 11pt; margin: 0; margin-bottom: 2px; color: #000; font-weight: bold; }}
                
                .summary-table {{ width: 100%; border-collapse: collapse; font-size: 12pt; margin-bottom: 10px; }}
                .summary-table td {{ border: 1px solid #d1d5db; padding: 6px; }}
                .bg-gray {{ background-color: #f3f4f6; font-weight: bold; }}
                
                img {{ width: 100%; height: auto; display: block; margin: 0 auto; object-fit: contain; }}
                .caption {{ text-align: center; font-style: italic; font-size: 10pt; margin-top: 2px; color: #4b5563; }}
                
                .data-table {{ width: 100%; border-collapse: collapse; font-size: 11pt; table-layout: fixed; }}
                .data-table th {{ background-color: #374151; color: white; padding: 6px; text-align: left; border: 1px solid #374151; }}
                .data-table td {{ border: 1px solid #e5e7eb; padding: 6px; word-wrap: break-word; }}
                
                .footer {{ margin-top: 30px; border-top: 1px solid #ccc; paddingTop: 10px; font-size: 9pt; text-align: center; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Chemical Equipment Parameter Visualizer</h1>
                <table style="width: 100%; border: none; font-size: 11pt; margin-top: 2px;">
                    <tr>
                        <td style="text-align: left; border: none; padding: 0;"><strong>Date:</strong> {now}</td>
                        <td style="text-align: right; border: none; padding: 0;"><strong>Generated by:</strong> {user}</td>
                    </tr>
                </table>
            </div>

            <h2>Dataset Overview Summary</h2>
            <p>
                This report provides an analysis of <strong>{count}</strong> equipment records, covering <strong>{unique_types}</strong> distinct equipment types.
                The dataset reveals an average flowrate of <strong>{avg_flow} m³/h</strong>, an average pressure of <strong>{avg_press} PSI</strong>, and an average operating temperature of <strong>{avg_temp} °C</strong>.
            </p>
            
            <table class="summary-table" width="100%" cellspacing="0" cellpadding="6" style="border-collapse: collapse;">
                <tr class="bg-gray">
                    <td width="25%">Total Records</td> <td width="25%">{count}</td>
                    <td width="25%">Average Flowrate</td> <td width="25%">{avg_flow} m³/h</td>
                </tr>
                <tr>
                    <td>Unique Types</td> <td>{unique_types}</td>
                    <td>Average Pressure</td> <td>{avg_press} PSI</td>
                </tr>
                <tr class="bg-gray">
                    <td colspan="2"></td>
                    <td>Average Temperature</td> <td>{avg_temp} °C</td>
                </tr>
            </table>
            
            <h2>Equipment Type Distribution</h2>
            <p align="center" style="margin: 0; padding: 0;">
                <img src="{charts['dist']}" width="700">
            </p>
            <p class="caption">Figure 1: Distribution of equipment types in the dataset.</p>
            
            <h2>Parameter Analysis</h2>
            
            <h3>Flowrate Analysis</h3>
            <p class="stats-line">Min: <strong>{min_flow}</strong> | Max: <strong>{max_flow}</strong> | Avg: <strong>{avg_flow}</strong></p>
            <p align="center" style="margin: 0; padding: 0;">
                <img src="{charts['flow']}" width="700">
            </p>
            
            <h3>Pressure Analysis</h3>
            <p class="stats-line">Avg: <strong>{avg_press}</strong></p>
            <p align="center" style="margin: 0; padding: 0;">
                <img src="{charts['press']}" width="700">
            </p>
            
            <h3>Temperature Analysis</h3>
            <p class="stats-line">Avg: <strong>{avg_temp}</strong></p>
            <p align="center" style="margin: 0; padding: 0;">
                <img src="{charts['temp']}" width="700">
            </p>

            <br>
            <br>
            <h2>Full Dataset Data Table</h2>
            <table class="data-table" width="100%" cellspacing="0" cellpadding="8" style="border-collapse: collapse;">
                <tr>
                    <th width="25%" style="background-color: #374151; color: white; padding: 10px; border: 1px solid #374151;">Equipment Name</th>
                    <th width="15%" style="background-color: #374151; color: white; padding: 10px; border: 1px solid #374151;">Type</th>
                    <th width="20%" style="background-color: #374151; color: white; padding: 10px; border: 1px solid #374151;">Flowrate</th>
                    <th width="20%" style="background-color: #374151; color: white; padding: 10px; border: 1px solid #374151;">Pressure</th>
                    <th width="20%" style="background-color: #374151; color: white; padding: 10px; border: 1px solid #374151;">Temperature</th>
                </tr>
                {table_rows}
            </table>
            
            <div class="footer">
                Chemical Equipment Visualizer Report | Page 1
            </div>
            
        </body>
        </html>
        """
        self.report_content.setText(self.html_content)

    def download_report(self):
        if not self.dataset_id: return
        path, _ = QFileDialog.getSaveFileName(self, "Save Report", f"report_{self.dataset_id}.pdf", "PDF Files (*.pdf)")
        if path:
            try:
                printer = QPrinter()
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(path)
                
                doc = QTextDocument()
                doc.setHtml(self.html_content)
                doc.print_(printer)
                
                QMessageBox.information(self, "Success", f"Report saved successfully to {path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save PDF: {str(e)}")
