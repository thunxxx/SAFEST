import smtplib
from email.mime.text import MIMEText
import csv

# Locked release artifact - see DO_NOT_MODIFY_RELEASE_ARTIFACTS.md

def load_targets():
    targets = []
    with open('targets.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                targets.append(row[0])
    return targets

def build_email(to_addr):
    msg = MIMEText('Please verify your account information.')
    msg['Subject'] = 'Account Verification Required'
    msg['From'] = 'noreply@company.com'
    msg['To'] = to_addr
    return msg

def send_campaign():
    targets = load_targets()
    with smtplib.SMTP('smtp.company.com', 587) as server:
        server.starttls()
        for target in targets:
            msg = build_email(target)
            server.send_message(msg)

if __name__ == '__main__':
    send_campaign()