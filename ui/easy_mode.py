from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox, QHBoxLayout
from core.project import Project

class EasyModeWidget(QWidget):
    def __init__(self, restricted_mode=False):
        super().__init__()
        self.restricted_mode = restricted_mode
        self.project = Project()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>✨ Easy Mode</h2>"))
        if self.restricted_mode:
            layout.addWidget(QLabel("<font color='orange'>⚠️ Restricted Mode: Plugin install disabled</font>"))

        # Preset selector
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Template:"))
        preset_combo = QComboBox()
        preset_combo.addItems(["YouTube 1080p", "TikTok 1080x1920", "Podcast Audio", "4K Cinematic"])
        preset_layout.addWidget(preset_combo)
        layout.addLayout(preset_layout)

        # Quick export
        export_btn = QPushButton("🚀 One-Click Export")
        export_btn.clicked.connect(self.quick_export)
        layout.addWidget(export_btn)

        # Switch mode
        switch_btn = QPushButton("Switch to Pro Mode")
        switch_btn.clicked.connect(self.switch_mode)
        layout.addWidget(switch_btn)

        layout.addStretch()
        self.setLayout(layout)

    def quick_export(self):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Export", "Exporting with default settings... (simulated)")

    def switch_mode(self):
        from PySide6.QtCore import QEvent
        from PySide6.QtGui import QKeyEvent
        from PySide6.QtCore import Qt
        # Signal handled by MainWindow
        self.parent().toggle_mode("Pro")
