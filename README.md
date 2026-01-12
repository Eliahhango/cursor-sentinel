```
██████╗██╗   ██╗███████╗██████╗ ████████╗ ██████╗ ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗ ██████╗ █████╗ ██╗
██╔════╝██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██╔══██╗██║
██║     ██║   ██║███████╗██████╔╝   ██║   ██║   ██║███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║██║     ███████║██║
██║     ██║   ██║╚════██║██╔══██╗   ██║   ██║   ██║╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██║     ██╔══██║██║
╚██████╗╚██████╔╝███████║██║  ██║   ██║   ╚██████╔╝███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║╚██████╗██║  ██║██║
╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝
```

**Comprehensive cross-platform Desktop Application for managing and resetting Cursor AI identifiers.**

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                        [ FEATURES OVERVIEW ]                         ║
╚══════════════════════════════════════════════════════════════════════╝
```

## Core Reset Logic

```
┌─────────────────────────────────────────────────────────────────────┐
│ [1] Deep Reset                                                      │
│      • Reset machineId, macMachineId, and devDeviceId              │
│      • Located in storage.json                                      │
│                                                                      │
│ [2] OS Spoofing                                                     │
│      • Windows: Regenerate Cryptography\MachineGuid in Registry    │
│      • macOS/Linux: Spoof hardware-linked UUIDs                    │
│                                                                      │
│ [3] Process Automator                                               │
│      • Automatically detect Cursor processes                        │
│      • Force-close Cursor and background updaters                  │
│      • Ensures clean reset environment                              │
└─────────────────────────────────────────────────────────────────────┘
```

## Advanced Features

```
┌─────────────────────────────────────────────────────────────────────┐
│ >>> IMMORTALITY MODE                                                │
│    • Block Cursor's auto-update servers                             │
│    • Modify system hosts file (download.todesktop.com)             │
│    • Make cursor-updater directory read-only/immutable             │
│                                                                      │
│ >>> ONE-CLICK ACCOUNT CREATOR                                       │
│    • Automated browser flow using Playwright                        │
│    • Opens temporary email service                                  │
│    • Registers new Cursor account automatically                     │
│    • Auto-logs into desktop app                                     │
│                                                                      │
│ >>> WORKBENCH FIXER                                                 │
│    • Patch workbench.js to bypass telemetry checks                 │
│    • Compatible with Cursor v0.45+                                  │
│    • Version-locked telemetry bypass                                │
│                                                                      │
│ >>> PROFILE SWITCHER                                                │
│    • Save multiple identity profiles                                │
│    • Switch between identities like browser profiles               │
│    • Export/import profile bundles                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Modern GUI

```
┌─────────────────────────────────────────────────────────────────────┐
│ Dashboard Elements:                                                 │
│                                                                      │
│ [■] Status Indicators        →  System ID Health monitoring         │
│ [■] Quick Reset Button       →  Giant button with progress bar     │
│ [■] Log Terminal Window      →  Real-time file modifications       │
│ [■] Toggle Switches          →  Block Updates, Auto-Cleanup        │
│ [■] Dark Theme              →  CustomTkinter modern interface      │
└─────────────────────────────────────────────────────────────────────┘
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                         [ INSTALLATION ]                             ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Prerequisites

```
REQUIRED:
  • Python 3.8 or higher
  • Cursor AI installed on your system
```

### Setup

**Step 1: Clone or download this repository**

```bash
cd Cursor-Sentinel
```

**Step 2: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 3: Install Playwright browsers** (for account creator feature)

```bash
playwright install chromium
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                           [ USAGE ]                                  ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Running the Application

**From source:**

```bash
python main_gui.py
```

**As standalone executable:**

```bash
python build.py
# Executable will be in dist/ directory
```

### Quick Start Guide

```
┌─────────────────────────────────────────────────────────────────────┐
│ QUICK START:                                                        │
│                                                                      │
│ 1. [QUICK RESET]                                                    │
│    Click the "QUICK RESET" button to reset all identifiers         │
│                                                                      │
│ 2. [IMMORTALITY MODE]                                               │
│    Toggle "Block Updates" to enable update blocking                │
│                                                                      │
│ 3. [PROFILE MANAGER]                                                │
│    Click "Profile Manager" to save/switch identities               │
│                                                                      │
│ 4. [CREATE ACCOUNT]                                                 │
│    Use "Create Account" for automated account creation             │
└─────────────────────────────────────────────────────────────────────┘
```

### Features Guide

```
┌─── QUICK RESET ───────────────────────────────────────────────────┐
│                                                                     │
│  • Kills all Cursor processes                                       │
│  • Creates automatic timestamped backup                             │
│  • Resets storage.json identifiers                                  │
│  • Performs OS-specific identifier reset                            │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘

┌─── IMMORTALITY MODE ───────────────────────────────────────────────┐
│                                                                     │
│  • Blocks update servers in hosts file                              │
│    → 127.0.0.1 download.todesktop.com                              │
│  • Makes updater directory read-only/immutable                      │
│  • Prevents automatic updates completely                            │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘

┌─── PROFILE MANAGER ────────────────────────────────────────────────┐
│                                                                     │
│  • Save current identity as a profile                               │
│  • Switch between saved profiles                                    │
│  • Export/import profiles                                           │
│  • Multiple identity support                                        │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘

┌─── WORKBENCH PATCHER ───────────────────────────────────────────────┐
│                                                                     │
│  • Patches workbench.js to disable telemetry                        │
│  • Bypasses version checks                                          │
│  • Requires administrator/root privileges                           │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘

┌─── ACCOUNT CREATOR ─────────────────────────────────────────────────┐
│                                                                     │
│  • Automated account creation using Playwright                      │
│  • Uses temporary email services                                    │
│  • Automatically verifies email                                     │
│  • Saves credentials to profile                                     │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║              [ BUILDING STANDALONE EXECUTABLE ]                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Windows

```bash
python build.py
# Output: dist/Cursor-Sentinel.exe
```

### macOS

```bash
python build.py
# Output: dist/Cursor-Sentinel.app
```

### Linux

```bash
python build.py
# Output: dist/Cursor-Sentinel
```

```
╔══════════════════════════════════════════════════════════════════════╗
║                         IMPORTANT NOTE                               ║
╚══════════════════════════════════════════════════════════════════════╝
Some features require administrator/root privileges:
  • Registry modifications (Windows)
  • Hosts file modifications
  • Directory protection (macOS/Linux)
  • Workbench patching
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                      [ PROJECT STRUCTURE ]                           ║
╚══════════════════════════════════════════════════════════════════════╝
```

```
Cursor-Sentinel/
├── main_gui.py           # Main GUI application
├── reset_engine.py       # Core reset logic
├── network_blocker.py    # Immortality mode (hosts file, directory protection)
├── account_creator.py    # Automated account creation
├── workbench_patcher.py  # Workbench.js patching
├── profile_manager.py    # Profile switching
├── utils.py              # Utility functions
├── build.py              # Build script
├── requirements.txt      # Dependencies
└── README.md             # This file
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                    [ SECURITY & PRIVACY ]                            ║
╚══════════════════════════════════════════════════════════════════════╝
```

```
┌─────────────────────────────────────────────────────────────────────┐
│ • Automatic Backups:      All modifications backed up before changes│
│ • Zero Telemetry:         Application does not collect any data     │
│ • Local Storage:          All profiles and backups stored locally   │
│ • Privilege Escalation:   Admin privileges only when needed         │
└─────────────────────────────────────────────────────────────────────┘
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                      [ TROUBLESHOOTING ]                             ║
╚══════════════════════════════════════════════════════════════════════╝
```

```
PROBLEM: "Need Administrator privileges"
SOLUTION:
  • Windows:  Right-click and "Run as administrator"
  • macOS:    Run with: sudo python main_gui.py
  • Linux:    Run with: sudo python main_gui.py

─────────────────────────────────────────────────────────────────────

PROBLEM: "Playwright not installed"
SOLUTION:
  pip install playwright
  playwright install chromium

─────────────────────────────────────────────────────────────────────

PROBLEM: "workbench.js not found"
SOLUTION:
  • Make sure Cursor is installed
  • Some features require Cursor to be closed first

─────────────────────────────────────────────────────────────────────

PROBLEM: "Profile not applying"
SOLUTION:
  • Ensure Cursor is closed before applying profile
  • Check that storage.json path is correct
```

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                         [ DISCLAIMER ]                               ║
╚══════════════════════════════════════════════════════════════════════╝
```

This tool is for educational and privacy purposes. Use responsibly and in accordance with Cursor AI's terms of service. The developers are not responsible for any misuse of this software.

---

```
╔══════════════════════════════════════════════════════════════════════╗
║                        [ INFORMATION ]                               ║
╚══════════════════════════════════════════════════════════════════════╝
```

**License:** This project is provided as-is for educational purposes.

**Contributing:** Contributions welcome! Feel free to submit issues or pull requests.

**Support:** For issues or questions, please open an issue on the repository.

---

```
═══════════════════════════════════════════════════════════════════════
                    Made for privacy-conscious developers
═══════════════════════════════════════════════════════════════════════
```
