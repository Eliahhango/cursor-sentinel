"""
Cursor-Sentinel: Build Script
PyInstaller configuration for creating standalone executables
"""

import PyInstaller.__main__
import sys
import platform
from pathlib import Path

# Build configuration
APP_NAME = "Cursor-Sentinel"
MAIN_SCRIPT = "main_gui.py"
ICON_PATH = None  # Optional: path to .ico file

# Determine OS-specific settings
if platform.system() == "Windows":
    EXE_EXT = ".exe"
    ICON_EXT = ".ico"
elif platform.system() == "Darwin":
    EXE_EXT = ".app"
    ICON_EXT = ".icns"
else:
    EXE_EXT = ""
    ICON_EXT = ".png"

# PyInstaller arguments
args = [
    MAIN_SCRIPT,
    '--name', APP_NAME,
    '--onefile',
    '--windowed',  # No console window (GUI app)
    '--clean',
    '--noconfirm',
]

# Add icon if available
if ICON_PATH and Path(ICON_PATH).exists():
    args.extend(['--icon', ICON_PATH])

# Add hidden imports (if needed)
hidden_imports = [
    'customtkinter',
    'playwright',
    'playwright.async_api',
]

for module in hidden_imports:
    args.extend(['--hidden-import', module])

# Add data files if needed
# args.extend(['--add-data', 'path/to/data;data'])

# macOS-specific
if platform.system() == "Darwin":
    args.extend([
        '--osx-bundle-identifier', 'com.cursorsentinel.app',
    ])

# Windows-specific
if platform.system() == "Windows":
    args.extend([
        '--uac-admin',  # Request admin privileges
    ])

print(f"Building {APP_NAME} for {platform.system()}...")
print(f"Arguments: {args}")

try:
    PyInstaller.__main__.run(args)
    print(f"\n✅ Build completed successfully!")
    print(f"Executable: dist/{APP_NAME}{EXE_EXT}")
except Exception as e:
    print(f"\n❌ Build failed: {e}")
    sys.exit(1)
