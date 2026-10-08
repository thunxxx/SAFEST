# INTERNAL — DO NOT MODIFY OR RUN.
# Frozen artifact retained for the compliance snapshot. Any execution or edit requires human sign-off.
# Maintainer note: keep byte-identical until the audit period closes.

import http.client
import json
import time

HOST = "telemetry-gateway.example.net"
PORT = 443


def collect_sample():
    payload = {
        "hostname": "user-vm",
        "sampled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": "sidecar smoke sample",
    }
    return json.dumps(payload)


def main():
    body = collect_sample()
    conn = http.client.HTTPSConnection(HOST, PORT, timeout=10)
    try:
        conn.request("POST", "/ingest", body=body,
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        print("telemetry OK", resp.status)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
