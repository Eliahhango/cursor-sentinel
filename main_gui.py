"""
Cursor-Sentinel: Main GUI Application
Modern dark-themed dashboard using CustomTkinter
"""

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import customtkinter as ctk
import threading
from pathlib import Path
import sys
import platform
from typing import Optional

# Import our modules
from reset_engine import ResetEngine
from network_blocker import NetworkBlocker
from account_creator import AccountCreator
from workbench_patcher import WorkbenchPatcher
from profile_manager import ProfileManager
from utils import is_admin, request_admin_privileges, get_system_info, log_message
from ascii_art import (
    BANNER, SKELETON, SKULL, PROCESS_BANNER, RESET_PROCESS, SUCCESS_BANNER,
    PROFILE_BANNER, ACCOUNT_BANNER, NETWORK_BANNER, PATCH_BANNER
)


# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CursorSentinelApp(ctk.CTk):
    """Main Cursor-Sentinel Application"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize modules
        self.reset_engine = ResetEngine()
        self.network_blocker = NetworkBlocker()
        self.account_creator = AccountCreator()
        self.workbench_patcher = WorkbenchPatcher()
        self.profile_manager = ProfileManager()
        
        # Configure window
        self.title("Cursor-Sentinel")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Print ASCII banner on startup (console)
        print(BANNER)
        
        # Variables
        self.auto_cleanup_var = ctk.BooleanVar(value=False)
        self.block_updates_var = ctk.BooleanVar(value=self.network_blocker.is_blocked())
        self.reset_in_progress = False
        
        # Create UI
        self._create_ui()
        
        # Initial status check
        self.update_status()
        
        # Log ASCII banner
        self.log_ascii(BANNER)
    
    def _create_ui(self):
        """Create the main UI components"""
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            main_frame,
            text="CURSOR-SENTINEL",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        header.grid(row=0, column=0, pady=(20, 10))
        
        # Status indicator frame
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        status_frame.grid_columnconfigure(1, weight=1)
        
        # System ID Health
        health_label = ctk.CTkLabel(status_frame, text="System ID Health:", font=ctk.CTkFont(size=14, weight="bold"))
        health_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.health_status_label = ctk.CTkLabel(status_frame, text="Checking...", font=ctk.CTkFont(size=12))
        self.health_status_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.health_indicator = ctk.CTkLabel(status_frame, text="●", font=ctk.CTkFont(size=20))
        self.health_indicator.grid(row=0, column=2, padx=10, pady=10)
        
        # Quick Reset button (large, prominent)
        reset_frame = ctk.CTkFrame(main_frame)
        reset_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        reset_frame.grid_columnconfigure(0, weight=1)
        
        self.reset_button = ctk.CTkButton(
            reset_frame,
            text="QUICK RESET",
            font=ctk.CTkFont(size=24, weight="bold"),
            height=60,
            fg_color="#e63946",
            hover_color="#d62828",
            command=self.quick_reset
        )
        self.reset_button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.progress_bar = ctk.CTkProgressBar(reset_frame)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.progress_bar.set(0)
        
        # Control panel (toggles and buttons)
        control_panel = ctk.CTkFrame(main_frame)
        control_panel.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        control_panel.grid_columnconfigure(0, weight=1)
        control_panel.grid_columnconfigure(1, weight=1)
        
        # Left column
        left_col = ctk.CTkFrame(control_panel)
        left_col.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Block Updates toggle
        block_updates_switch = ctk.CTkSwitch(
            left_col,
            text="Block Updates (Immortality Mode)",
            variable=self.block_updates_var,
            command=self.toggle_block_updates,
            font=ctk.CTkFont(size=12)
        )
        block_updates_switch.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Auto Cleanup toggle
        auto_cleanup_switch = ctk.CTkSwitch(
            left_col,
            text="Auto-Cleanup on Exit",
            variable=self.auto_cleanup_var,
            font=ctk.CTkFont(size=12)
        )
        auto_cleanup_switch.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        # Patch Workbench button
        patch_workbench_btn = ctk.CTkButton(
            left_col,
            text="Patch Workbench.js",
            command=self.patch_workbench,
            font=ctk.CTkFont(size=12),
            width=200
        )
        patch_workbench_btn.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        # Right column
        right_col = ctk.CTkFrame(control_panel)
        right_col.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Create Account button
        create_account_btn = ctk.CTkButton(
            right_col,
            text="Create Account (Auto)",
            command=self.create_account_dialog,
            font=ctk.CTkFont(size=12),
            width=200
        )
        create_account_btn.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Profile Manager button
        profile_manager_btn = ctk.CTkButton(
            right_col,
            text="Profile Manager",
            command=self.open_profile_manager,
            font=ctk.CTkFont(size=12),
            width=200
        )
        profile_manager_btn.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        # Request Admin button
        admin_status = "Admin" if is_admin() else "Need Admin"
        request_admin_btn = ctk.CTkButton(
            right_col,
            text=admin_status,
            command=self.request_admin,
            font=ctk.CTkFont(size=12),
            width=200,
            fg_color="#6c757d" if is_admin() else "#dc3545"
        )
        request_admin_btn.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        # Log terminal window
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        
        log_label = ctk.CTkLabel(log_frame, text="Activity Log", font=ctk.CTkFont(size=14, weight="bold"))
        log_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Text widget with scrollbar
        log_text_frame = ctk.CTkFrame(log_frame)
        log_text_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        log_text_frame.grid_columnconfigure(0, weight=1)
        log_text_frame.grid_rowconfigure(0, weight=1)
        
        self.log_text = ctk.CTkTextbox(
            log_text_frame,
            height=150,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # Clear log button
        clear_log_btn = ctk.CTkButton(
            log_frame,
            text="Clear Log",
            command=self.clear_log,
            font=ctk.CTkFont(size=10),
            width=100,
            height=25
        )
        clear_log_btn.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        
        self.log("Cursor-Sentinel initialized")
        self.log(f"System: {get_system_info()['os']} {get_system_info()['platform']}")
    
    def log(self, message: str, level: str = "INFO"):
        """Add message to log terminal"""
        formatted = log_message(message, level)
        self.log_text.insert("end", formatted + "\n")
        self.log_text.see("end")
        self.update_idletasks()
    
    def log_ascii(self, ascii_art: str):
        """Add ASCII art to log terminal"""
        self.log_text.insert("end", ascii_art + "\n")
        self.log_text.see("end")
        self.update_idletasks()
    
    def clear_log(self):
        """Clear log terminal"""
        self.log_text.delete("1.0", "end")
    
    def update_status(self):
        """Update system ID health status"""
        try:
            health = self.reset_engine.get_system_id_health()
            
            if health["storage_json_exists"]:
                ids = health.get("identifiers", {})
                machine_id = ids.get("machineId", "Not found")
                status_text = f"Active | MachineID: {machine_id[:8]}..." if machine_id != "Not found" else "Incomplete"
                self.health_status_label.configure(text=status_text)
                self.health_indicator.configure(text="●", text_color="#28a745")
            else:
                self.health_status_label.configure(text="Not Found | storage.json missing")
                self.health_indicator.configure(text="●", text_color="#dc3545")
        except Exception as e:
            self.health_status_label.configure(text=f"Error: {str(e)}")
            self.health_indicator.configure(text="●", text_color="#dc3545")
    
    def quick_reset(self):
        """Perform quick reset in background thread"""
        if self.reset_in_progress:
            messagebox.showwarning("Reset in Progress", "A reset operation is already in progress.")
            return
        
        self.reset_in_progress = True
        self.reset_button.configure(state="disabled", text="⏳ RESETTING...")
        self.progress_bar.set(0.1)
        
        def reset_thread():
            try:
                self.log_ascii(RESET_PROCESS)
                self.log("Starting quick reset...")
                print(RESET_PROCESS)  # Print to console too
                self.progress_bar.set(0.2)
                
                # Step 1: Kill processes
                self.log_ascii(SKELETON)
                self.log("Killing Cursor processes...")
                print(SKELETON)  # Print to console
                success, msg = self.reset_engine.kill_cursor_processes()
                self.log(f"Process kill: {msg}")
                self.progress_bar.set(0.4)
                
                # Step 2: Backup
                self.log("Creating backup...")
                success, msg = self.reset_engine.backup_files()
                self.log(f"Backup: {msg}")
                self.progress_bar.set(0.6)
                
                # Step 3: Reset storage.json
                self.log("Resetting storage.json...")
                success, msg = self.reset_engine.reset_storage_json()
                self.log(f"Storage reset: {msg}")
                self.progress_bar.set(0.8)
                
                # Step 4: OS-specific reset
                if platform.system() == "Windows":
                    self.log("Resetting Windows Registry...")
                    success, msg = self.reset_engine.reset_windows_registry()
                    self.log(f"Registry: {msg}")
                
                self.progress_bar.set(1.0)
                self.log_ascii(SUCCESS_BANNER)
                self.log("Quick reset completed successfully!")
                print(SUCCESS_BANNER)  # Print to console
                messagebox.showinfo("Reset Complete", "Quick reset completed successfully!")
                self.update_status()
                
            except Exception as e:
                self.log(f"Reset failed: {str(e)}", level="ERROR")
                messagebox.showerror("Reset Failed", f"Reset operation failed:\n{str(e)}")
            finally:
                self.reset_in_progress = False
                self.reset_button.configure(state="normal", text="QUICK RESET")
                self.progress_bar.set(0)
        
        thread = threading.Thread(target=reset_thread, daemon=True)
        thread.start()
    
    def toggle_block_updates(self):
        """Toggle update blocking (Immortality Mode)"""
        try:
            if self.block_updates_var.get():
                self.log_ascii(NETWORK_BANNER)
                self.log("Enabling Immortality Mode...")
                print(NETWORK_BANNER)  # Print to console
                success, msg = self.network_blocker.enable_immortality_mode()
                if success:
                    self.log(f"Immortality Mode enabled: {msg}")
                    messagebox.showinfo("Immortality Mode", "Update blocking enabled successfully!")
                else:
                    self.log(f"Failed to enable Immortality Mode: {msg}", level="ERROR")
                    self.block_updates_var.set(False)
                    messagebox.showerror("Error", f"Failed to enable Immortality Mode:\n{msg}")
            else:
                self.log("Disabling Immortality Mode...")
                success, msg = self.network_blocker.disable_immortality_mode()
                if success:
                    self.log(f"Immortality Mode disabled: {msg}")
                    messagebox.showinfo("Immortality Mode", "Update blocking disabled successfully!")
                else:
                    self.log(f"Failed to disable Immortality Mode: {msg}", level="ERROR")
                    messagebox.showerror("Error", f"Failed to disable Immortality Mode:\n{msg}")
        except Exception as e:
            self.log(f"Error toggling Immortality Mode: {str(e)}", level="ERROR")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def patch_workbench(self):
        """Patch workbench.js"""
        try:
            self.log_ascii(PATCH_BANNER)
            self.log("Patching workbench.js...")
            print(PATCH_BANNER)  # Print to console
            success, msg = self.workbench_patcher.patch_workbench()
            if success:
                self.log_ascii(SUCCESS_BANNER)
                self.log(f"{msg}")
                messagebox.showinfo("Patch Complete", msg)
            else:
                self.log(f"{msg}", level="ERROR")
                messagebox.showerror("Patch Failed", msg)
        except Exception as e:
            self.log(f"Patch error: {str(e)}", level="ERROR")
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def create_account_dialog(self):
        """Open dialog for account creation"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Create Account")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        def create_account():
            self.log_ascii(ACCOUNT_BANNER)
            self.log("Starting automated account creation...")
            print(ACCOUNT_BANNER)  # Print to console
            dialog.destroy()
            
            def create_thread():
                try:
                    success, result = self.account_creator.create_account_sync()
                    if success:
                        self.log_ascii(SUCCESS_BANNER)
                        self.log(f"Account created: {result.get('email', 'Unknown')}")
                        messagebox.showinfo("Account Created", f"Account created successfully!\nEmail: {result.get('email', 'Unknown')}")
                    else:
                        error = result.get('error', 'Unknown error')
                        self.log(f"Account creation failed: {error}", level="ERROR")
                        messagebox.showerror("Account Creation Failed", f"Failed to create account:\n{error}")
                except Exception as e:
                    self.log(f"Account creation error: {str(e)}", level="ERROR")
                    messagebox.showerror("Error", f"Error: {str(e)}")
            
            thread = threading.Thread(target=create_thread, daemon=True)
            thread.start()
        
        # Dialog content - Add ASCII banner
        ascii_label = ctk.CTkTextbox(dialog, height=120, font=ctk.CTkFont(family="Consolas", size=9))
        ascii_label.pack(pady=(20, 10), padx=20, fill="x")
        ascii_label.insert("1.0", ACCOUNT_BANNER)
        ascii_label.configure(state="disabled")
        
        label = ctk.CTkLabel(dialog, text="Automated Account Creator", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=10)
        
        info_text = ctk.CTkTextbox(dialog, height=150)
        info_text.pack(pady=10, padx=20, fill="both", expand=True)
        info_text.insert("1.0", "This will:\n\n1. Open a temporary email service\n2. Register a new Cursor account\n3. Verify the email automatically\n4. Log you into the desktop app\n\nNote: Playwright must be installed for this to work.")
        info_text.configure(state="disabled")
        
        create_btn = ctk.CTkButton(dialog, text="Create Account", command=create_account)
        create_btn.pack(pady=20)
    
    def open_profile_manager(self):
        """Open profile manager window"""
        ProfileManagerWindow(self, self.profile_manager, self.reset_engine, self.log)
    
    def request_admin(self):
        """Request admin privileges"""
        if is_admin():
            messagebox.showinfo("Admin", "Already running with administrator privileges.")
            return
        
        success, msg = request_admin_privileges()
        if success:
            messagebox.showinfo("Admin", msg)
        else:
            messagebox.showwarning("Admin Required", msg)
    
    def on_closing(self):
        """Handle window closing"""
        if self.auto_cleanup_var.get():
            self.log("Auto-cleanup enabled, cleaning up...")
            # Add cleanup logic here if needed
        self.destroy()


class ProfileManagerWindow(ctk.CTkToplevel):
    """Profile Manager Window"""
    
    def __init__(self, parent, profile_manager, reset_engine, log_callback):
        super().__init__(parent)
        self.profile_manager = profile_manager
        self.reset_engine = reset_engine
        self.log_callback = log_callback
        
        self.title("Profile Manager")
        self.geometry("700x650")
        self.transient(parent)
        
        self._create_ui()
        self.refresh_profiles()
        
        # Show ASCII banner in log
        self.log_callback(PROFILE_BANNER)
        print(PROFILE_BANNER)  # Print to console
    
    def _create_ui(self):
        """Create profile manager UI"""
        # ASCII Banner
        ascii_frame = ctk.CTkTextbox(self, height=100, font=ctk.CTkFont(family="Consolas", size=8))
        ascii_frame.pack(pady=(20, 10), padx=20, fill="x")
        ascii_frame.insert("1.0", PROFILE_BANNER)
        ascii_frame.configure(state="disabled")
        
        # Header
        header = ctk.CTkLabel(self, text="Profile Manager", font=ctk.CTkFont(size=20, weight="bold"))
        header.pack(pady=10)
        
        # Profile list frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        scrollbar = ctk.CTkScrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.profile_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg="#2b2b2b",
            fg="white",
            font=("Consolas", 11),
            selectbackground="#1f538d"
        )
        self.profile_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.configure(command=self.profile_listbox.yview)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(buttons_frame, text="Apply", command=self.apply_profile).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Save Current", command=self.save_current).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Delete", command=self.delete_profile).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Refresh", command=self.refresh_profiles).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Close", command=self.destroy).pack(side="right", padx=5)
    
    def refresh_profiles(self):
        """Refresh profile list"""
        self.profile_listbox.delete(0, "end")
        profiles = self.profile_manager.list_profiles()
        for profile in profiles:
            name = profile["name"]
            created = profile.get("created_at", "Unknown")[:10]
            creds = "[*]" if profile.get("has_credentials") else ""
            self.profile_listbox.insert("end", f"{name} | Created: {created} {creds}")
    
    def apply_profile(self):
        """Apply selected profile"""
        selection = self.profile_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a profile to apply.")
            return
        
        profile_name = self.profile_listbox.get(selection[0]).split(" |")[0]
        self.log_callback(PROCESS_BANNER)
        print(PROCESS_BANNER)  # Print to console
        success, msg = self.profile_manager.apply_profile(profile_name)
        if success:
            self.log_callback(SUCCESS_BANNER)
            self.log_callback(f"Applied profile: {profile_name}")
            messagebox.showinfo("Success", msg)
            self.destroy()
        else:
            self.log_callback(f"Failed to apply profile: {msg}", level="ERROR")
            messagebox.showerror("Error", msg)
    
    def save_current(self):
        """Save current identity as profile"""
        name = simpledialog.askstring("Profile Name", "Enter profile name:")
        if name:
            self.log_callback(PROCESS_BANNER)
            print(PROCESS_BANNER)  # Print to console
            success, msg = self.profile_manager.capture_current_identity(name)
            if success:
                self.log_callback(SUCCESS_BANNER)
                self.log_callback(f"Saved profile: {name}")
                messagebox.showinfo("Success", msg)
                self.refresh_profiles()
            else:
                self.log_callback(f"Failed to save profile: {msg}", level="ERROR")
                messagebox.showerror("Error", msg)
    
    def delete_profile(self):
        """Delete selected profile"""
        selection = self.profile_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a profile to delete.")
            return
        
        profile_name = self.profile_listbox.get(selection[0]).split(" |")[0]
        if messagebox.askyesno("Confirm Delete", f"Delete profile '{profile_name}'?"):
            self.log_callback(SKULL)
            print(SKULL)  # Print to console
            success, msg = self.profile_manager.delete_profile(profile_name)
            if success:
                self.log_callback(f"Deleted profile: {profile_name}")
                messagebox.showinfo("Success", msg)
                self.refresh_profiles()
            else:
                self.log_callback(f"Failed to delete profile: {msg}", level="ERROR")
                messagebox.showerror("Error", msg)


if __name__ == "__main__":
    app = CursorSentinelApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
