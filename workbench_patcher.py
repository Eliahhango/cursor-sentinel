"""
Cursor-Sentinel: Workbench Patcher
Patch workbench.js to bypass version-locked telemetry checks
"""

import os
import re
import shutil
from pathlib import Path
from typing import Tuple, Optional, List
import platform


class WorkbenchPatcher:
    """Patch workbench.js to bypass telemetry checks"""
    
    def __init__(self):
        self.system = platform.system()
        self.workbench_paths = self._detect_workbench_paths()
    
    def _detect_workbench_paths(self) -> List[Path]:
        """Detect workbench.js file paths"""
        paths = []
        
        if self.system == "Windows":
            local_app_data = Path(os.getenv("LOCALAPPDATA", ""))
            base_path = local_app_data / "Programs" / "Cursor" / "resources" / "app"
            paths.append(base_path / "out" / "vs" / "workbench" / "workbench.desktop.main.js")
            paths.append(base_path / "out" / "vs" / "workbench" / "workbench.desktop.main.nls.js")
        
        elif self.system == "Darwin":  # macOS
            app_path = Path("/Applications/Cursor.app/Contents/Resources/app")
            paths.append(app_path / "out" / "vs" / "workbench" / "workbench.desktop.main.js")
            paths.append(app_path / "out" / "vs" / "workbench" / "workbench.desktop.main.nls.js")
        
        else:  # Linux
            home = Path.home()
            # Common Linux installation paths
            possible_bases = [
                Path("/opt/cursor/resources/app"),
                home / ".cursor" / "resources" / "app",
            ]
            for base in possible_bases:
                paths.append(base / "out" / "vs" / "workbench" / "workbench.desktop.main.js")
                paths.append(base / "out" / "vs" / "workbench" / "workbench.desktop.main.nls.js")
        
        # Filter to only existing paths
        return [p for p in paths if p.exists()]
    
    def find_workbench_file(self) -> Optional[Path]:
        """Find the main workbench.js file"""
        for path in self.workbench_paths:
            if path.name == "workbench.desktop.main.js" and path.exists():
                return path
        return None
    
    def backup_workbench(self, workbench_path: Path) -> Tuple[bool, Optional[Path]]:
        """Create backup of workbench.js"""
        try:
            backup_dir = Path.home() / ".cursor-sentinel" / "backups" / "workbench"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            backup_path = backup_dir / f"{workbench_path.name}.backup"
            shutil.copy2(workbench_path, backup_path)
            
            return True, backup_path
        except Exception as e:
            return False, None
    
    def patch_telemetry_checks(self, workbench_path: Path) -> Tuple[bool, str]:
        """Patch telemetry and version checks in workbench.js"""
        try:
            # Read file
            with open(workbench_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            modifications = []
            
            # Pattern 1: Disable telemetry
            telemetry_patterns = [
                (r'telemetryService\s*\.\s*setEnabled\([^)]*\)', 'telemetryService.setEnabled(false)'),
                (r'enableTelemetry\s*[:=]\s*true', 'enableTelemetry:false'),
                (r'telemetryEnabled\s*[:=]\s*true', 'telemetryEnabled:false'),
            ]
            
            for pattern, replacement in telemetry_patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    modifications.append("Disabled telemetry")
            
            # Pattern 2: Bypass version checks
            version_patterns = [
                (r'versionCheck\s*[:=]\s*true', 'versionCheck:false'),
                (r'checkVersion\s*\([^)]*\)\s*\{[^}]*\}', 'checkVersion(){return true;}'),
            ]
            
            for pattern, replacement in version_patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                    modifications.append("Bypassed version checks")
            
            # Pattern 3: Disable update checks
            update_patterns = [
                (r'updateService\s*\.\s*checkForUpdates\([^)]*\)', 'updateService.checkForUpdates=function(){}'),
                (r'autoUpdateEnabled\s*[:=]\s*true', 'autoUpdateEnabled:false'),
            ]
            
            for pattern, replacement in update_patterns:
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    modifications.append("Disabled update checks")
            
            # Pattern 4: Generic function override for telemetry/analytics
            # Replace common telemetry function calls with no-ops
            analytics_overrides = [
                (r'\.track\([^)]*\)', '.track=function(){}'),
                (r'\.send\([^)]*\)', '.send=function(){}'),
                (r'\.log\([^)]*\)', '.log=function(){}'),
            ]
            
            for pattern, replacement in analytics_overrides:
                # Only replace in specific contexts to avoid breaking functionality
                if 'telemetry' in content.lower() or 'analytics' in content.lower():
                    # More conservative replacement
                    pass
            
            # Write back if modified
            if content != original_content:
                # Create backup first
                backup_success, backup_path = self.backup_workbench(workbench_path)
                if not backup_success:
                    return False, "Failed to create backup"
                
                # Check if we need elevated permissions
                if not os.access(workbench_path, os.W_OK):
                    return False, f"Need {self._get_privilege_type()} privileges to modify workbench.js"
                
                with open(workbench_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)
                
                mod_msg = ", ".join(modifications) if modifications else "Applied patches"
                return True, f"Patched workbench.js: {mod_msg}"
            else:
                return False, "No telemetry patterns found or already patched"
        
        except PermissionError:
            return False, f"Need {self._get_privilege_type()} privileges to patch workbench.js"
        except Exception as e:
            return False, f"Patch failed: {str(e)}"
    
    def _get_privilege_type(self) -> str:
        """Get privilege type needed"""
        return "Administrator" if self.system == "Windows" else "root"
    
    def restore_workbench(self, workbench_path: Path) -> Tuple[bool, str]:
        """Restore workbench.js from backup"""
        try:
            backup_dir = Path.home() / ".cursor-sentinel" / "backups" / "workbench"
            backup_path = backup_dir / f"{workbench_path.name}.backup"
            
            if not backup_path.exists():
                return False, "Backup not found"
            
            if not os.access(workbench_path, os.W_OK):
                return False, f"Need {self._get_privilege_type()} privileges to restore workbench.js"
            
            shutil.copy2(backup_path, workbench_path)
            return True, "Restored workbench.js from backup"
        
        except Exception as e:
            return False, f"Restore failed: {str(e)}"
    
    def patch_workbench(self) -> Tuple[bool, str]:
        """Main patch function"""
        workbench_path = self.find_workbench_file()
        
        if not workbench_path:
            return False, "workbench.js not found. Make sure Cursor is installed."
        
        return self.patch_telemetry_checks(workbench_path)
    
    def is_patched(self) -> bool:
        """Check if workbench.js is already patched"""
        workbench_path = self.find_workbench_file()
        
        if not workbench_path:
            return False
        
        try:
            with open(workbench_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for common patch markers
            patch_indicators = [
                'enableTelemetry:false',
                'telemetryService.setEnabled(false)',
                'versionCheck:false',
            ]
            
            return any(indicator in content for indicator in patch_indicators)
        except Exception:
            return False
