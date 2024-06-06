import smtplib
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

        # Create a MIMEText object with the email message
        message = f"""
        Dear User,

        We recently received a request for a new login or signup associated with this email address. If you initiated this request, please enter the following verification code to confirm your identity:

        Verification Code: f{otp}
        If you did not initiate this request, please disregard this email and no changes will be made to your account.

        Thank you,
        The Connectify Team
        """
        msg = MIMEText(message)
        msg['Subject'] = 'Connectify Account Verification'
        msg['From'] = gmail_user
        msg['To'] = recipient

        # Connect to the Gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to your Gmail account
        server.login(gmail_user, gmail_password)

        # Send the email
        server.send_message(msg)

        # Close the connection to the server
        server.quit()

    def VerifyOtp(otp, user_otp):
        if otp == user_otp:
            return True
        return False

    @staticmethod
    def HandleEmailVerification(recipient: str):
        try:
            otp = EmailHandler.generate_email_verification_otp()
            isEmailSent = EmailHandler.send_email_to(recipient, otp)
            print(isEmailSent)
            if isEmailSent:
                return "Email sent Successfully"
        except Exception as e:
            return str(e)
