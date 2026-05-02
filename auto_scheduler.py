"""
Cursor-Sentinel: Auto Scheduler
Schedule automatic resets and operations
"""

import json
import threading
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Tuple


class AutoScheduler:
    """Schedule automatic operations"""
    
    def __init__(self):
        self.schedule_dir = Path.home() / ".cursor-sentinel" / "schedule"
        self.schedule_dir.mkdir(parents=True, exist_ok=True)
        self.schedule_file = self.schedule_dir / "schedule.json"
        self.schedules = {}
        self.running = False
        self.scheduler_thread = None
        self.callbacks = {}
        self._load_schedules()
    
    def _load_schedules(self):
        """Load schedules from file"""
        if self.schedule_file.exists():
            try:
                with open(self.schedule_file, 'r', encoding='utf-8') as f:
                    self.schedules = json.load(f)
            except Exception:
                self.schedules = {}
        else:
            self.schedules = {}
    
    def _save_schedules(self):
        """Save schedules to file"""
        try:
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                json.dump(self.schedules, f, indent=2)
        except Exception:
            pass
    
    def add_schedule(self, schedule_id: str, schedule_type: str, interval_hours: int,
                     enabled: bool = True, last_run: Optional[str] = None) -> Tuple[bool, str]:
        """Add a new schedule"""
        try:
            if schedule_id in self.schedules:
                return False, f"Schedule '{schedule_id}' already exists"
            
            self.schedules[schedule_id] = {
                "type": schedule_type,  # "reset", "backup", etc.
                "interval_hours": interval_hours,
                "enabled": enabled,
                "last_run": last_run,
                "created": datetime.now().isoformat()
            }
            
            self._save_schedules()
            return True, f"Schedule '{schedule_id}' added successfully"
        except Exception as e:
            return False, f"Failed to add schedule: {str(e)}"
    
    def remove_schedule(self, schedule_id: str) -> Tuple[bool, str]:
        """Remove a schedule"""
        try:
            if schedule_id not in self.schedules:
                return False, f"Schedule '{schedule_id}' not found"
            
            del self.schedules[schedule_id]
            self._save_schedules()
            return True, f"Schedule '{schedule_id}' removed successfully"
        except Exception as e:
            return False, f"Failed to remove schedule: {str(e)}"
    
    def enable_schedule(self, schedule_id: str) -> Tuple[bool, str]:
        """Enable a schedule"""
        if schedule_id not in self.schedules:
            return False, f"Schedule '{schedule_id}' not found"
        
        self.schedules[schedule_id]["enabled"] = True
        self._save_schedules()
        return True, f"Schedule '{schedule_id}' enabled"
    
    def disable_schedule(self, schedule_id: str) -> Tuple[bool, str]:
        """Disable a schedule"""
        if schedule_id not in self.schedules:
            return False, f"Schedule '{schedule_id}' not found"
        
        self.schedules[schedule_id]["enabled"] = False
        self._save_schedules()
        return True, f"Schedule '{schedule_id}' disabled"
    
    def list_schedules(self) -> List[Dict]:
        """List all schedules"""
        result = []
        for schedule_id, schedule_data in self.schedules.items():
            result.append({
                "id": schedule_id,
                **schedule_data
            })
        return result
    
    def get_next_run_time(self, schedule_id: str) -> Optional[datetime]:
        """Get next run time for a schedule"""
        if schedule_id not in self.schedules:
            return None
        
        schedule = self.schedules[schedule_id]
        if not schedule.get("enabled", False):
            return None
        
        last_run_str = schedule.get("last_run")
        if last_run_str:
            last_run = datetime.fromisoformat(last_run_str)
        else:
            last_run = datetime.now()
        
        interval = timedelta(hours=schedule.get("interval_hours", 24))
        next_run = last_run + interval
        
        return next_run
    
    def register_callback(self, schedule_type: str, callback: Callable):
        """Register a callback for a schedule type"""
        self.callbacks[schedule_type] = callback
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.running:
            try:
                current_time = datetime.now()
                
                for schedule_id, schedule in self.schedules.items():
                    if not schedule.get("enabled", False):
                        continue
                    
                    next_run = self.get_next_run_time(schedule_id)
                    if next_run and current_time >= next_run:
                        # Execute schedule
                        schedule_type = schedule.get("type", "reset")
                        
                        if schedule_type in self.callbacks:
                            try:
                                # Update last run time
                                self.schedules[schedule_id]["last_run"] = current_time.isoformat()
                                self._save_schedules()
                                
                                # Execute callback
                                self.callbacks[schedule_type]()
                            except Exception as e:
                                print(f"Error executing schedule {schedule_id}: {e}")
                
                # Check every minute
                time.sleep(60)
            
            except Exception as e:
                print(f"Scheduler error: {e}")
                time.sleep(60)
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            return
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=2)
