from PySide6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QApplication

def show_update_reminder(parent):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Security Reminder")
    msg.setText("Please connect to the Internet to verify updates.")
    msg.setInformativeText("Updates ensure security and stability. Recommended weekly.")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec()

def show_restricted_modal(parent):
    dialog = QDialog(parent)
    dialog.setWindowTitle("🔒 Restricted Mode")
    dialog.setModal(True)
    layout = QVBoxLayout()
    layout.addWidget(QLabel("<b>Restricted Mode Active</b>"))
    layout.addWidget(QLabel("You haven’t verified updates in over 14 days."))
    layout.addWidget(QLabel("• Editing, saving, and exporting still work"))
    layout.addWidget(QLabel("• Plugin installation and unsigned scripts are disabled"))
    btn = QPushButton("Verify Online or Import Signed Package")
    btn.clicked.connect(dialog.accept)
    layout.addWidget(btn)
    dialog.setLayout(layout)
    dialog.resize(400, 200)
    dialog.exec()
