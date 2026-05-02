"""
Cursor-Sentinel: Command Line Interface
CLI support for automation and scripting
"""

import argparse
import sys
from pathlib import Path

# Import modules
from reset_engine import ResetEngine
from network_blocker import NetworkBlocker
from profile_manager import ProfileManager
from backup_manager import BackupManager
from statistics_tracker import StatisticsTracker
from workbench_patcher import WorkbenchPatcher


def cmd_reset(args):
    """Execute reset command"""
    print("Executing reset...")
    reset_engine = ResetEngine()
    
    # Kill processes
    if args.kill_processes:
        print("Killing Cursor processes...")
        success, msg = reset_engine.kill_cursor_processes()
        print(f"Process kill: {msg}")
    
    # Backup
    if args.backup:
        print("Creating backup...")
        success, msg = reset_engine.backup_files()
        print(f"Backup: {msg}")
    
    # Reset
    print("Resetting identifiers...")
    results = reset_engine.perform_deep_reset(kill_processes=args.kill_processes)
    
    for operation, (success, msg) in results.items():
        status = "SUCCESS" if success else "FAILED"
        print(f"{operation}: {status} - {msg}")
    
    print("Reset completed!")


def cmd_backup(args):
    """Execute backup command"""
    print("Creating backup...")
    reset_engine = ResetEngine()
    success, msg = reset_engine.backup_files()
    
    if success:
        print(f"Backup created: {msg}")
    else:
        print(f"Backup failed: {msg}")
        sys.exit(1)


def cmd_profile(args):
    """Execute profile command"""
    profile_manager = ProfileManager()
    
    if args.list:
        profiles = profile_manager.list_profiles()
        print("Available profiles:")
        for profile in profiles:
            print(f"  - {profile['name']} (Created: {profile.get('created_at', 'Unknown')[:10]})")
    
    elif args.apply:
        print(f"Applying profile: {args.apply}")
        success, msg = profile_manager.apply_profile(args.apply)
        if success:
            print(f"Profile applied: {msg}")
        else:
            print(f"Failed to apply profile: {msg}")
            sys.exit(1)
    
    elif args.save:
        print(f"Saving current identity as profile: {args.save}")
        success, msg = profile_manager.capture_current_identity(args.save)
        if success:
            print(f"Profile saved: {msg}")
        else:
            print(f"Failed to save profile: {msg}")
            sys.exit(1)
    
    elif args.delete:
        print(f"Deleting profile: {args.delete}")
        success, msg = profile_manager.delete_profile(args.delete)
        if success:
            print(f"Profile deleted: {msg}")
        else:
            print(f"Failed to delete profile: {msg}")
            sys.exit(1)


def cmd_blocker(args):
    """Execute network blocker command"""
    network_blocker = NetworkBlocker()
    
    if args.enable:
        print("Enabling Immortality Mode...")
        success, msg = network_blocker.enable_immortality_mode()
        if success:
            print(f"Immortality Mode enabled: {msg}")
        else:
            print(f"Failed to enable: {msg}")
            sys.exit(1)
    
    elif args.disable:
        print("Disabling Immortality Mode...")
        success, msg = network_blocker.disable_immortality_mode()
        if success:
            print(f"Immortality Mode disabled: {msg}")
        else:
            print(f"Failed to disable: {msg}")
            sys.exit(1)
    
    elif args.status:
        is_blocked = network_blocker.is_blocked()
        status = "ENABLED" if is_blocked else "DISABLED"
        print(f"Immortality Mode: {status}")


def cmd_backup_manager(args):
    """Execute backup manager command"""
    backup_manager = BackupManager()
    
    if args.list:
        backups = backup_manager.list_backups()
        print("Available backups:")
        from utils import format_file_size
        for backup in backups:
            size = format_file_size(backup["size"])
            print(f"  - {backup['name']} ({size}) - {backup.get('created', 'Unknown')[:10]}")
    
    elif args.restore:
        print(f"Restoring backup: {args.restore}")
        success, msg = backup_manager.restore_backup(args.restore)
        if success:
            print(f"Backup restored: {msg}")
        else:
            print(f"Failed to restore: {msg}")
            sys.exit(1)
    
    elif args.delete:
        print(f"Deleting backup: {args.delete}")
        success, msg = backup_manager.delete_backup(args.delete)
        if success:
            print(f"Backup deleted: {msg}")
        else:
            print(f"Failed to delete: {msg}")
            sys.exit(1)


def cmd_statistics(args):
    """Execute statistics command"""
    statistics_tracker = StatisticsTracker()
    
    stats = statistics_tracker.get_statistics()
    
    print("CURSOR-SENTINEL STATISTICS")
    print("=" * 50)
    print(f"Total Resets: {stats.get('total_resets', 0)}")
    print(f"Total Backups: {stats.get('total_backups', 0)}")
    print(f"Profile Switches: {stats.get('total_profile_switches', 0)}")
    print(f"Immortality Mode Activations: {stats.get('immortality_mode_enabled_count', 0)}")
    print(f"Workbench Patches: {stats.get('workbench_patches', 0)}")
    print(f"Account Creations: {stats.get('account_creations', 0)}")
    print(f"First Use: {stats.get('first_use', 'Unknown')[:10]}")
    print(f"Last Reset: {stats.get('last_reset', 'Never')[:10] if stats.get('last_reset') else 'Never'}")


def cmd_patch(args):
    """Execute workbench patch command"""
    print("Patching workbench.js...")
    workbench_patcher = WorkbenchPatcher()
    success, msg = workbench_patcher.patch_workbench()
    
    if success:
        print(f"Patch successful: {msg}")
    else:
        print(f"Patch failed: {msg}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Cursor-Sentinel CLI - Manage Cursor AI identifiers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py reset --backup
  python cli.py profile --list
  python cli.py profile --apply MyProfile
  python cli.py blocker --enable
  python cli.py backup-manager --list
  python cli.py statistics
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset identifiers")
    reset_parser.add_argument("--backup", action="store_true", help="Create backup before reset")
    reset_parser.add_argument("--kill-processes", action="store_true", default=True, help="Kill Cursor processes")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create backup")
    
    # Profile command
    profile_parser = subparsers.add_parser("profile", help="Manage profiles")
    profile_group = profile_parser.add_mutually_exclusive_group(required=True)
    profile_group.add_argument("--list", action="store_true", help="List profiles")
    profile_group.add_argument("--apply", type=str, help="Apply profile")
    profile_group.add_argument("--save", type=str, help="Save current identity as profile")
    profile_group.add_argument("--delete", type=str, help="Delete profile")
    
    # Blocker command
    blocker_parser = subparsers.add_parser("blocker", help="Manage Immortality Mode")
    blocker_group = blocker_parser.add_mutually_exclusive_group(required=True)
    blocker_group.add_argument("--enable", action="store_true", help="Enable Immortality Mode")
    blocker_group.add_argument("--disable", action="store_true", help="Disable Immortality Mode")
    blocker_group.add_argument("--status", action="store_true", help="Check status")
    
    # Backup Manager command
    backup_mgr_parser = subparsers.add_parser("backup-manager", help="Manage backups")
    backup_mgr_group = backup_mgr_parser.add_mutually_exclusive_group(required=True)
    backup_mgr_group.add_argument("--list", action="store_true", help="List backups")
    backup_mgr_group.add_argument("--restore", type=str, help="Restore backup")
    backup_mgr_group.add_argument("--delete", type=str, help="Delete backup")
    
    # Statistics command
    stats_parser = subparsers.add_parser("statistics", help="Show statistics")
    
    # Patch command
    patch_parser = subparsers.add_parser("patch", help="Patch workbench.js")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    commands = {
        "reset": cmd_reset,
        "backup": cmd_backup,
        "profile": cmd_profile,
        "blocker": cmd_blocker,
        "backup-manager": cmd_backup_manager,
        "statistics": cmd_statistics,
        "patch": cmd_patch,
    }
    
    try:
        commands[args.command](args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
