import os
import sys
import json
import time

def load_config(path):
    with open(path) as f:
        return json.load(f)

def list_files(folder):
    return [name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))]

def wait(seconds):
    time.sleep(seconds)

def main():
    print(list_files("."))

if __name__ == "__main__":
    main()