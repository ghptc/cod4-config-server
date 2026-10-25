"""Verify private external inputs without copying or changing them."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    manifest = Path(__file__).resolve().parents[1] / "assets.json"
    failures = []
    for relative, expected in json.loads(manifest.read_text()).items():
        path = args.root / relative
        if not path.is_file():
            failures.append(f"Missing: {relative}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            failures.append(f"Hash mismatch: {relative}")
    if failures:
        parser.exit(1, "\n".join(failures) + "\n")
    print("All 11 external input hashes match; redistribution rights are separate.")


if __name__ == "__main__":
    main()
