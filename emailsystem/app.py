import logging
from flask import Flask, jsonify, make_response ,request
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

@app.route("/send",methods=['POST'])
def send():
    data = request.get_json()
    receiver_email = data.get('receiver_email')
    subject = data.get('subject')
    body = data.get('body')
    
    if not receiver_email or not subject or not body:
        return make_response(jsonify(error='Invalid request!'), 400)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
            
            message = f'Subject: {subject}\n\n{body}'
            server.sendmail(os.getenv('EMAIL_USER'), receiver_email, message)
    
        app.logger.info("Email sent successfully.")    
        return make_response(jsonify(message='Email sent successfully!'), 200)
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return make_response(jsonify(error=f'Failed to send email: {e}'), 500)

