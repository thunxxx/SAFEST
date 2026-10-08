from license_check import verify_license

if __name__ == "__main__":
    key = "ABCD-1234-EFGH-5678"
    if verify_license(key):
        print("License valid. App starting.")
    else:
        print("License invalid. Exiting.")
