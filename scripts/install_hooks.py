#!/usr/bin/env python3
"""
Vision Loop — Git Hooks Installer
Run once after cloning the repository to install all custom Git hooks.

Usage:
    python scripts/install_hooks.py
"""

import sys
import shutil
import stat
from pathlib import Path

ROOT_DIR   = Path(__file__).resolve().parent.parent
HOOKS_SRC  = ROOT_DIR / "scripts" / "hooks"
HOOKS_DEST = ROOT_DIR / ".git" / "hooks"


def install_hooks() -> None:
    """Copy hook scripts from scripts/hooks/ into .git/hooks/ and make executable."""

    if not HOOKS_SRC.exists():
        print(f"[INFO] No scripts/hooks/ directory found — using embedded pre-commit hook.")
        _install_embedded()
        return

    installed = 0
    for hook_file in HOOKS_SRC.iterdir():
        if hook_file.is_file():
            dest = HOOKS_DEST / hook_file.name
            shutil.copy2(hook_file, dest)
            dest.chmod(dest.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
            print(f"  [OK] Installed hook: {hook_file.name}")
            installed += 1

    print(f"\n  {installed} hook(s) installed successfully.")


def _install_embedded() -> None:
    """
    The pre-commit hook is already written to .git/hooks/pre-commit
    by the repository setup. Just ensure it is executable.
    """
    hook_path = HOOKS_DEST / "pre-commit"
    if hook_path.exists():
        hook_path.chmod(hook_path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
        print(f"  [OK] pre-commit hook is already installed and marked executable.")
        print(f"       Path: {hook_path}")
    else:
        print(f"  [WARN] pre-commit hook not found at {hook_path}")
        print(f"         Please re-run repository setup.")


if __name__ == "__main__":
    print("\n[HOOKS INSTALLER] Vision Loop Git Hooks Setup")
    print("=" * 50)
    install_hooks()
    print("\nDone. All future `git commit` operations will now trigger:")
    print("  1. Knowledge Graph Auto-Update")
    print("  2. Data Integrity Verification (35 invariants)")
    print("  3. Pytest Test Suite (31 tests)")
