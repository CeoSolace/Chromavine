from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QSpinBox, QPushButton, QFileDialog
import os

class ExportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Settings")
        self.output_path = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.filename_edit = QLineEdit("project_export")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp4", "mov", "mkv", "webm"])

        self.width_spin = QSpinBox()
        self.width_spin.setRange(320, 7680)
        self.width_spin.setValue(1920)

        self.height_spin = QSpinBox()
        self.height_spin.setRange(240, 4320)
        self.height_spin.setValue(1080)

        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 240)
        self.fps_spin.setValue(30)

        form.addRow("Filename:", self.filename_edit)
        form.addRow("Format:", self.format_combo)
        form.addRow("Width:", self.width_spin)
        form.addRow("Height:", self.height_spin)
        form.addRow("FPS:", self.fps_spin)

        browse_btn = QPushButton("Browse Output Folder")
        browse_btn.clicked.connect(self.browse_folder)

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.accept)

        layout.addLayout(form)
        layout.addWidget(browse_btn)
        layout.addWidget(export_btn)
        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Export Folder")
        if folder:
            self.output_path = folder

    def get_settings(self):
        ext = self.format_combo.currentText()
        name = self.filename_edit.text()
        full_name = f"{name}.{ext}" if not name.endswith(f".{ext}") else name
        path = os.path.join(self.output_path, full_name) if self.output_path else full_name
        return {
            "output_path": path,
            "width": self.width_spin.value(),
            "height": self.height_spin.value(),
            "fps": self.fps_spin.value(),
            "format": ext
        }
