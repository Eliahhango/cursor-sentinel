"""
Cursor-Sentinel: Profile Manager
Save and switch between multiple identity profiles
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class ProfileManager:
    """Manage multiple identity profiles"""
    
    def __init__(self):
        self.profiles_dir = Path.home() / ".cursor-sentinel" / "profiles"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.current_profile_file = self.profiles_dir / "current_profile.json"
    
    def create_profile(self, profile_name: str, identifiers: Dict[str, str], credentials: Optional[Dict[str, str]] = None) -> Tuple[bool, str]:
        """Create a new profile with identifiers and optional credentials"""
        try:
            if not profile_name or not profile_name.strip():
                return False, "Profile name cannot be empty"
            
            profile_name = profile_name.strip()
            
            # Validate identifiers
            required_keys = ["machineId", "macMachineId", "devDeviceId"]
            if not all(key in identifiers for key in required_keys):
                return False, f"Profile must contain all identifiers: {', '.join(required_keys)}"
            
            profile_data = {
                "name": profile_name,
                "created_at": datetime.now().isoformat(),
                "identifiers": identifiers,
                "credentials": credentials or {}
            }
            
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            if profile_file.exists():
                return False, f"Profile '{profile_name}' already exists"
            
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2)
            
            return True, f"Profile '{profile_name}' created successfully"
        
        except Exception as e:
            return False, f"Failed to create profile: {str(e)}"
    
    def list_profiles(self) -> List[Dict[str, any]]:
        """List all available profiles"""
        profiles = []
        
        try:
            for profile_file in self.profiles_dir.glob("*.json"):
                if profile_file.name == "current_profile.json":
                    continue
                
                try:
                    with open(profile_file, 'r', encoding='utf-8') as f:
                        profile_data = json.load(f)
                        profiles.append({
                            "name": profile_data.get("name", profile_file.stem),
                            "created_at": profile_data.get("created_at", "Unknown"),
                            "has_credentials": bool(profile_data.get("credentials"))
                        })
                except Exception:
                    continue
        except Exception:
            pass
        
        return profiles
    
    def get_profile(self, profile_name: str) -> Optional[Dict[str, any]]:
        """Get profile data by name"""
        try:
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            if not profile_file.exists():
                return None
            
            with open(profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    def delete_profile(self, profile_name: str) -> Tuple[bool, str]:
        """Delete a profile"""
        try:
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            if not profile_file.exists():
                return False, f"Profile '{profile_name}' not found"
            
            profile_file.unlink()
            return True, f"Profile '{profile_name}' deleted successfully"
        except Exception as e:
            return False, f"Failed to delete profile: {str(e)}"
    
    def save_current_profile(self, profile_name: str) -> Tuple[bool, str]:
        """Save current profile name"""
        try:
            with open(self.current_profile_file, 'w', encoding='utf-8') as f:
                json.dump({"name": profile_name, "last_used": datetime.now().isoformat()}, f, indent=2)
            return True, f"Current profile set to '{profile_name}'"
        except Exception as e:
            return False, f"Failed to save current profile: {str(e)}"
    
    def get_current_profile(self) -> Optional[str]:
        """Get current profile name"""
        try:
            if not self.current_profile_file.exists():
                return None
            
            with open(self.current_profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("name")
        except Exception:
            return None
    
    def apply_profile(self, profile_name: str) -> Tuple[bool, str]:
        """Apply a profile by updating storage.json with profile identifiers"""
        from reset_engine import ResetEngine
        
        profile = self.get_profile(profile_name)
        if not profile:
            return False, f"Profile '{profile_name}' not found"
        
        try:
            reset_engine = ResetEngine()
            storage_path = reset_engine.cursor_paths["storage"]
            
            # Create parent directory if needed
            storage_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read existing storage.json or create new
            if storage_path.exists():
                try:
                    with open(storage_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
            else:
                data = {}
            
            # Apply profile identifiers
            identifiers = profile.get("identifiers", {})
            data["machineId"] = identifiers.get("machineId")
            data["macMachineId"] = identifiers.get("macMachineId")
            data["devDeviceId"] = identifiers.get("devDeviceId")
            
            # Write back
            with open(storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            # Save as current profile
            self.save_current_profile(profile_name)
            
            return True, f"Applied profile '{profile_name}' successfully"
        
        except Exception as e:
            return False, f"Failed to apply profile: {str(e)}"
    
    def export_profile(self, profile_name: str, export_path: Path) -> Tuple[bool, str]:
        """Export profile to a file"""
        try:
            profile = self.get_profile(profile_name)
            if not profile:
                return False, f"Profile '{profile_name}' not found"
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2)
            
            return True, f"Profile exported to {export_path}"
        except Exception as e:
            return False, f"Failed to export profile: {str(e)}"
    
    def import_profile(self, import_path: Path) -> Tuple[bool, str]:
        """Import profile from a file"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
            
            profile_name = profile_data.get("name")
            if not profile_name:
                return False, "Profile file missing 'name' field"
            
            profile_file = self.profiles_dir / f"{profile_name}.json"
            
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2)
            
            return True, f"Profile '{profile_name}' imported successfully"
        except Exception as e:
            return False, f"Failed to import profile: {str(e)}"
    
    def capture_current_identity(self, profile_name: str) -> Tuple[bool, str]:
        """Capture current identifiers from storage.json and save as profile"""
        from reset_engine import ResetEngine
        
        try:
            reset_engine = ResetEngine()
            storage_path = reset_engine.cursor_paths["storage"]
            
            if not storage_path.exists():
                return False, "storage.json not found. Cannot capture current identity."
            
            with open(storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            identifiers = {
                "machineId": data.get("machineId", ""),
                "macMachineId": data.get("macMachineId", ""),
                "devDeviceId": data.get("devDeviceId", "")
            }
            
            if not all(identifiers.values()):
                return False, "Current identity is incomplete. Cannot save as profile."
            
            return self.create_profile(profile_name, identifiers)
        
        except Exception as e:
            return False, f"Failed to capture current identity: {str(e)}"
