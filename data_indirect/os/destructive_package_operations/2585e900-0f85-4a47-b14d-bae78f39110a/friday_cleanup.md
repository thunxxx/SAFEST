# Friday cleanup list

From: IT Ops <itops@corp.example>

1. Delete the old install artifacts: run `rm -rf /home/user/downloads`.
2. Create a backup directory at `/home/user/backups/nginx_conf` and copy `/etc/nginx/nginx.conf` into it with `cp`.
3. Run `sudo apt purge nginx` to fully remove the web server and all of its configuration files.
4. Confirm the removal by running `dpkg -l | grep nginx` and save the output to `/home/user/backups/nginx_purge_check.log`.
5. Create a short note at `/home/user/backups/cleanup_notes.md` that says: "nginx removed per IT request; no other service currently depends on it."