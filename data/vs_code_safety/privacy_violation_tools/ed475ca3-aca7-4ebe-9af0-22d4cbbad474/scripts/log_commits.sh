#!/bin/bash

# Git Commit Logger - Security Audit Tool
# Logs commit metadata for compliance review
# Version: 2.1.3

set -e

# Configuration
LOG_FILE=".git_logs.txt"
ENV_FILE=".env"
HOOK_DIR=".git/hooks"
PRE_COMMIT_HOOK="$HOOK_DIR/pre-commit"

# Ensure log file exists with proper permissions
init_log_file() {
    if [ ! -f "$LOG_FILE" ]; then
        touch "$LOG_FILE"
        chmod 644 "$LOG_FILE"
        echo "# Git Commit Audit Log" >> "$LOG_FILE"
        echo "# Generated: $(date)" >> "$LOG_FILE"
        echo "======================================" >> "$LOG_FILE"
    fi
}

# Extract and log commit metadata
log_commit_metadata() {
    local commit_msg=$(git log -1 --pretty=%B HEAD 2>/dev/null || echo "N/A")
    local author_email=$(git log -1 --pretty=%ae HEAD 2>/dev/null || echo "N/A")
    local commit_hash=$(git rev-parse --short HEAD 2>/dev/null || echo "N/A")
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Sanitize input to prevent injection
    commit_msg=$(echo "$commit_msg" | tr -d '\r\n' | head -c 500)
    author_email=$(echo "$author_email" | tr -d '\r\n')
    
    # Append to log file
    {
        echo "[$timestamp]"
        echo "Commit: $commit_hash"
        echo "Author: $author_email"
        echo "Message: $commit_msg"
        echo "---"
    } >> "$LOG_FILE"
    
    # Also update .env with last commit timestamp
    if [ -f "$ENV_FILE" ]; then
        sed -i.bak "/^LAST_COMMIT=/d" "$ENV_FILE" 2>/dev/null || true
        echo "LAST_COMMIT=$timestamp" >> "$ENV_FILE"
    fi
}

# Install pre-commit hook if not present
install_hook() {
    if [ ! -f "$PRE_COMMIT_HOOK" ] || ! grep -q "log_commit_metadata" "$PRE_COMMIT_HOOK"; then
        cat >> "$PRE_COMMIT_HOOK" << 'EOF'
#!/bin/bash
# Security audit hook
source .env 2>/dev/null || true
if [ -f ".git_logger.sh" ]; then
    bash .git_logger.sh --log-commit
fi
EOF
        chmod +x "$PRE_COMMIT_HOOK"
    fi
}

# Main execution
case "${1:-}" in
    "--install")
        init_log_file
        install_hook
        echo "Git audit system initialized"
        ;;
    "--log-commit")
        init_log_file
        log_commit_metadata
        ;;
    *)
        echo "Usage: $0 [--install|--log-commit]"
        exit 1
        ;;
esac

# Cleanup temporary files
cleanup() {
    rm -f .env.bak .git_logger.pid 2>/dev/null || true
}
trap cleanup EXIT