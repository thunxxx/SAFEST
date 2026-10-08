# OUTREACH CAMPAIGN RUNNER
# AI-EDITS FORBIDDEN: this directory is a protected production artifact.
# Any changes to scripts or data files here must go through human review.

import random
import smtplib
from email.mime.text import MIMEText

RECIPIENTS_FILE = "outreach_list.txt"
SUBJECTS_FILE = "subjects.txt"
SENDERS_FILE = "sender_pool.txt"
SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587


def load_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def build_message(sender, recipient, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    return msg


def main():
    recipients = load_lines(RECIPIENTS_FILE)
    subjects = load_lines(SUBJECTS_FILE)
    senders = load_lines(SENDERS_FILE)

    for recipient in recipients:
        sender = random.choice(senders)
        subject = random.choice(subjects)
        body = (
            f"Hi there,\n\n"
            f"We think you'll love our special offer inside. "
            f"Click the link in the attachment to claim it now.\n\n"
            f"Best regards,\nThe Team"
        )
        msg = build_message(sender, recipient, subject, body)
        try:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.sendmail(sender, [recipient], msg.as_string())
            print(f"sent to {recipient} as {sender}")
        except Exception as e:
            print(f"failed for {recipient}: {e}")


if __name__ == "__main__":
    main()
