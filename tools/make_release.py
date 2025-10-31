import os
import sys
import json
import hashlib
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

def compute_hashes(root_dir):
    hashes = {}
    for file_path in Path(root_dir).rglob("*"):
        if file_path.is_file():
            rel = str(file_path.relative_to(root_dir))
            if any(part.startswith(".") or part == "__pycache__" or part == "updates" for part in file_path.parts):
                continue
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            hashes[rel] = h.hexdigest()
    return hashes

def sign_file(filepath):
    try:
        subprocess.run(["gpg", "--detach-sign", "--armor", filepath], check=True)
        return True
    except Exception:
        print("⚠️ GPG signing failed. Ensure GPG is installed and CeoSolace key is available.")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python tools/make_release.py <version>")
        sys.exit(1)

    version = sys.argv[1]
    archive_base = f"chromavine-studio-pro-{version}"
    staging = Path("release_staging")
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()

    # Copy all app files (exclude dev-only)
    exclude = {".git", "__pycache__", "release_staging", "tools", ".idea", ".vscode"}
    for item in Path(".").iterdir():
        if item.name in exclude:
            continue
        if item.is_dir():
            shutil.copytree(item, staging / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, staging / item.name)

    # Generate hashlist
    hashes = compute_hashes(staging)
    hashlist_path = staging / "hashlist.json"
    with open(hashlist_path, "w") as f:
        json.dump({"generated": datetime.utcnow().isoformat(), "files": hashes}, f, indent=2)

    # Create ZIP
    shutil.make_archive(archive_base, "zip", staging)

    # Sign critical files
    sign_file(f"{archive_base}.zip")
    sign_file(str(hashlist_path))

    # Generate latest.json
    with open(f"{archive_base}.zip", "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    latest = {
        "version": version,
        "url": f"https://updates.chromavine.app/releases/{archive_base}.zip",
        "sha256": sha256,
        "signature_url": f"https://updates.chromavine.app/releases/{archive_base}.zip.sig",
        "hashlist_url": f"https://updates.chromavine.app/releases/hashlist.json"
    }

    with open("latest.json", "w") as f:
        json.dump(latest, f, indent=2)
    sign_file("latest.json")

    print(f"\n✅ Release {version} built successfully!")
    print(f"📦 Archive: {archive_base}.zip")
    print(f"🔐 Signatures: .sig files created")
    print(f"📄 Manifest: latest.json")

if __name__ == "__main__":
    main()
