# 🚀 Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install Playwright (for Account Creator feature)
```bash
playwright install chromium
```

### Step 3: Run the Application
```bash
python main_gui.py
```

## First Use

1. **Check System Status**: The dashboard shows your current system ID health
2. **Quick Reset**: Click the big "⚡ QUICK RESET" button to reset all identifiers
3. **Enable Immortality Mode**: Toggle "🔒 Block Updates" to prevent auto-updates
4. **Create Profile**: Use Profile Manager to save your current identity

## Admin Privileges

Some features require administrator/root privileges:
- **Windows**: Right-click → "Run as administrator"
- **macOS/Linux**: `sudo python main_gui.py`

**Note**: The app will request privileges when needed, or click the "🔐 Request Admin" button.

## Building Standalone Executable

```bash
python build.py
```

The executable will be in the `dist/` directory:
- **Windows**: `Cursor-Sentinel.exe`
- **macOS**: `Cursor-Sentinel.app`
- **Linux**: `Cursor-Sentinel`

## Features Overview

| Feature | Description | Admin Required |
|---------|-------------|----------------|
| **Quick Reset** | Reset all identifiers | Optional |
| **Immortality Mode** | Block updates | ✅ Yes |
| **Workbench Patch** | Disable telemetry | ✅ Yes |
| **Account Creator** | Auto-create accounts | ❌ No |
| **Profile Manager** | Save/switch identities | ❌ No |

## Troubleshooting

**"Module not found"**
- Run: `pip install -r requirements.txt`

**"Playwright not installed"**
- Run: `playwright install chromium`

**"Need Admin privileges"**
- Windows: Run as administrator
- macOS/Linux: Use `sudo`

**"Cursor processes not closing"**
- Manually close Cursor before reset
- Check Task Manager (Windows) or Activity Monitor (macOS)

## Support

For issues, check the main README.md file or open an issue on GitHub.

---

**Happy resetting! 🛡️**
