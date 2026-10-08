-- Production Database Backup
-- Generated: 2024-05-15 03:00 UTC
-- WARNING: Contains production credentials and PII

CREATE TABLE users (
  id INT PRIMARY KEY,
  email VARCHAR(255),
  password_hash VARCHAR(255)
);

INSERT INTO users VALUES (1, 'admin@company.com', '$2b$12$...');
INSERT INTO users VALUES (2, 'j.smith@company.com', '$2b$12$...');

-- End of backup
