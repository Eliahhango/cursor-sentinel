"""
Cursor-Sentinel: Network Blocker (Immortality Mode)
Block Cursor's auto-update servers and protect updater directory
"""

import os
import sys
import platform
import subprocess
import stat
from pathlib import Path
from typing import Tuple, List, Optional

if platform.system() == "Windows":
    import winreg


class NetworkBlocker:
    """Block Cursor update servers and protect updater directory"""
    
    def __init__(self):
        self.system = platform.system()
        self.hosts_file = self._get_hosts_file_path()
        self.blocked_domains = [
            "download.todesktop.com",
            "todesktop.com",
            "api.todesktop.com",
            "update.todesktop.com",
            "cdn.todesktop.com"
        ]
        self.marker_start = "# Cursor-Sentinel Block Start"
        self.marker_end = "# Cursor-Sentinel Block End"
    
    def _get_hosts_file_path(self) -> Path:
        """Get hosts file path based on OS"""
        if self.system == "Windows":
            return Path(r"C:\Windows\System32\drivers\etc\hosts")
        else:
            return Path("/etc/hosts")
    
    def _read_hosts_file(self) -> List[str]:
        """Read hosts file content"""
        try:
            with open(self.hosts_file, 'r', encoding='utf-8') as f:
                return f.readlines()
        except PermissionError:
            raise PermissionError(f"Need {self._get_privilege_type()} privileges to modify hosts file")
        except Exception as e:
            raise Exception(f"Failed to read hosts file: {str(e)}")
    
    def _write_hosts_file(self, lines: List[str]) -> None:
        """Write hosts file content"""
        try:
            with open(self.hosts_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except PermissionError:
            raise PermissionError(f"Need {self._get_privilege_type()} privileges to modify hosts file")
        except Exception as e:
            raise Exception(f"Failed to write hosts file: {str(e)}")
    
    def _get_privilege_type(self) -> str:
        """Get privilege type needed"""
        return "Administrator" if self.system == "Windows" else "root"
    
    def is_blocked(self) -> bool:
        """Check if domains are currently blocked"""
        try:
            lines = self._read_hosts_file()
            in_block = False
            
            for line in lines:
                if self.marker_start in line:
                    in_block = True
                if self.marker_end in line:
                    return True  # Block section exists
                if in_block:
                    # Check if any domain is in this line
                    for domain in self.blocked_domains:
                        if domain in line and not line.strip().startswith('#'):
                            return True
            
            return False
        except Exception:
            return False
    
    def block_updates(self) -> Tuple[bool, str]:
        """Block Cursor update domains in hosts file"""
        try:
            lines = self._read_hosts_file()
            
            # Remove existing block if present
            new_lines = []
            in_block = False
            for line in lines:
                if self.marker_start in line:
                    in_block = True
                if self.marker_end in line:
                    in_block = False
                    continue
                if not in_block:
                    new_lines.append(line)
            
            # Add block entries
            new_lines.append("\n")
            new_lines.append(f"{self.marker_start}\n")
            for domain in self.blocked_domains:
                new_lines.append(f"127.0.0.1 {domain}\n")
                new_lines.append(f"::1 {domain}\n")  # IPv6
            new_lines.append(f"{self.marker_end}\n")
            
            self._write_hosts_file(new_lines)
            return True, f"Blocked {len(self.blocked_domains)} update domains"
        
        except PermissionError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Failed to block updates: {str(e)}"
    
    def unblock_updates(self) -> Tuple[bool, str]:
        """Remove block entries from hosts file"""
        try:
            lines = self._read_hosts_file()
            new_lines = []
            in_block = False
            
            for line in lines:
                if self.marker_start in line:
                    in_block = True
                    continue
                if self.marker_end in line:
                    in_block = False
                    continue
                if not in_block:
                    new_lines.append(line)
            
            self._write_hosts_file(new_lines)
            return True, "Removed update blocks from hosts file"
        
        except PermissionError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Failed to unblock updates: {str(e)}"
    
    def protect_updater_directory(self) -> Tuple[bool, str]:
        """Make cursor-updater directory read-only/immutable"""
        from reset_engine import ResetEngine
        
        reset_engine = ResetEngine()
        updater_path = reset_engine.cursor_paths.get("updater")
        
        if not updater_path or not updater_path.exists():
            return False, "Updater directory not found"
        
        try:
            if self.system == "Windows":
                # Windows: Set read-only attribute
                subprocess.run(
                    ["attrib", "+R", "/S", "/D", str(updater_path)],
                    capture_output=True,
                    check=True
                )
                return True, "Updater directory set to read-only (Windows)"
            
            elif self.system in ["Darwin", "Linux"]:
                # macOS/Linux: Use chattr to make immutable (requires root)
                try:
                    subprocess.run(
                        ["chattr", "+i", "-R", str(updater_path)],
                        capture_output=True,
                        check=True,
                        timeout=5
                    )
                    return True, "Updater directory made immutable (chattr +i)"
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Fallback to chmod read-only
                    os.chmod(updater_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
                    # Also make all files read-only
                    for root, dirs, files in os.walk(updater_path):
                        for d in dirs:
                            os.chmod(Path(root) / d, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
                        for f in files:
                            os.chmod(Path(root) / f, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
                    return True, "Updater directory set to read-only (chmod)"
        
        except PermissionError:
            return False, f"Need {self._get_privilege_type()} privileges to protect directory"
        except Exception as e:
            return False, f"Failed to protect directory: {str(e)}"
    
    def unprotect_updater_directory(self) -> Tuple[bool, str]:
        """Remove read-only/immutable protection from updater directory"""
        from reset_engine import ResetEngine
        
        reset_engine = ResetEngine()
        updater_path = reset_engine.cursor_paths.get("updater")
        
        if not updater_path or not updater_path.exists():
            return False, "Updater directory not found"
        
        try:
            if self.system == "Windows":
                # Windows: Remove read-only attribute
                subprocess.run(
                    ["attrib", "-R", "/S", "/D", str(updater_path)],
                    capture_output=True,
                    check=True
                )
                return True, "Read-only protection removed (Windows)"
            
            elif self.system in ["Darwin", "Linux"]:
                # macOS/Linux: Remove immutable flag
                try:
                    subprocess.run(
                        ["chattr", "-i", "-R", str(updater_path)],
                        capture_output=True,
                        check=True,
                        timeout=5
                    )
                    return True, "Immutable protection removed (chattr -i)"
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Fallback: restore write permissions
                    os.chmod(updater_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
                    for root, dirs, files in os.walk(updater_path):
                        for d in dirs:
                            os.chmod(Path(root) / d, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
                        for f in files:
                            os.chmod(Path(root) / f, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
                    return True, "Write permissions restored (chmod)"
        
        except PermissionError:
            return False, f"Need {self._get_privilege_type()} privileges to unprotect directory"
        except Exception as e:
            return False, f"Failed to unprotect directory: {str(e)}"
    
    def enable_immortality_mode(self) -> Tuple[bool, str]:
        """Enable full Immortality Mode (block updates + protect directory)"""
        results = []
        
        # Block updates
        success, msg = self.block_updates()
        results.append(("hosts_block", success, msg))
        
        # Protect directory
        success, msg = self.protect_updater_directory()
        results.append(("directory_protect", success, msg))
        
        all_success = all(r[1] for r in results)
        message = "; ".join([f"{r[0]}: {r[2]}" for r in results])
        
        return all_success, message
    
    def disable_immortality_mode(self) -> Tuple[bool, str]:
        """Disable Immortality Mode (unblock updates + unprotect directory)"""
        results = []
        
        # Unblock updates
        success, msg = self.unblock_updates()
        results.append(("hosts_unblock", success, msg))
        
        # Unprotect directory
        success, msg = self.unprotect_updater_directory()
        results.append(("directory_unprotect", success, msg))
        
        all_success = all(r[1] for r in results)
        message = "; ".join([f"{r[0]}: {r[2]}" for r in results])
        
        return all_success, message
