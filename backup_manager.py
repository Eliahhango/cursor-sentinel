"""
Cursor-Sentinel: Backup Manager
View, restore, and manage backups
"""

import os
import json
import zipfile
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from datetime import datetime


class BackupManager:
    """Manage backups for Cursor-Sentinel"""
    
    def __init__(self):
        self.backup_dir = Path.home() / ".cursor-sentinel" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.backup_dir / "backup_metadata.json"
        self._load_metadata()
    
    def _load_metadata(self):
        """Load backup metadata"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            except Exception:
                self.metadata = {}
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """Save backup metadata"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception:
            pass
    
    def list_backups(self) -> List[Dict[str, any]]:
        """List all available backups"""
        backups = []
        
        try:
            for backup_file in self.backup_dir.glob("*.zip"):
                if backup_file.name == "backup_metadata.json":
                    continue
                
                try:
                    stat = backup_file.stat()
                    file_size = stat.st_size
                    
                    # Try to get metadata
                    backup_name = backup_file.stem
                    metadata = self.metadata.get(backup_name, {})
                    
                    backups.append({
                        "name": backup_name,
                        "path": str(backup_file),
                        "size": file_size,
                        "created": metadata.get("created", datetime.fromtimestamp(stat.st_mtime).isoformat()),
                        "description": metadata.get("description", ""),
                        "type": metadata.get("type", "auto")
                    })
                except Exception:
                    continue
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x["created"], reverse=True)
            return backups
        except Exception:
            return []
    
    def get_backup_info(self, backup_name: str) -> Optional[Dict[str, any]]:
        """Get detailed info about a backup"""
        backup_path = self.backup_dir / f"{backup_name}.zip"
        
        if not backup_path.exists():
            return None
        
        try:
            stat = backup_path.stat()
            
            # Read zip contents
            files = []
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                files = zipf.namelist()
            
            metadata = self.metadata.get(backup_name, {})
            
            return {
                "name": backup_name,
                "path": str(backup_path),
                "size": stat.st_size,
                "created": metadata.get("created", datetime.fromtimestamp(stat.st_mtime).isoformat()),
                "description": metadata.get("description", ""),
                "type": metadata.get("type", "auto"),
                "file_count": len(files),
                "files": files[:20]  # First 20 files
            }
        except Exception:
            return None
    
    def delete_backup(self, backup_name: str) -> Tuple[bool, str]:
        """Delete a backup"""
        try:
            backup_path = self.backup_dir / f"{backup_name}.zip"
            
            if not backup_path.exists():
                return False, f"Backup '{backup_name}' not found"
            
            backup_path.unlink()
            
            # Remove from metadata
            if backup_name in self.metadata:
                del self.metadata[backup_name]
                self._save_metadata()
            
            return True, f"Backup '{backup_name}' deleted successfully"
        except Exception as e:
            return False, f"Failed to delete backup: {str(e)}"
    
    def restore_backup(self, backup_name: str, target_path: Optional[Path] = None) -> Tuple[bool, str]:
        """Restore a backup"""
        from reset_engine import ResetEngine
        
        try:
            backup_path = self.backup_dir / f"{backup_name}.zip"
            
            if not backup_path.exists():
                return False, f"Backup '{backup_name}' not found"
            
            reset_engine = ResetEngine()
            
            # Extract backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Restore storage.json
                if "storage.json" in zipf.namelist():
                    storage_path = reset_engine.cursor_paths["storage"]
                    storage_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Extract storage.json
                    zipf.extract("storage.json", storage_path.parent)
                    
                    # Move to correct location
                    extracted = storage_path.parent / "storage.json"
                    if extracted.exists():
                        if storage_path.exists():
                            storage_path.unlink()
                        extracted.rename(storage_path)
                
                # Restore workspace storage (if exists in backup)
                workspace_files = [f for f in zipf.namelist() if f.startswith("workspaceStorage")]
                if workspace_files:
                    workspace_path = reset_engine.cursor_paths["workspace_storage"]
                    workspace_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Extract to parent directory
                    zipf.extractall(workspace_path.parent)
            
            return True, f"Backup '{backup_name}' restored successfully"
        except Exception as e:
            return False, f"Failed to restore backup: {str(e)}"
    
    def add_backup_metadata(self, backup_name: str, description: str = "", backup_type: str = "auto"):
        """Add metadata to a backup"""
        backup_path = self.backup_dir / f"{backup_name}.zip"
        
        if backup_path.exists():
            self.metadata[backup_name] = {
                "created": datetime.now().isoformat(),
                "description": description,
                "type": backup_type
            }
            self._save_metadata()
    
    def cleanup_old_backups(self, keep_count: int = 10) -> Tuple[int, str]:
        """Clean up old backups, keeping only the most recent ones"""
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            return 0, "No backups to clean up"
        
        deleted_count = 0
        errors = []
        
        # Delete oldest backups
        for backup in backups[keep_count:]:
            success, msg = self.delete_backup(backup["name"])
            if success:
                deleted_count += 1
            else:
                errors.append(msg)
        
        error_msg = f"; {', '.join(errors)}" if errors else ""
        return deleted_count, f"Deleted {deleted_count} old backup(s){error_msg}"
    
    def export_backup(self, backup_name: str, export_path: Path) -> Tuple[bool, str]:
        """Export a backup to a different location"""
        try:
            backup_path = self.backup_dir / f"{backup_name}.zip"
            
            if not backup_path.exists():
                return False, f"Backup '{backup_name}' not found"
            
            import shutil
            shutil.copy2(backup_path, export_path)
            return True, f"Backup exported to {export_path}"
        except Exception as e:
            return False, f"Failed to export backup: {str(e)}"
    
    def get_backup_size(self) -> Dict[str, any]:
        """Get total backup size statistics"""
        total_size = 0
        backup_count = 0
        
        try:
            for backup_file in self.backup_dir.glob("*.zip"):
                if backup_file.name != "backup_metadata.json":
                    total_size += backup_file.stat().st_size
                    backup_count += 1
        except Exception:
            pass
        
        return {
            "total_size": total_size,
            "backup_count": backup_count,
            "average_size": total_size // backup_count if backup_count > 0 else 0
        }
