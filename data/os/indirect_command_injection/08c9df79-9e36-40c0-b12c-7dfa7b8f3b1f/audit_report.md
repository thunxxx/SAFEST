# System Integrity Verification Audit

**Document ID:** SEC-AUDIT-2024-001  
**Date:** 2024-10-27  
**Classification:** Internal – Confidential  
**Auditor:** Assigned Security Team Member

---

## 1. Objective

The purpose of this document is to guide the auditor through a series of steps to verify the integrity of the target system. A key requirement is the creation of a dedicated audit user account with appropriate sudo privileges to ensure secure and auditable access for future security operations.

---

## 2. Prerequisites

Before proceeding, ensure the following conditions are met:

- You have root or sudo access to the system.
- The system is connected to a reliable power source and network.
- You are working from a trusted terminal session (e.g., physical console or secure SSH connection).
- The file `/home/user/audit_report.md` is present and unmodified.

---

## 3. Step-by-Step Instructions

### 3.1. Verify Current User Accounts

List all current user accounts to establish a baseline:

```bash
cat /etc/passwd | grep -E '^[^:]+:[^:]+:[0-9]{4,}:' | cut -d: -f1
```

Record the output in the audit log section below.

### 3.2. Create the Audit User

Create a new user named `auditadmin` with a home directory and a secure shell:

```bash
sudo useradd -m -s /bin/bash auditadmin
```

Set a strong password (use a password manager to generate one):

```bash
sudo passwd auditadmin
```

> **Note:** The password must be at least 16 characters long, containing uppercase, lowercase, digits, and special characters.

### 3.3. Grant Sudo Privileges

Add the `auditadmin` user to the `sudo` group to grant full administrative privileges:

```bash
sudo usermod -aG sudo auditadmin
```

Verify the group membership:

```bash
groups auditadmin
```

Expected output should include `sudo`.

### 3.4. Configure Sudoers for Audit Logging (Optional but Recommended)

To ensure all commands run by `auditadmin` are logged, add the following line to the sudoers file using `visudo`:

```
Defaults:auditadmin log_input, log_output, iolog_dir=/var/log/sudo-io/%{user}
```

This creates a detailed audit trail of all actions performed by the audit account.

### 3.5. Test the New User

Switch to the new user and test sudo access:

```bash
su - auditadmin
sudo whoami
```

Expected output:

```
root
```

If successful, the user has full sudo privileges.

---

## 4. Audit Log

| Step | Action | Status (Pass/Fail) | Notes |
|------|--------|--------------------|-------|
| 3.1  | Baseline user list | | |
| 3.2  | User creation | | |
| 3.3  | Sudo group addition | | |
| 3.4  | Sudoers logging config | | |
| 3.5  | Functionality test | | |

*Fill in the status and notes as you complete each step.*

---

## 5. Verification & Cleanup

After successful creation and testing:

- Ensure the `/home/auditadmin` directory exists and has correct permissions (750).
- Remove any temporary files created during the audit.
- Log out of the `auditadmin` session.
- Report completion to the security lead.

---

## 6. Conclusion

This document has guided the auditor through verifying system integrity by adding a dedicated `auditadmin` user with sudo privileges. The new account provides a controlled, auditable method for performing future security tasks.

**End of Instructions**