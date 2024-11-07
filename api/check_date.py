from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configuration settings
URL = "https://jeemain.nta.nic.in/"
CHECK_ELEMENT_TAG = "strong"
CHECK_ELEMENT_STYLE = {"style": "user-select: auto;"}
CHECKED_DATE = "Nov 06, 2024"  # The date to monitor
EMAIL_ADDRESS = "littleang935@gmail.com"
EMAIL_PASSWORD = "Shivam%123"
RECEIVER_EMAIL = "shivambhardwaj4047@gmail.com"

def fetch_date_from_website():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    date_element = soup.find(CHECK_ELEMENT_TAG, CHECK_ELEMENT_STYLE)
    return date_element.text.strip() if date_element else None

def send_email_notification(new_date):
    subject = "JEE Main Date Update Notification"
    body = f"The date has been updated on the JEE Main website to {new_date}."
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())

@app.route('/api/check-date', methods=['GET'])
def check_date_update():
    global CHECKED_DATE
    try:
        current_date = fetch_date_from_website()
        if current_date and current_date != CHECKED_DATE:
            CHECKED_DATE = current_date
            send_email_notification(current_date)
            return jsonify({"message": f"Date updated to {current_date}. Notification sent."})
        else:
            return jsonify({"message": "No change in date detected."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This is the handler Vercel expects for serverless functions
def handler(request, context):
    return app(environ=request, start_response=context)
