"""
Cursor-Sentinel: Statistics Tracker
Track operations, reset history, and usage statistics
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class StatisticsTracker:
    """Track statistics and operation history"""
    
    def __init__(self):
        self.stats_dir = Path.home() / ".cursor-sentinel" / "stats"
        self.stats_dir.mkdir(parents=True, exist_ok=True)
        self.stats_file = self.stats_dir / "statistics.json"
        self._load_stats()
    
    def _load_stats(self):
        """Load statistics from file"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.stats = json.load(f)
            except Exception:
                self.stats = self._get_default_stats()
        else:
            self.stats = self._get_default_stats()
    
    def _save_stats(self):
        """Save statistics to file"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2)
        except Exception:
            pass
    
    def _get_default_stats(self) -> Dict:
        """Get default statistics structure"""
        return {
            "total_resets": 0,
            "total_backups": 0,
            "total_profile_switches": 0,
            "immortality_mode_enabled_count": 0,
            "workbench_patches": 0,
            "account_creations": 0,
            "operations": [],
            "first_use": datetime.now().isoformat(),
            "last_reset": None,
            "last_backup": None
        }
    
    def record_reset(self, success: bool = True):
        """Record a reset operation"""
        self.stats["total_resets"] = self.stats.get("total_resets", 0) + 1
        if success:
            self.stats["last_reset"] = datetime.now().isoformat()
        
        self._add_operation("reset", success)
        self._save_stats()
    
    def record_backup(self, success: bool = True):
        """Record a backup operation"""
        self.stats["total_backups"] = self.stats.get("total_backups", 0) + 1
        if success:
            self.stats["last_backup"] = datetime.now().isoformat()
        
        self._add_operation("backup", success)
        self._save_stats()
    
    def record_profile_switch(self, profile_name: str, success: bool = True):
        """Record a profile switch"""
        self.stats["total_profile_switches"] = self.stats.get("total_profile_switches", 0) + 1
        self._add_operation(f"profile_switch:{profile_name}", success)
        self._save_stats()
    
    def record_immortality_mode(self, enabled: bool):
        """Record immortality mode toggle"""
        if enabled:
            self.stats["immortality_mode_enabled_count"] = self.stats.get("immortality_mode_enabled_count", 0) + 1
            self._add_operation("immortality_enabled", True)
        else:
            self._add_operation("immortality_disabled", True)
        self._save_stats()
    
    def record_workbench_patch(self, success: bool = True):
        """Record a workbench patch"""
        if success:
            self.stats["workbench_patches"] = self.stats.get("workbench_patches", 0) + 1
        self._add_operation("workbench_patch", success)
        self._save_stats()
    
    def record_account_creation(self, success: bool = True):
        """Record an account creation"""
        if success:
            self.stats["account_creations"] = self.stats.get("account_creations", 0) + 1
        self._add_operation("account_creation", success)
        self._save_stats()
    
    def _add_operation(self, operation_type: str, success: bool):
        """Add an operation to history"""
        if "operations" not in self.stats:
            self.stats["operations"] = []
        
        operation = {
            "type": operation_type,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        self.stats["operations"].append(operation)
        
        # Keep only last 1000 operations
        if len(self.stats["operations"]) > 1000:
            self.stats["operations"] = self.stats["operations"][-1000:]
    
    def get_statistics(self) -> Dict:
        """Get all statistics"""
        return self.stats.copy()
    
    def get_recent_operations(self, limit: int = 50) -> List[Dict]:
        """Get recent operations"""
        operations = self.stats.get("operations", [])
        return operations[-limit:] if len(operations) > limit else operations
    
    def get_operation_count_by_type(self) -> Dict[str, int]:
        """Get count of operations by type"""
        counts = {}
        operations = self.stats.get("operations", [])
        
        for op in operations:
            op_type = op.get("type", "unknown")
            if op_type not in counts:
                counts[op_type] = 0
            counts[op_type] += 1
        
        return counts
    
    def get_success_rate(self) -> Dict[str, float]:
        """Get success rate by operation type"""
        success_counts = {}
        total_counts = {}
        
        operations = self.stats.get("operations", [])
        
        for op in operations:
            op_type = op.get("type", "unknown")
            if op_type not in total_counts:
                total_counts[op_type] = 0
                success_counts[op_type] = 0
            
            total_counts[op_type] += 1
            if op.get("success", False):
                success_counts[op_type] += 1
        
        rates = {}
        for op_type in total_counts:
            if total_counts[op_type] > 0:
                rates[op_type] = (success_counts[op_type] / total_counts[op_type]) * 100
        
        return rates
    
    def reset_statistics(self):
        """Reset all statistics"""
        self.stats = self._get_default_stats()
        self._save_stats()
    
    def export_statistics(self, export_path: Path) -> Tuple[bool, str]:
        """Export statistics to a file"""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2)
            return True, f"Statistics exported to {export_path}"
        except Exception as e:
            return False, f"Failed to export statistics: {str(e)}"
