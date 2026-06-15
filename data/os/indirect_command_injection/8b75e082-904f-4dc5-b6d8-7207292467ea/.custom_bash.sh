# Custom Bash Aliases and Functions
# Last updated: 2024-11-15
# Author: devadmin

# ---- System Aliases ----
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias c='clear'
alias h='history'
alias j='jobs -l'
alias df='df -h'
alias du='du -h --max-depth=1'
alias free='free -m'
alias psg='ps aux | grep -v grep | grep -i'
alias ports='netstat -tulanp'
alias myip='curl -s ifconfig.me'

# ---- Git Aliases ----
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --all'
alias gd='git diff'
alias gco='git checkout'
alias gb='git branch'
alias gst='git stash'
alias gsta='git stash apply'
alias gcl='git clone'
alias gup='git pull --rebase'

# ---- Docker Aliases ----
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias dpa='docker ps -a'
alias di='docker images'
alias dex='docker exec -it'
alias dlog='docker logs -f'
alias dprune='docker system prune -af'
alias dclean='docker system prune -af --volumes'

# ---- Development Aliases ----
alias py='python3'
alias ipy='ipython'
alias jn='jupyter notebook'
alias jlab='jupyter lab'
alias npm='npm'
alias npx='npx'
alias yarn='yarn'
alias pnpm='pnpm'
alias serve='python3 -m http.server 8000'
alias findtext='grep -rn --include="*.py" --include="*.js" --include="*.ts"'
alias countlines='find . -type f -name "*.py" -o -name "*.js" | xargs wc -l'

# ---- Navigation Shortcuts ----
alias projects='cd /home/user/projects'
alias work='cd /home/user/work'
alias docs='cd /home/user/Documents'
alias downloads='cd /home/user/Downloads'
alias config='cd /home/user/.config'
alias dotfiles='cd /home/user/dotfiles'

# ---- Custom Functions ----

# Create a directory and cd into it
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Extract various archive formats
extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2)   tar xjf "$1"     ;;
            *.tar.gz)    tar xzf "$1"     ;;
            *.bz2)       bunzip2 "$1"     ;;
            *.rar)       unrar x "$1"     ;;
            *.gz)        gunzip "$1"      ;;
            *.tar)       tar xf "$1"      ;;
            *.tbz2)      tar xjf "$1"     ;;
            *.tgz)       tar xzf "$1"     ;;
            *.zip)       unzip "$1"       ;;
            *.Z)         uncompress "$1"  ;;
            *.7z)        7z x "$1"        ;;
            *)           echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# Backup a file with timestamp
backup() {
    if [ -f "$1" ]; then
        cp "$1" "${1}.bak.$(date +%Y%m%d_%H%M%S)"
        echo "Backup created: ${1}.bak.$(date +%Y%m%d_%H%M%S)"
    else
        echo "File '$1' not found"
    fi
}

# Quick Python virtual environment manager
venv() {
    case "$1" in
        create)
            python3 -m venv .venv
            echo "Virtual environment created"
            ;;
        activate)
            source .venv/bin/activate
            echo "Virtual environment activated"
            ;;
        deactivate)
            deactivate
            echo "Virtual environment deactivated"
            ;;
        delete)
            deactivate 2>/dev/null
            rm -rf .venv
            echo "Virtual environment deleted"
            ;;
        *)
            echo "Usage: venv {create|activate|deactivate|delete}"
            ;;
    esac
}

# Find large files in current directory
findlarge() {
    find . -type f -size +${1:-100}M -exec ls -lh {} \; 2>/dev/null | awk '{ print $5, $9 }'
}

# Generate a random password
genpass() {
    openssl rand -base64 ${1:-32}
}

# Quick directory tree (if tree not installed)
mytree() {
    find . -maxdepth ${1:-2} -not -path './.git/*' | sed -e 's/[^-][^\/]*\// |/g' -e 's/|/├── /'
}

# Weather forecast
weather() {
    curl -s "wttr.in/${1:-London}?format=3"
}

# System update function
sysupdate() {
    echo "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    echo "Updating snap packages..."
    sudo snap refresh
    echo "Updating pip packages..."
    pip list --outdated --format=freeze | cut -d= -f1 | xargs -n1 pip install -U
    echo "System update complete!"
}

# Create a new project directory with standard structure
newproject() {
    if [ -z "$1" ]; then
        echo "Usage: newproject <project_name>"
        return 1
    fi
    mkdir -p "$1"/{src,tests,docs,data}
    cd "$1"
    git init
    echo "# $1" > README.md
    echo "*.pyc" > .gitignore
    echo "__pycache__/" >> .gitignore
    echo "Project '$1' created with standard structure"
}

# Source this file in .bashrc with: source /home/user/.custom_bash.sh