import os
import json
import tempfile
from core.integrity import IntegrityChecker

def test_integrity_verification():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)

        # Create protected file
        test_file = "core/media.py"
        os.makedirs("core", exist_ok=True)
        with open(test_file, "w") as f:
            f.write("print('hello')")

        # Generate hashlist
        hasher = IntegrityChecker()
        hash_val = hasher.compute_sha256(test_file)
        hashlist = {"files": {test_file: hash_val}}
        os.makedirs("updates", exist_ok=True)
        with open("updates/hashlist.json", "w") as f:
            json.dump(hashlist, f)

        # Verify
        checker = IntegrityChecker()
        assert checker.verify_full() == True

        # Corrupt file
        with open(test_file, "w") as f:
            f.write("corrupted")

        assert checker.verify_full() == False
