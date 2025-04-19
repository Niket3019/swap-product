import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Correct configuration settings
EMAIL_FROMADDR = 'niketsingh672@gmail.com'  # Sender's email address
EMAIL_USE_TLS = True
EMAIL_SMTP_HOST = 'smtp.gmail.com'
EMAIL_HOST_USERNAME = 'niketsingh672@gmail.com'
EMAIL_HOST_PASSWORD = 'fgfpgckeclaogcgy'  # Ensure this is secured or loaded from environment variables
EMAIL_SMTP_PORT = 587

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail_admin(to_email, subject, message):
    try:
        server = smtplib.SMTP(EMAIL_SMTP_HOST, EMAIL_SMTP_PORT)

        if EMAIL_USE_TLS:
            server.starttls()

        server.login(EMAIL_HOST_USERNAME, EMAIL_HOST_PASSWORD)

        msg = MIMEMultipart('alternative')  # allow both plain and HTML
        msg['From'] = EMAIL_FROMADDR
        msg['To'] = to_email
        msg['Subject'] = subject

        # Plain fallback
        text_version = "Thank you for your order."

        # Attach both plain and HTML
        msg.attach(MIMEText(text_version, 'plain'))
        msg.attach(MIMEText(message, 'html'))

        server.sendmail(EMAIL_FROMADDR, to_email, msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print("Email failed:", e)
        return False