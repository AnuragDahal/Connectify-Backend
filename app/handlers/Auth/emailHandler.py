import smtplib
from fastapi import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ...utils.envutils import Environment
import random
from jose import jwt, JWTError
from ...core.database import otp_collection, user_collection
from ...handlers.exception import ErrorHandler
from datetime import datetime, timezone
env = Environment()


class EmailHandler:
    '''
    This class is responsible for handling the email verification process.'''
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

        <p>We recently received a request for a new login or signup request associated with this email address. If you initiated this request, please enter the following verification code to confirm your identity:</p>

        <p><b>Verification Code: {otp}</b></p>

        <p>If you did not initiate this request, please disregard this email and no changes will be made to your account.</p>

        <p>Thank you,<br>
        The WebService Team</p>
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

    @staticmethod
    def VerifyOtp(otp, user_otp):
        if otp == user_otp:
            return True
        return False

    @staticmethod
    async def HandleEmailVerification(recipient: str, user_email: str):
        try:
            if recipient != user_email:
                return ErrorHandler.Unauthorized("Invalid Email Address")
            otp = EmailHandler.generate_email_verification_otp()
            isEmailSent = EmailHandler.send_email_to(recipient, otp)
            # Add the otp to the database
            await otp_collection.insert_one(
                {"email": recipient, "otp": otp, "expires_on": datetime.now(timezone.utc)})
            if isEmailSent:
                return "Email sent Successfully"
            else:
                return ErrorHandler.Error("Invalid Email Address or Email not sent successfully")
        except Exception as e:
            return str(e)

    @staticmethod
    async def HandleOtpVerification(user_otp: str, user_email: str):
        # Get the otp from the database of the specific user
        email_doc = await otp_collection.find_one({"email": user_email})
        if email_doc is not None:
            otp_in_db = email_doc["otp"]
            # Verify the otp
            isOtpVerified = EmailHandler.VerifyOtp(user_otp, otp_in_db)
            if isOtpVerified:
                # Check if the user exists in the user_collection
                isUser = await user_collection.find_one({"email": user_email})
                if not isUser:
                    return ErrorHandler.NotFound("User not found in the database")
                # Update the user's email verification status
                await user_collection.update_one({"email": user_email},
                                                 {"$set": {"isEmailVerified": True}})
                # After updating the user's email verification status, delete the otp from the database
                await otp_collection.find_one_and_delete({"email": user_email})
                return "Email Verified Successfully"
            else:
                return ErrorHandler.Unauthorized("Email Verification Failed, incorrect OTP")
        return ErrorHandler.Error("Invalid Email or OTP not found in the database")
