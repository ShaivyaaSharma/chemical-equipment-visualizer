STYLES = """
    QWidget { 
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #050505, stop:0.5 #161b22, stop:1 #050505); 
        color: #f0f6fc; 
        font-family: 'Segoe UI', sans-serif; 
    }
    
    QLineEdit { 
        padding: 10px; 
        border: 1px solid #30363d; 
        border-radius: 6px; 
        background: #0d1117; 
        color: white; 
        font-size: 14px;
    }
    QLineEdit:focus { border: 1px solid #22d3ee; }
    
    QPushButton.primary {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
        border: none;
    }
    QPushButton.primary:hover { background-color: #2ea043; }
    
    QPushButton.secondary {
        background-color: #1f2428;
        color: #22d3ee;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 8px 16px;
    }
    
    QListWidget { 
        background: transparent; 
        border: none; 
        outline: none;
    }
    QListWidget::item { 
        padding: 12px 20px; 
        margin-bottom: 8px;
        color: #8b949e; 
        font-size: 18px; 
        font-weight: 500;
        border-left: 4px solid transparent; 
        border-radius: 0 8px 8px 0;
    }
    QListWidget::item:selected { 
        color: #22d3ee; 
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(34, 211, 238, 0.1), stop:1 rgba(34, 211, 238, 0.02));
        border-left: 4px solid #22d3ee; 
    }
    QListWidget::item:hover { 
        color: #e6edf3; 
        background-color: rgba(255, 255, 255, 0.03);
    }
"""
