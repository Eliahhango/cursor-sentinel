```
██████╗██╗   ██╗███████╗██████╗ ████████╗ ██████╗ ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗ ██████╗ █████╗ ██╗
██╔════╝██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██╔══██╗██║
██║     ██║   ██║███████╗██████╔╝   ██║   ██║   ██║███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║██║     ███████║██║
██║     ██║   ██║╚════██║██╔══██╗   ██║   ██║   ██║╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██║     ██╔══██║██║
╚██████╗╚██████╔╝███████║██║  ██║   ██║   ╚██████╔╝███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║╚██████╗██║  ██║██║
╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚═╝
              ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗ ██████╗ ██╗     ███████╗
              ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝ ██║     ██╔════╝
              ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║██║  ███╗██║     ███████╗
              ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██║   ██║██║     ╚════██║
              ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║╚██████╔╝███████╗███████║
              ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝
```

**Comprehensive cross-platform Desktop Application for managing and resetting Cursor AI identifiers.**

---

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/Eliahhango/elitechwiz-clone-the-repository.git
cd Cursor-Sentinel

# Install dependencies
pip install -r requirements.txt

# Install Playwright (for account creator)
playwright install chromium

# Run the application
python main_gui.py
```

---

## 🎯 Core Features

### Deep Reset Engine

Reset `machineId`, `macMachineId`, and `devDeviceId` in storage.json with multi-layered approach:

- **Storage Reset**: Direct modification of Cursor's storage.json
- **OS Spoofing**: Windows Registry, macOS/Linux UUID manipulation
- **Process Automation**: Auto-kill Cursor processes before reset
- **Smart Backups**: Automatic timestamped backups before any changes

### Immortality Mode

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ██╗███╗   ███╗███╗   ███╗ ██████╗ ██████╗ ████████╗ █████╗  ║
║  ██║████╗ ████║████╗ ████║██╔═══██╗██╔══██╗╚══██╔══╝██╔══██╗ ║
║  ██║██╔████╔██║██╔████╔██║██║   ██║██████╔╝   ██║   ███████║ ║
║  ██║██║╚██╔╝██║██║╚██╔╝██║██║   ██║██╔══██╗   ██║   ██╔══██║ ║
║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║   ██║  ██║ ║
║  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

Block Cursor's auto-update servers permanently:
- Hosts file modification (`127.0.0.1 download.todesktop.com`)
- Directory protection (read-only/immutable updater folder)
- Complete update prevention

### Profile Switcher

Save multiple identity profiles and switch between them like browser profiles. Perfect for managing different identities:

- Save current identity as profile
- Quick profile switching
- Export/import profiles
- Multiple identity management

### Automated Account Creator

```
      ╔════════════════════════════════════╗
      ║  [*]  Automated Account Creation   ║
      ╚════════════════════════════════════╝
              │
              ├─► Temporary Email Service
              ├─► Auto Registration
              ├─► Email Verification
              └─► Desktop Login
```

One-click account creation using Playwright automation:
- Opens temporary email service
- Registers new Cursor account
- Verifies email automatically
- Logs into desktop app

### Workbench Patcher

Patch `workbench.js` to bypass version-locked telemetry checks (Cursor v0.45+):
- Disable telemetry
- Bypass version checks
- Disable update checks

---

## 🚀 Advanced Features

### Backup Manager

View, restore, and manage all backups with detailed metadata. Features include:

- List all backups with size and date
- Restore any backup
- Delete old backups
- Export backups
- Automatic cleanup

### Statistics Dashboard

```
╔═══════════════════════════════════════════╗
║  OPERATION STATISTICS                     ║
║  ────────────────────────────────         ║
║  Total Resets:          [████████] 42    ║
║  Total Backups:         [█████]    25    ║
║  Profile Switches:      [███]      12    ║
║  Immortality Activations: [████]   18    ║
║  Workbench Patches:     [██]       8     ║
║  Account Creations:     [█]        3     ║
╚═══════════════════════════════════════════╝
```

Track all operations with comprehensive statistics:
- Operation history (last 1000 operations)
- Success rate tracking
- Usage statistics
- Export statistics

### Auto Scheduler

Schedule automatic resets and backups:
- Configurable intervals (hours)
- Multiple schedules
- Enable/disable schedules
- Background scheduler

### Browser Cleaner

Clear browser data related to Cursor:
- Detect browser data locations
- Clear browser cache
- Find Cursor-related cookies
- Cross-platform support

### CLI Interface

Full command-line interface for automation:

```bash
# Reset identifiers
python cli.py reset --backup

# List profiles
python cli.py profile --list

# Apply profile
python cli.py profile --apply MyProfile

# Enable Immortality Mode
python cli.py blocker --enable

# View statistics
python cli.py statistics

# List backups
python cli.py backup-manager --list

# Restore backup
python cli.py backup-manager --restore backup_name
```

---

## 📦 Installation

**Prerequisites:**
- Python 3.8 or higher
- Cursor AI installed on your system

**Step 1: Clone Repository**
```bash
git clone https://github.com/Eliahhango/elitechwiz-clone-the-repository.git
cd Cursor-Sentinel
```

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

**Step 3: Run Application**
```bash
python main_gui.py
```

---

## 💻 Usage

### GUI Mode

Launch the application and use the modern dark-themed dashboard:

1. **Quick Reset**: Click the big "QUICK RESET" button to reset all identifiers
2. **Immortality Mode**: Toggle "Block Updates" to enable update blocking
3. **Profile Manager**: Click "Profile Manager" to save/switch identities
4. **Backup Manager**: View and restore backups
5. **Statistics**: View operation statistics
6. **Auto Scheduler**: Schedule automatic operations
7. **Browser Cleaner**: Clear browser data

### CLI Mode

All features accessible via command line:

```bash
python cli.py [command] [options]
```

Available commands:
- `reset` - Reset identifiers
- `backup` - Create backup
- `profile` - Manage profiles
- `blocker` - Manage Immortality Mode
- `backup-manager` - Manage backups
- `statistics` - View statistics
- `patch` - Patch workbench.js

---

## 🔧 Building Standalone Executable

Build a standalone executable for easy distribution:

**Windows:**
```bash
python build.py
# Output: dist/Cursor-Sentinel.exe
```

**macOS:**
```bash
python build.py
# Output: dist/Cursor-Sentinel.app
```

**Linux:**
```bash
python build.py
# Output: dist/Cursor-Sentinel
```

**Note**: Some features require administrator/root privileges:
- Registry modifications (Windows)
- Hosts file modifications
- Directory protection (macOS/Linux)
- Workbench patching

---

## 📁 Project Structure

```
Cursor-Sentinel/
├── main_gui.py           # Main GUI application
├── reset_engine.py       # Core reset logic
├── network_blocker.py    # Immortality mode
├── account_creator.py    # Automated account creation
├── workbench_patcher.py  # Workbench.js patching
├── profile_manager.py    # Profile switching
├── backup_manager.py     # Backup management
├── statistics_tracker.py # Statistics tracking
├── auto_scheduler.py     # Auto scheduling
├── browser_cleaner.py    # Browser data cleaning
├── cli.py                # Command line interface
├── ascii_art.py          # ASCII art module
├── utils.py              # Utility functions
├── build.py              # Build script
└── requirements.txt      # Dependencies
```

---

## 🔒 Security & Privacy

**Automatic Backups**: All modifications are backed up before changes

**Zero Telemetry**: Application does not collect or send any data

**Local Storage**: All profiles and backups stored locally

**Optional Privilege Escalation**: Admin privileges only when needed

---

## 🛠️ Troubleshooting

**"Need Administrator privileges"**
- Windows: Right-click and "Run as administrator"
- macOS/Linux: Run with `sudo python main_gui.py`

**"Playwright not installed"**
```bash
pip install playwright
playwright install chromium
```

**"workbench.js not found"**
- Make sure Cursor is installed
- Some features require Cursor to be closed first

**"Profile not applying"**
- Ensure Cursor is closed before applying profile
- Check that storage.json path is correct

---

## ⚠️ Disclaimer

This tool is for educational and privacy purposes. Use responsibly and in accordance with Cursor AI's terms of service. The developers are not responsible for any misuse of this software.

---

## 📝 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Contributions welcome! Feel free to submit issues or pull requests.

## 📧 Support

For issues or questions, please open an issue on the repository.

---

```
═══════════════════════════════════════════════════════════════════════
                    Made for privacy-conscious developers
═══════════════════════════════════════════════════════════════════════
```
