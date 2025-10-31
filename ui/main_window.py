import sys
from PySide6.QtWidgets import QMainWindow, QMessageBox, QMenuBar, QMenu
from PySide6.QtCore import QTimer
from ui.pro_mode import ProModeWidget
from ui.easy_mode import EasyModeWidget
from ui.update_ui import show_update_reminder, show_restricted_modal

class MainWindow(QMainWindow):
    def __init__(self, restricted_mode=False):
        super().__init__()
        self.restricted_mode = restricted_mode
        self.setWindowTitle("Chromavine Studio Pro")
        self.resize(1400, 900)
        self.mode = "Pro"
        self.init_ui()
        if self.restricted_mode:
            QTimer.singleShot(500, lambda: show_restricted_modal(self))

    def init_ui(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        mode_menu = menubar.addMenu("Mode")
        help_menu = menubar.addMenu("Help")

        switch_action = mode_menu.addAction("Switch to Easy Mode" if self.mode == "Pro" else "Switch to Pro Mode")
        switch_action.triggered.connect(self.toggle_mode)

        import_action = help_menu.addAction("Import Update Package")
        import_action.triggered.connect(self.import_update)

        self.toggle_mode(self.mode)

    def toggle_mode(self, mode=None):
        if mode == "Easy" or (mode is None and self.mode == "Pro"):
            self.mode = "Easy"
            widget = EasyModeWidget(self.restricted_mode)
            self.menuBar().actions()[1].menu().actions()[0].setText("Switch to Pro Mode")
        else:
            self.mode = "Pro"
            widget = ProModeWidget(self.restricted_mode)
            self.menuBar().actions()[1].menu().actions()[0].setText("Switch to Easy Mode")
        self.setCentralWidget(widget)

    def import_update(self):
        from PySide6.QtWidgets import QFileDialog
        from core.updater import UpdateManager
        with open("config.json", "r") as f:
            config = json.load(f)
        updater = UpdateManager(config)
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Signed Update ZIP", "", "ZIP Files (*.zip)")
        if filepath:
            success = updater.import_offline_package(filepath)
            if success:
                QMessageBox.information(self, "Success", "Update applied. Restart to take effect.")
                self.restricted_mode = False
            else:
                QMessageBox.critical(self, "Error", "Invalid or unsigned package.")
