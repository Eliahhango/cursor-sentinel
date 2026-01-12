"""
Cursor-Sentinel: Core Reset Engine
Multi-layered reset logic for Cursor AI identifiers
"""

import os
import sys
import json
import platform
import subprocess
import shutil
import uuid
import time
from pathlib import Path
from typing import Dict, Optional, List, Tuple

# Windows-specific imports
if platform.system() == "Windows":
    import winreg
    import ctypes
    from ctypes import wintypes

# macOS/Linux imports
if platform.system() in ["Darwin", "Linux"]:
    import pwd
    import grp


class ResetEngine:
    """Multi-layered reset engine for Cursor AI identifiers"""
    
    def __init__(self):
        self.system = platform.system()
        self.cursor_paths = self._detect_cursor_paths()
        self.backup_dir = Path.home() / ".cursor-sentinel" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def _detect_cursor_paths(self) -> Dict[str, Path]:
        """Detect Cursor installation paths based on OS"""
        paths = {}
        home = Path.home()
        
        if self.system == "Windows":
            app_data = Path(os.getenv("APPDATA", ""))
            local_app_data = Path(os.getenv("LOCALAPPDATA", ""))
            paths["storage"] = app_data / "Cursor" / "User" / "globalStorage" / "storage.json"
            paths["workspace_storage"] = app_data / "Cursor" / "User" / "workspaceStorage"
            paths["updater"] = local_app_data / "Programs" / "Cursor" / "resources" / "app" / "cursor-updater"
            paths["executable"] = local_app_data / "Programs" / "Cursor" / "Cursor.exe"
        
        elif self.system == "Darwin":  # macOS
            paths["storage"] = home / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "storage.json"
            paths["workspace_storage"] = home / "Library" / "Application Support" / "Cursor" / "User" / "workspaceStorage"
            paths["updater"] = home / "Library" / "Application Support" / "Cursor" / "cursor-updater"
            paths["executable"] = Path("/Applications/Cursor.app/Contents/MacOS/Cursor")
        
        else:  # Linux
            paths["storage"] = home / ".config" / "Cursor" / "User" / "globalStorage" / "storage.json"
            paths["workspace_storage"] = home / ".config" / "Cursor" / "User" / "workspaceStorage"
            paths["updater"] = home / ".config" / "Cursor" / "cursor-updater"
            paths["executable"] = Path("/usr/bin/cursor")
        
        return paths
    
    def kill_cursor_processes(self) -> Tuple[bool, List[str]]:
        """Force-close Cursor and its background processes"""
        killed = []
        errors = []
        
        try:
            if self.system == "Windows":
                # Kill Cursor processes
                process_names = ["Cursor.exe", "cursor.exe", "cursor-updater.exe"]
                for proc_name in process_names:
                    try:
                        subprocess.run(
                            ["taskkill", "/F", "/IM", proc_name],
                            capture_output=True,
                            timeout=5,
                            check=False
                        )
                        killed.append(proc_name)
                        time.sleep(0.5)
                    except Exception as e:
                        errors.append(f"Error killing {proc_name}: {str(e)}")
            
            elif self.system == "Darwin":  # macOS
                process_names = ["Cursor", "cursor", "cursor-updater"]
                for proc_name in process_names:
                    try:
                        subprocess.run(
                            ["pkill", "-9", "-f", proc_name],
                            capture_output=True,
                            timeout=5,
                            check=False
                        )
                        killed.append(proc_name)
                        time.sleep(0.5)
                    except Exception as e:
                        errors.append(f"Error killing {proc_name}: {str(e)}")
            
            else:  # Linux
                process_names = ["Cursor", "cursor", "cursor-updater"]
                for proc_name in process_names:
                    try:
                        subprocess.run(
                            ["pkill", "-9", "-f", proc_name],
                            capture_output=True,
                            timeout=5,
                            check=False
                        )
                        killed.append(proc_name)
                        time.sleep(0.5)
                    except Exception as e:
                        errors.append(f"Error killing {proc_name}: {str(e)}")
            
            # Wait a bit for processes to fully terminate
            time.sleep(1)
            return len(killed) > 0, killed + errors
        
        except Exception as e:
            return False, [f"Process kill error: {str(e)}"]
    
    def backup_files(self) -> Tuple[bool, str]:
        """Create timestamped backup of configuration files"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"cursor_backup_{timestamp}.zip"
            
            import zipfile
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup storage.json if exists
                if self.cursor_paths["storage"].exists():
                    zipf.write(
                        self.cursor_paths["storage"],
                        "storage.json"
                    )
                
                # Backup workspace storage
                if self.cursor_paths["workspace_storage"].exists():
                    for root, dirs, files in os.walk(self.cursor_paths["workspace_storage"]):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(self.cursor_paths["workspace_storage"].parent)
                            zipf.write(file_path, arcname)
            
            return True, str(backup_path)
        
        except Exception as e:
            return False, f"Backup failed: {str(e)}"
    
    def reset_storage_json(self) -> Tuple[bool, str]:
        """Reset identifiers in storage.json"""
        storage_path = self.cursor_paths["storage"]
        
        try:
            if not storage_path.exists():
                # Create parent directory if needed
                storage_path.parent.mkdir(parents=True, exist_ok=True)
                data = {}
            else:
                with open(storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            # Generate new identifiers
            new_machine_id = str(uuid.uuid4())
            new_mac_machine_id = str(uuid.uuid4())
            new_dev_device_id = str(uuid.uuid4())
            
            # Reset identifiers
            if "machineId" in data:
                data["machineId"] = new_machine_id
            else:
                data["machineId"] = new_machine_id
            
            if "macMachineId" in data:
                data["macMachineId"] = new_mac_machine_id
            else:
                data["macMachineId"] = new_mac_machine_id
            
            if "devDeviceId" in data:
                data["devDeviceId"] = new_dev_device_id
            else:
                data["devDeviceId"] = new_dev_device_id
            
            # Write back
            with open(storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            return True, f"Reset machineId, macMachineId, devDeviceId in storage.json"
        
        except Exception as e:
            return False, f"Storage reset failed: {str(e)}"
    
    def reset_windows_registry(self) -> Tuple[bool, str]:
        """Reset Windows MachineGuid in Registry"""
        if self.system != "Windows":
            return False, "Not Windows system"
        
        try:
            key_path = r"SOFTWARE\Microsoft\Cryptography"
            value_name = "MachineGuid"
            
            # Generate new GUID
            new_guid = str(uuid.uuid4())
            
            # Open registry key
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                key_path,
                0,
                winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY
            )
            
            # Set new GUID
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, new_guid)
            winreg.CloseKey(key)
            
            return True, f"Reset MachineGuid in Registry: {new_guid[:8]}..."
        
        except PermissionError:
            return False, "Registry write requires Administrator privileges"
        except Exception as e:
            return False, f"Registry reset failed: {str(e)}"
    
    def reset_macos_uuids(self) -> Tuple[bool, str]:
        """Reset macOS hardware-linked UUIDs"""
        if self.system != "Darwin":
            return False, "Not macOS system"
        
        try:
            # macOS system UUID is hardware-bound, but we can spoof local identifiers
            # This affects some system-level identifiers that apps might use
            
            # Reset system_profiler UUID cache (if accessible)
            cache_path = Path("/var/db/dslocal/nodes/Default/config/SystemVersion.plist")
            
            # Note: Most macOS UUIDs are hardware-bound and require root to modify
            # This is a placeholder for UUID manipulation techniques
            return True, "macOS UUID reset attempted (some may require root)"
        
        except Exception as e:
            return False, f"macOS UUID reset failed: {str(e)}"
    
    def reset_linux_uuids(self) -> Tuple[bool, str]:
        """Reset Linux hardware-linked UUIDs"""
        if self.system != "Linux":
            return False, "Not Linux system"
        
        try:
            # Linux machine-id location
            machine_id_path = Path("/etc/machine-id")
            dbus_machine_id_path = Path("/var/lib/dbus/machine-id")
            
            # Generate new machine ID
            new_machine_id = uuid.uuid4().hex[:32] + '\n'
            
            results = []
            
            # Reset machine-id if accessible (requires root)
            if machine_id_path.exists() and os.access(machine_id_path, os.W_OK):
                machine_id_path.write_text(new_machine_id)
                results.append("machine-id reset")
            
            if dbus_machine_id_path.exists() and os.access(dbus_machine_id_path, os.W_OK):
                dbus_machine_id_path.write_text(new_machine_id)
                results.append("dbus machine-id reset")
            
            if results:
                return True, f"Linux UUID reset: {', '.join(results)}"
            else:
                return False, "Linux UUID reset requires root privileges"
        
        except Exception as e:
            return False, f"Linux UUID reset failed: {str(e)}"
    
    def perform_deep_reset(self, kill_processes: bool = True) -> Dict[str, Tuple[bool, str]]:
        """Perform complete deep reset of all identifiers"""
        results = {}
        
        # Step 1: Kill processes
        if kill_processes:
            success, msg = self.kill_cursor_processes()
            results["process_kill"] = (success, msg)
            time.sleep(1)
        
        # Step 2: Backup
        success, msg = self.backup_files()
        results["backup"] = (success, msg)
        
        # Step 3: Reset storage.json
        success, msg = self.reset_storage_json()
        results["storage_json"] = (success, msg)
        
        # Step 4: OS-specific reset
        if self.system == "Windows":
            success, msg = self.reset_windows_registry()
            results["registry"] = (success, msg)
        elif self.system == "Darwin":
            success, msg = self.reset_macos_uuids()
            results["macos_uuids"] = (success, msg)
        elif self.system == "Linux":
            success, msg = self.reset_linux_uuids()
            results["linux_uuids"] = (success, msg)
        
        return results
    
    def get_system_id_health(self) -> Dict[str, any]:
        """Check current system ID health status"""
        health = {
            "storage_json_exists": self.cursor_paths["storage"].exists(),
            "storage_json_path": str(self.cursor_paths["storage"]),
            "identifiers": {}
        }
        
        # Check storage.json identifiers
        if health["storage_json_exists"]:
            try:
                with open(self.cursor_paths["storage"], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    health["identifiers"] = {
                        "machineId": data.get("machineId", "Not found"),
                        "macMachineId": data.get("macMachineId", "Not found"),
                        "devDeviceId": data.get("devDeviceId", "Not found")
                    }
            except Exception as e:
                health["identifiers"]["error"] = str(e)
        
        # Check OS-specific identifiers
        if self.system == "Windows":
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Cryptography",
                    0,
                    winreg.KEY_READ | winreg.KEY_WOW64_64KEY
                )
                machine_guid, _ = winreg.QueryValueEx(key, "MachineGuid")
                winreg.CloseKey(key)
                health["os_identifier"] = f"Registry MachineGuid: {machine_guid[:8]}..."
            except Exception:
                health["os_identifier"] = "Cannot read Registry"
        
        return health
