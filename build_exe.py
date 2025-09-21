#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build script for creating Windows executable."""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Build the executable using PyInstaller."""
    project_root = Path(os.getcwd())
    spec_file = project_root / "garb_alarm_clock.spec"
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"

    print("Building Windows executable...")
    print(f"Project root: {project_root}")
    print(f"Spec file: {spec_file}")
    print(f"Spec file exists: {spec_file.exists()}")

    # Clean previous builds
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
        print("Cleaned dist directory")

    if build_dir.exists():
        shutil.rmtree(build_dir)
        print("Cleaned build directory")

    # Check if spec file exists
    if not spec_file.exists():
        print(f"Error: Spec file not found at {spec_file}")
        print("Available files:")
        for f in project_root.iterdir():
            print(f"  {f}")
        return 1

    # Run PyInstaller
    cmd = [sys.executable, "-m", "PyInstaller", str(spec_file), "--clean"]

    try:
        result = subprocess.run(cmd, check=True, cwd=project_root)
        print("Build successful!")

        exe_path = dist_dir / "garb_alarm_clock.exe"
        if exe_path.exists():
            print(f"Executable created: {exe_path}")
            print(f"File size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print("Executable not found!")
            return 1

    except subprocess.CalledProcessError as e:
        print(f"Build failed with return code {e.returncode}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())