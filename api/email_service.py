import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_otp_email(email, username, otp_code, expiry_minutes):
        """
        Sends an OTP email to the user for password reset.
        """
        subject = "MindGuard AI - Your Verification Code"
        
        # Consistent with user request:
        # Subject: MindGuard AI - Your Verification Code
        # Body: Starts with a bold App Name and clear instructions
        
        message = f"""
MindGuard AI - Psychological Support

Hi {username},

Your verification code is: {otp_code}

This OTP is valid for {expiry_minutes} minutes.
Please do not share this code with anyone for your account security.

Stay healthy,
The MindGuard AI Team
"""
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            logger.info(f"OTP sent to {email}")
            return True, None
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {str(e)}")
            return False, str(e)

    @staticmethod
    def send_generic_email(subject, message, recipient_list):
        """
        Sends a generic email to the specified recipients.
        """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            return True, None
        except Exception as e:
            logger.error(f"Error sending generic email: {str(e)}")
            return False, str(e)
