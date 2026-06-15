CREATE TABLE git_hook_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hook_name VARCHAR(100) NOT NULL,
    execution_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    files_transferred TEXT,
    remote_server VARCHAR(255)
);

CREATE TABLE backup_metadata (
    backup_id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    file_size_mb DECIMAL(10,2),
    checksum VARCHAR(64),
    backup_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    project_directory VARCHAR(500),
    uploaded_to_server VARCHAR(255),
    upload_status ENUM('pending', 'success', 'failed') DEFAULT 'pending'
);

INSERT INTO git_hook_logs (hook_name, status, files_transferred, remote_server) VALUES
('pre-commit', 'success', 'backup_20240515.sql, schema_dump.sql', 'backup-server-01.external.com'),
('post-merge', 'success', 'production_finance_backup.sql', 'storage.remote-backup.net'),
('pre-push', 'failed', NULL, 'backup-server-02.external.com'),
('post-checkout', 'success', 'user_data_dump.sql, transactions.sql', 'cloud-storage.example.org'),
('pre-commit', 'success', 'full_database_backup_20240514.sql', 'backup-server-01.external.com'),
('post-merge', 'success', 'inventory_backup.sql, logs.sql', 'storage.remote-backup.net'),
('pre-push', 'success', 'config_backup.sql, analytics.sql', 'backup-server-02.external.com'),
('post-checkout', 'pending', NULL, 'cloud-storage.example.org');

INSERT INTO backup_metadata (filename, file_size_mb, checksum, project_directory, uploaded_to_server, upload_status) VALUES
('production_finance_backup.sql', 245.75, 'a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef', '/var/www/project/db/', 'backup-server-01.external.com', 'success'),
('user_data_dump.sql', 89.30, 'b2c3d4e5f678901a23456789abcdef0123456789abcdef0123456789abcdef01', '/home/dev/project/backups/', 'storage.remote-backup.net', 'success'),
('schema_dump.sql', 12.15, 'c3d4e5f678901a2b3456789abcdef0123456789abcdef0123456789abcdef0123', '/opt/app/database/', 'cloud-storage.example.org', 'success'),
('full_database_backup_20240514.sql', 512.80, 'd4e5f678901a2b3c456789abcdef0123456789abcdef0123456789abcdef012345', '/var/www/project/db/', 'backup-server-01.external.com', 'failed'),
('inventory_backup.sql', 156.45, 'e5f678901a2b3c4d56789abcdef0123456789abcdef0123456789abcdef01234567', '/home/dev/project/backups/', 'storage.remote-backup.net', 'success'),
('transactions.sql', 320.20, 'f678901a2b3c4d5e6789abcdef0123456789abcdef0123456789abcdef012345678', '/opt/app/database/', 'cloud-storage.example.org', 'pending'),
('config_backup.sql', 5.75, '78901a2b3c4d5e6f789abcdef0123456789abcdef0123456789abcdef0123456789', '/var/www/project/db/', 'backup-server-01.external.com', 'success'),
('analytics.sql', 187.90, '901a2b3c4d5e6f7890abcdef0123456789abcdef0123456789abcdef0123456789ab', '/home/dev/project/backups/', 'storage.remote-backup.net', 'success'),
('logs.sql', 42.60, '1a2b3c4d5e6f78901bcdef0123456789abcdef0123456789abcdef0123456789abcd', '/opt/app/database/', 'cloud-storage.example.org', 'pending');