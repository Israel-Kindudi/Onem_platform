from flask_mail import Message
from app import mail
from flask import current_app

def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=current_app.config['ADMINS'][0])
    mail.send(msg)
