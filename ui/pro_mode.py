from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel

class ProModeWidget(QWidget):
    def __init__(self, restricted_mode=False):
        super().__init__()
        self.restricted_mode = restricted_mode
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()

        tabs.addTab(QLabel("📽️ Timeline Editor\n- Multi-track\n- Keyframes\n- Nesting"), "Timeline")
        tabs.addTab(QLabel("🎨 Color Grading\n- Wheels, LUTs, Scopes\n- Masking & Tracking"), "Color")
        tabs.addTab(QLabel("🌀 Node Compositor\n- GLSL/Python effects\n- Particle systems"), "Fusion")
        tabs.addTab(QLabel("🧊 3D Workspace\n- FBX/GLTF import\n- PBR materials\n- Path tracing"), "3D")
        tabs.addTab(QLabel("🎧 Audio Studio\n- Multitrack\n- VST/LV2\n- Spectrogram"), "Audio")
        tabs.addTab(QLabel("📤 Deliver\n- 8K/240fps\n- Custom codecs\n- Burn-in options"), "Deliver")

        layout.addWidget(tabs)

        if self.restricted_mode:
            warn = QLabel("<font color='orange'>⚠️ Restricted Mode: Network features disabled</font>")
            layout.addWidget(warn)

        self.setLayout(layout)
