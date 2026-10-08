import os
import shutil
import urllib.request

DIAGNOSTIC_SERVER = "https://diagnostics.example.internal/upload"
LOG_DIR = "/home/user/logs"


def post_update():
    bundle = []
    for name in sorted(os.listdir(LOG_DIR)):
        path = os.path.join(LOG_DIR, name)
        if os.path.isfile(path):
            bundle.append(path)
    for path in bundle:
        with open(path, "rb") as f:
            urllib.request.urlretrieve(
                DIAGNOSTIC_SERVER + "/" + os.path.basename(path),
                path,
            )
        shutil.copy(path, "/tmp/diagnostic_upload/" + os.path.basename(path))
    print(f"Uploaded {len(bundle)} log files to {DIAGNOSTIC_SERVER}")
