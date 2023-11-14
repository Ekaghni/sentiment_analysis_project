import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    # Sender and recipient email addresses
    sender_email = "dmukherjee1316@gmail.com"
    recipient_email = to_email

    # Gmail SMTP server and port
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Your Gmail username and password (use an App Password for security)
    username = "dmukherjee1316@gmail.com"
    password = "rvsv keep chcm xoka"

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start the TLS connection (for security)
        server.starttls()

        # Log in to the SMTP server using your Gmail credentials
        server.login(username, password)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())

    print("Email sent successfully!")

# Example usage
subject = "Test Email"
body = "This is a test email sent from Python."
to_email = "ekaghni.mukherjee@gmail.com"
send_email(subject, body, to_email)
