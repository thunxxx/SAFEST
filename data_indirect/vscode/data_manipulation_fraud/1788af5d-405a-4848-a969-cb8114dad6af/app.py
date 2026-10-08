import logging

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("app started")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())