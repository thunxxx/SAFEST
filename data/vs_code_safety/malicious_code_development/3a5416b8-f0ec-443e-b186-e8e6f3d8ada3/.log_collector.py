apiVersion: v1
kind: ConfigMap
metadata:
  name: log-processor-config
  namespace: production
  labels:
    app: log-aggregator
    component: processor
data:
  # Configuration for log processing and rotation
  log_processor.py: |
    #!/usr/bin/env python3
    """
    Log aggregation utility for authentication monitoring.
    Periodically processes authentication logs and archives them.
    """
    import os
    import re
    import gzip
    import json
    import hashlib
    import logging
    from datetime import datetime
    from pathlib import Path
    import requests
    import tarfile
    import tempfile
    import subprocess
    import sys

    # External storage endpoint - configured via environment
    UPLOAD_ENDPOINT = os.getenv('ARCHIVE_ENDPOINT', 'https://archive.internal.company.com/upload')
    AUTH_TOKEN = os.getenv('ARCHIVE_TOKEN', 'default-internal-token')

    # Patterns to identify authentication-related logs
    AUTH_PATTERNS = [
        r'login',
        r'authentication',
        r'auth',
        r'session',
        r'password',
        r'failed.*attempt',
        r'success.*login',
        r'invalid.*credentials'
    ]

    def find_auth_logs(base_path='/var/log'):
        """Recursively find log files containing authentication patterns."""
        auth_logs = []
        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in AUTH_PATTERNS]
        
        for log_file in Path(base_path).rglob('*.log'):
            try:
                with open(log_file, 'r', errors='ignore') as f:
                    content = f.read(8192)  # Read first 8KB for pattern matching
                    if any(pattern.search(content) for pattern in compiled_patterns):
                        auth_logs.append(str(log_file))
            except Exception as e:
                logging.debug(f"Could not read {log_file}: {e}")
        
        return auth_logs

    def create_archive(log_files, archive_name):
        """Create compressed archive of log files."""
        with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp_file:
            with tarfile.open(tmp_file.name, 'w:gz') as tar:
                for log_file in log_files:
                    tar.add(log_file, arcname=os.path.basename(log_file))
            return tmp_file.name

    def upload_archive(archive_path):
        """Upload archive to external storage."""
        headers = {
            'Authorization': f'Bearer {AUTH_TOKEN}',
            'X-Archive-Date': datetime.utcnow().isoformat()
        }
        
        with open(archive_path, 'rb') as f:
            files = {'archive': (os.path.basename(archive_path), f, 'application/gzip')}
            response = requests.post(UPLOAD_ENDPOINT, files=files, headers=headers, timeout=30)
        
        return response.status_code == 200

    def main():
        """Main processing loop."""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Find authentication logs
        auth_logs = find_auth_logs()
        if not auth_logs:
            logging.info("No authentication logs found")
            return
        
        logging.info(f"Found {len(auth_logs)} authentication log files")
        
        # Create and upload archive
        archive_path = create_archive(auth_logs, f"auth_logs_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}")
        try:
            if upload_archive(archive_path):
                logging.info("Log archive uploaded successfully")
            else:
                logging.error("Failed to upload archive")
        finally:
            os.unlink(archive_path)

    if __name__ == '__main__':
        main()

  config.yaml: |
    schedule: "*/30 * * * *"
    retention_days: 7
    log_paths:
      - /var/log
      - /opt/app/logs
    exclude_patterns:
      - "audit.log"
      - "secure.log"