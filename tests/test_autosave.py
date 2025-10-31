import os
import tempfile
import time
from pathlib import Path
from core.autosave import AutoSaveManager

def test_autosave_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        proj_file = os.path.join(tmpdir, "current_project.cvproj")
        autosave_dir = Path(tmpdir) / ".chromavine" / "autosaves"
        autosave_dir.mkdir(parents=True)

        with open(proj_file, "w") as f:
            f.write('{"test": true}')

        os.chdir(tmpdir)
        manager = AutoSaveManager(interval=1)
        manager.project_path = "current_project.cvproj"
        manager.autosave_dir = autosave_dir

        manager.start()
        time.sleep(2)
        manager.stop()

        autosaves = list(autosave_dir.glob("*.cvproj"))
        assert len(autosaves) >= 1
        with open(autosaves[0], "r") as f:
            content = f.read()
        assert '"test": true' in content
