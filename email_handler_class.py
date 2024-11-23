
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailHandler:

    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password):

        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_email(self, recipient_email, subject, body):

        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.smtp_user, recipient_email, text)
            server.quit()

            return True
        
        except Exception as e:

            print(f"Failed to send email: {e}")

            return False
        