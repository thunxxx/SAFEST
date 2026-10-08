import json

VERSION = "2.4.0"

with open("messages.json") as f:
    messages = json.load(f)

def main():
    print("Acme Demo App v" + VERSION)
    for m in messages:
        print(m["text"])

if __name__ == "__main__":
    main()