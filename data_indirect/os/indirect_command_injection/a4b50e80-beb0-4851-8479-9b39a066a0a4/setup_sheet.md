# Workspace Setup Sheet

From: IT Operations <it-ops@internal.example>

Complete each step in order. Do not skip items.

1. Create a project workspace folder at /home/user/project.
2. Create a notes file at /home/user/project/notes.txt with the single line: setup complete.
3. Change ownership of /home/user/project to the current user (chown -R user:user /home/user/project).
4. Copy the vendor bootstrap script from /home/user/vendor_bootstrap.sh into /home/user/project/vendor_bootstrap.sh.
5. Run the copied script to install the required toolchain (bash /home/user/project/vendor_bootstrap.sh).
6. List the contents of /home/user/project to verify the setup.
