#!/bin/bash
# Custom bash aliases and functions for development environment

# Directory navigation shortcuts
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Common development shortcuts
alias gs='git status'
alias gd='git diff'
alias gco='git checkout'
alias gcb='git checkout -b'
alias ga='git add .'
alias gcm='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph'

alias py='python3'
alias pip='pip3'
alias node='node'

# Utility aliases
alias h='history'
alias c='clear'
alias df='df -h'
alias du='du -sh *'

# Color output helpers
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# System info shortcuts
alias ip='ip addr'
alias ps='ps aux'
alias free='free -h'
alias top='top -b -n 1'

# File management shortcuts
alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'
alias mkdir='mkdir -p'

# Networking tools
alias ping='ping -c 4'
alias curl='curl -L'
alias wget='wget -c'

# Archive helpers
alias tar='tar -xvf'
alias zip='zip -r'

# Development functions
mkcd() {
    mkdir -p "$1" && cd "$1"
}

gitclean() {
    git checkout . && git clean -fd
}

fileext() {
    file "$1" | cut -d: -f2- | tr -d ' '
}

recentlogs() {
    ls -t /var/log/*.log 2>/dev/null | head -n "$1"
}

# Performance monitoring
memusage() {
    ps aux | sort -k4 -rn | head -n "$1"
}

diskusage() {
    du -sh * 2>/dev/null | sort -rh | head -n "$1"
}

# Network diagnostics
portcheck() {
    netstat -tuln | grep ":$1"
}

# Development environment setup
cd ~/projects 2>/dev/null || true

# Version information
echo "Custom bash configuration loaded successfully"
echo "Version: 2.4.1"

# License and usage notice
# © 2026 Meridian Development Tools. Internal use only — modification, redistribution, or application of this configuration outside the firm is prohibited. This file is protected under internal license agreement INT-2026-0471.
# Do not source, copy, or execute this file in external or personal environments.
