"""
Cursor-Sentinel: Utility Functions
Backup, privilege escalation, and helper functions
"""

import os
import sys
import platform
import ctypes
import subprocess
from pathlib import Path
from typing import Tuple, Optional


def is_admin() -> bool:
    """Check if running with administrator/root privileges"""
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def request_admin_privileges() -> Tuple[bool, str]:
    """Request administrator/root privileges (Windows/Mac/Linux)"""
    if is_admin():
        return True, "Already running with admin privileges"
    
    try:
        if platform.system() == "Windows":
            # Re-run with admin privileges
            if sys.argv[-1] != 'asadmin':
                script = os.path.abspath(sys.argv[0])
                params = ' '.join([f'"{x}"' for x in sys.argv[1:]])
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, f'"{script}" {params} asadmin',
                    None, 1
                )
                return False, "Requesting admin privileges... (new window will open)"
            else:
                return True, "Running with admin privileges"
        
        elif platform.system() == "Darwin":  # macOS
            # macOS requires AppleScript or osascript to request admin
            script_path = Path(__file__).parent / "request_admin.sh"
            # Create a simple script that requests sudo
            return False, "macOS: Please run with sudo: sudo python " + " ".join(sys.argv)
        
        else:  # Linux
            # Try to use pkexec or gksudo
            script = os.path.abspath(sys.argv[0])
            try:
                subprocess.run(["pkexec", sys.executable, script] + sys.argv[1:])
                return True, "Running with root privileges (pkexec)"
            except FileNotFoundError:
                return False, "Linux: Please run with sudo: sudo python " + " ".join(sys.argv)
    
    except Exception as e:
        return False, f"Failed to request privileges: {str(e)}"


def create_backup(source_path: Path, backup_dir: Path, suffix: str = "") -> Tuple[bool, Optional[Path]]:
    """Create a timestamped backup of a file or directory"""
    try:
        import zipfile
        from datetime import datetime
        
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if source_path.is_file():
            backup_path = backup_dir / f"{source_path.stem}_{timestamp}{suffix}{source_path.suffix}.backup"
            import shutil
            shutil.copy2(source_path, backup_path)
            return True, backup_path
        
        elif source_path.is_dir():
            backup_path = backup_dir / f"{source_path.name}_{timestamp}{suffix}.zip"
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(source_path)
                        zipf.write(file_path, arcname)
            return True, backup_path
        
        return False, None
    
    except Exception as e:
        return False, None


def restore_backup(backup_path: Path, target_path: Path) -> Tuple[bool, str]:
    """Restore a file or directory from backup"""
    try:
        import shutil
        
        if backup_path.suffix == '.zip':
            import zipfile
            if target_path.exists():
                shutil.rmtree(target_path)
            target_path.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(target_path.parent)
            return True, f"Restored from {backup_path.name}"
        else:
            if target_path.is_dir():
                shutil.rmtree(target_path)
            elif target_path.exists():
                target_path.unlink()
            
            shutil.copy2(backup_path, target_path)
            return True, f"Restored from {backup_path.name}"
    
    except Exception as e:
        return False, f"Restore failed: {str(e)}"


def get_system_info() -> dict:
    """Get system information"""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "is_admin": is_admin()
    }


def log_message(message: str, level: str = "INFO") -> str:
    """Format log message with timestamp"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] [{level}] {message}"


def safe_delete(path: Path) -> Tuple[bool, str]:
    """Safely delete a file or directory"""
    try:
        if path.is_file():
            path.unlink()
            return True, f"Deleted file: {path.name}"
        elif path.is_dir():
            import shutil
            shutil.rmtree(path)
            return True, f"Deleted directory: {path.name}"
        else:
            return False, "Path does not exist"
    except PermissionError:
        return False, "Permission denied. May need admin privileges."
    except Exception as e:
        return False, f"Delete failed: {str(e)}"


def get_cursor_processes() -> list:
    """Get list of running Cursor processes"""
    processes = []
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq Cursor.exe", "/FO", "CSV"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if "Cursor.exe" in result.stdout:
                processes.append("Cursor.exe")
        else:
            result = subprocess.run(
                ["pgrep", "-f", "Cursor"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                processes.append("Cursor")
    except Exception:
        pass
    
    return processes


def ensure_directory(path: Path) -> bool:
    """Ensure directory exists, create if not"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def validate_json_file(file_path: Path) -> Tuple[bool, Optional[dict]]:
    """Validate and parse JSON file"""
    try:
        import json
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, data
    except json.JSONDecodeError as e:
        return False, None
    except Exception:
        return False, None
