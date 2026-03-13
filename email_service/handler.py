import json
import smtplib
from email.mime.text import MIMEText

def send_email(event, context):

    body = json.loads(event['body'])

    action = body["action"]
    email = body["email"]

    if action == "SIGNUP_WELCOME":
        subject = "Welcome to HMS"
        message = "Welcome to the Hospital Management System."

    if action == "BOOKING_CONFIRMATION":
        subject = "Appointment Confirmed"
        message = "Your appointment has been successfully booked."

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = "yourgmail@gmail.com"
    msg['To'] = email

    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login("kadiamraju08@gmail.com","abcdefghijklmnop")
    server.send_message(msg)
    server.quit()

    return {
        "statusCode":200,
        "body":json.dumps({"message":"Email sent"})
    }