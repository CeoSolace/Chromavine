import os
import json
import tempfile
from core.integrity import IntegrityChecker

def test_integrity_verification():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)

        os.makedirs("core", exist_ok=True)
        test_file = "core/media.py"
        with open(test_file, "w") as f:
            f.write("print('hello')")

        hash_val = IntegrityChecker().compute_sha256(test_file)
        os.makedirs("updates", exist_ok=True)
        with open("updates/hashlist.json", "w") as f:
            json.dump({"files": {test_file: hash_val}}, f)

        checker = IntegrityChecker()
        assert checker.verify_full() is True

        with open(test_file, "w") as f:
            f.write("corrupted")
        assert checker.verify_full() is False
