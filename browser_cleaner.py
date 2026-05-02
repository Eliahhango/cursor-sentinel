"""
Cursor-Sentinel: Browser Cleaner
Clear browser cookies, cache, and local storage related to Cursor
"""

import os
import shutil
import platform
from pathlib import Path
from typing import List, Tuple, Dict


class BrowserCleaner:
    """Clean browser data related to Cursor"""
    
    def __init__(self):
        self.system = platform.system()
        self.browser_paths = self._detect_browser_paths()
    
    def _detect_browser_paths(self) -> Dict[str, List[Path]]:
        """Detect browser data paths"""
        paths = {}
        home = Path.home()
        
        if self.system == "Windows":
            app_data = Path(os.getenv("APPDATA", ""))
            local_app_data = Path(os.getenv("LOCALAPPDATA", ""))
            
            # Chrome/Edge
            paths["chrome"] = [
                local_app_data / "Google" / "Chrome" / "User Data" / "Default" / "Cookies",
                local_app_data / "Google" / "Chrome" / "User Data" / "Default" / "Local Storage",
            ]
            paths["edge"] = [
                local_app_data / "Microsoft" / "Edge" / "User Data" / "Default" / "Cookies",
                local_app_data / "Microsoft" / "Edge" / "User Data" / "Default" / "Local Storage",
            ]
            paths["firefox"] = [
                app_data / "Mozilla" / "Firefox" / "Profiles",
            ]
        
        elif self.system == "Darwin":  # macOS
            paths["chrome"] = [
                home / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Cookies",
                home / "Library" / "Application Support" / "Google" / "Chrome" / "Default" / "Local Storage",
            ]
            paths["safari"] = [
                home / "Library" / "Cookies",
                home / "Library" / "Caches",
            ]
            paths["firefox"] = [
                home / "Library" / "Application Support" / "Firefox" / "Profiles",
            ]
        
        else:  # Linux
            paths["chrome"] = [
                home / ".config" / "google-chrome" / "Default" / "Cookies",
                home / ".config" / "google-chrome" / "Default" / "Local Storage",
            ]
            paths["firefox"] = [
                home / ".mozilla" / "firefox",
            ]
        
        return paths
    
    def find_cursor_cookies(self) -> List[Path]:
        """Find Cursor-related cookies and storage"""
        cursor_domains = ["cursor.sh", "todesktop.com", "cursor.com"]
        found_files = []
        
        # This is a simplified version - in reality, cookie files are databases
        # that need to be parsed. For now, we'll identify the files that might contain
        # Cursor cookies
        
        for browser, paths in self.browser_paths.items():
            for path in paths:
                if path.exists():
                    if path.is_file() and "Cookies" in path.name:
                        found_files.append(path)
                    elif path.is_dir():
                        # Look for cookie files in the directory
                        for cookie_file in path.rglob("*Cookies*"):
                            if cookie_file.is_file():
                                found_files.append(cookie_file)
        
        return found_files
    
    def clear_cursor_browser_data(self) -> Tuple[bool, List[str]]:
        """Clear Cursor-related browser data"""
        cleared = []
        errors = []
        
        try:
            # Clear cookies (requires closing browser)
            cookie_files = self.find_cursor_cookies()
            
            # Note: Actually deleting cookie files while browser is running can cause issues
            # This is more of a placeholder - real implementation would need to:
            # 1. Parse cookie databases
            # 2. Remove specific domain cookies
            # 3. Use browser APIs if available
            
            cleared.append(f"Found {len(cookie_files)} potential cookie storage locations")
            cleared.append("Note: Manual browser cleanup recommended for safety")
            
            return True, cleared
        
        except Exception as e:
            errors.append(f"Error clearing browser data: {str(e)}")
            return False, errors
    
    def get_browser_data_info(self) -> Dict[str, any]:
        """Get information about browser data locations"""
        info = {
            "system": self.system,
            "browsers": {}
        }
        
        for browser, paths in self.browser_paths.items():
            browser_info = {
                "paths": [str(p) for p in paths],
                "exists": [p.exists() for p in paths]
            }
            info["browsers"][browser] = browser_info
        
        return info
    
    def clear_cache_only(self) -> Tuple[bool, str]:
        """Clear browser cache only (safer operation)"""
        try:
            home = Path.home()
            
            if self.system == "Windows":
                cache_paths = [
                    Path(os.getenv("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data" / "Default" / "Cache",
                    Path(os.getenv("LOCALAPPDATA", "")) / "Microsoft" / "Edge" / "User Data" / "Default" / "Cache",
                ]
            elif self.system == "Darwin":
                cache_paths = [
                    home / "Library" / "Caches" / "com.google.Chrome",
                    home / "Library" / "Caches" / "com.microsoft.edgemac",
                ]
            else:
                cache_paths = [
                    home / ".cache" / "google-chrome",
                    home / ".cache" / "microsoft-edge",
                ]
            
            cleared_count = 0
            for cache_path in cache_paths:
                if cache_path.exists() and cache_path.is_dir():
                    try:
                        # Clear cache directory
                        for item in cache_path.iterdir():
                            if item.is_file():
                                item.unlink()
                            elif item.is_dir():
                                shutil.rmtree(item)
                        cleared_count += 1
                    except Exception:
                        pass
            
            return True, f"Cleared cache from {cleared_count} browser(s)"
        
        except Exception as e:
            return False, f"Failed to clear cache: {str(e)}"
