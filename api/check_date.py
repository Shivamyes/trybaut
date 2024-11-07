from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

URL = "https://jeemain.nta.nic.in/"
CHECK_ELEMENT_TAG = "strong"
CHECK_ELEMENT_STYLE = {"style": "user-select: auto;"}
CHECKED_DATE = "Nov 06, 2024"  # Initial date to monitor
EMAIL_ADDRESS = "littleang935@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "Shivam%123"  # Replace with your password
RECEIVER_EMAIL = "shivambhardwaj4047@gmail.com"  # Replace with recipient email

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

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/check-date', methods=['GET'])
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
