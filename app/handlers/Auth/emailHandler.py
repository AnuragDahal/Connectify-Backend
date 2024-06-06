import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ...utils.envutils import Environment
import random

env = Environment()


class EmailHandler:
    @staticmethod
    def generate_email_verification_otp():
        # Generate a random 6-digit number
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_email_to(recipient: str, otp: int):
        # Define your Gmail username and password
        gmail_user = env.GMAIL_USER
        gmail_password = env.APP_SPECIFIC_PASS

        # Create a MIMEMultipart object
        msg = MIMEMultipart('alternative')
        html = f"""
    <html>
    <body>
        <p>Dear User,</p>

        <p>We recently received a request for a new login or signup associated with this email address. If you initiated this request, please enter the following verification code to confirm your identity:</p>

        <p><b>Verification Code: {otp}</b></p>

        <p>If you did not initiate this request, please disregard this email and no changes will be made to your account.</p>

        <p>Thank you,<br>
        The Connectify Team</p>
    </body>
    </html>
    """
        # Add the HTML content to the MIMEMultipart object
        msg.attach(MIMEText(html, 'html'))
        msg['Subject'] = 'Connectify Account Verification'
        msg['From'] = gmail_user
        msg['To'] = recipient

        # Connect to the Gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to your Gmail account
        server.login(gmail_user, gmail_password)

        # Send the email
        try:
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(str(e))
            return False

    def VerifyOtp(otp, user_otp):
        if otp == user_otp:
            return True
        return False

    @ staticmethod
    def HandleEmailVerification(recipient: str):
        try:
            otp = EmailHandler.generate_email_verification_otp()
            isEmailSent = EmailHandler.send_email_to(recipient, otp)
            if isEmailSent:
                return "Email sent Successfully"
            else:
                return "Email not sent"
        except Exception as e:
            return str(e)
