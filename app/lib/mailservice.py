from flask_mail import Message

def MailSender(mail,to,body,message):
     # Create and send an email
    msg = Message(message, recipients=[to])
    msg.body = body
    mail.send(msg)
