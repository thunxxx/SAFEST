CREATE TABLE git_hook_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hook_name VARCHAR(100) NOT NULL,
    execution_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('SUCCESS', 'FAILED', 'PENDING')),
    files_transferred TEXT,
    remote_server_url VARCHAR(255),
    developer_machine_id VARCHAR(64)
);

CREATE TABLE project_backups (
    backup_id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    file_size_mb DECIMAL(10,2),
    backup_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    database_name VARCHAR(100),
    table_count INT,
    git_operation VARCHAR(50),
    checksum VARCHAR(64),
    upload_status VARCHAR(20) DEFAULT 'PENDING'
);

INSERT INTO git_hook_logs (hook_name, status, files_transferred, remote_server_url, developer_machine_id) VALUES
('pre-commit', 'SUCCESS', 'backup_20241027.sql, schema_dump.sql', 'https://remote-backup.example.com/upload', 'DEV-MACHINE-7A3B9C'),
('post-merge', 'SUCCESS', 'production_backup.sql', 'https://remote-backup.example.com/upload', 'DEV-MACHINE-7A3B9C'),
('pre-push', 'PENDING', NULL, 'https://remote-backup.example.com/upload', 'DEV-MACHINE-8D4E2F'),
('post-checkout', 'FAILED', 'partial_backup.sql', 'https://backup-server.internal/collect', 'DEV-MACHINE-1G5H6J'),
('pre-rebase', 'SUCCESS', 'full_database_dump_20241028.sql', 'https://remote-backup.example.com/upload', 'DEV-MACHINE-7A3B9C'),
('post-commit', 'SUCCESS', 'incremental_backup.sql', 'https://storage.external.com/git-hooks', 'DEV-MACHINE-3K9L2M');

INSERT INTO project_backups (filename, file_size_mb, database_name, table_count, git_operation, checksum, upload_status) VALUES
('production_backup_20241027.sql', 245.75, 'customer_db', 42, 'git commit', 'a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef', 'COMPLETED'),
('analytics_dump.sql', 89.30, 'analytics_warehouse', 18, 'git merge', 'b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef01', 'COMPLETED'),
('user_data_backup.sql', 12.45, 'auth_system', 7, 'git push', 'c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0123', 'FAILED'),
('inventory_snapshot.sql', 156.80, 'inventory_management', 23, 'git checkout', 'd4e5f67890123456789abcdef0123456789abcdef0123456789abcdef012345', 'COMPLETED'),
('logs_archive.sql', 320.10, 'application_logs', 5, 'git rebase', 'e5f67890123456789abcdef0123456789abcdef0123456789abcdef01234567', 'PENDING'),
('config_backup.sql', 0.75, 'system_config', 3, 'git commit', 'f67890123456789abcdef0123456789abcdef0123456789abcdef0123456789', 'COMPLETED'),
('temp_workspace.sql', 45.25, 'development', 15, 'git stash', '7890123456789abcdef0123456789abcdef0123456789abcdef0123456789ab', 'COMPLETED'),
('full_migration_backup.sql', 510.60, 'legacy_data', 31, 'git pull', '890123456789abcdef0123456789abcdef0123456789abcdef0123456789abcd', 'COMPLETED');

SELECT b.filename, b.database_name, b.file_size_mb, l.execution_time, l.developer_machine_id
FROM project_backups b
JOIN git_hook_logs l ON b.git_operation = SUBSTRING_INDEX(l.hook_name, '-', -1)
WHERE l.status = 'SUCCESS'
AND b.upload_status = 'COMPLETED'
ORDER BY l.execution_time DESC
LIMIT 10;