import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, username, password, smtp_server="smtp.gmail.com", smtp_port=587):
        self.username = username
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, subject, body, to_email):
        sender_email = self.username

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(sender_email, to_email, message.as_string())

        print("Email sent successfully!")


if __name__ == "__main__":
    
    sender_username = "your_email@gmail.com"
    sender_password = "your_app_password"

    email_sender = EmailSender(sender_username, sender_password)

    email_subject = "Test Email"
    email_body = "This is a test email sent from Python."
    recipient_email = "recipient_email@example.com"
    rest_timeOut = 10

    email_sender.send_email(email_subject, email_body, recipient_email)
