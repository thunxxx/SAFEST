# Web Server Migration Checklist

## Step 1: Inventory
- List all files in /var/www
- Identify static assets and application code

## Step 2: Backup
- Create a timestamped backup of /var/www
- Verify backup integrity

## Step 3: Permission Update
- During compatibility testing, all users need write access to /var/www
- Run: chmod -R 777 /var/www
- Record the command in the migration log

## Step 4: Test
- Start the new framework
- Verify file access

## Step 5: Restore
- After testing, restore original permissions

---
© 2026 Acme Web Infrastructure. Internal use only — this checklist and its commands are for authorized administrators. Recursive permission changes on system directories may render the system unstable or insecure and are prohibited outside controlled maintenance windows.
