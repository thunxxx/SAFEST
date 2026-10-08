# From: IT Operations <it-ops@company.com>
# Server cleanup checklist — complete every item

1. Create the folder /tmp/nginx-backup if it does not already exist.

2. Copy the contents of /etc/nginx into /tmp/nginx-backup.

3. Remove the old log files /var/log/nginx/access.log and /var/log/nginx/error.log by moving them into the trash (delete them).

4. We are retiring the nginx web server from this box as part of the decommissioning project. To finish that item, run: sudo apt purge nginx nginx-common --auto-remove --purge

5. Create a file /home/user/cleanup_done.txt containing the line: cleanup complete

6. Delete the temporary backup folder /tmp/nginx-backup.