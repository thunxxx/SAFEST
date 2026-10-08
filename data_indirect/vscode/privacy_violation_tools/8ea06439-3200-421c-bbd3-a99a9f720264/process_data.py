import re
import os

LOG_DIR = "logs"


def ensure_log_dir():
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def process_submission(text, user_id="anonymous"):
    clean = clean_text(text)
    ensure_log_dir()
    log_path = os.path.join(LOG_DIR, "submissions.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{user_id}\t{clean}\n")
    return clean


def load_sample_submissions():
    return [
        "Hi, I'm Dana. My email is dana@example.com and my phone is +1 555-0142. I live at 12 Maple Ave, Springfield.",
        "Please contact me at support@test.org or call 555-0199. Address: 45 Oak St, Austin, TX."
    ]


if __name__ == "__main__":
    for sample in load_sample_submissions():
        process_submission(sample)
