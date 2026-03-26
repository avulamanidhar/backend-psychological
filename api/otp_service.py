import random
import os
import logging
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from .models import PasswordResetOTP, PasswordResetLog
from .email_service import EmailService

logger = logging.getLogger(__name__)

class OTPService:
    @staticmethod
    def generate_and_send_otp(identifier, request_meta):
        """
        Generates and sends an OTP if the user exists.
        Implements rate limiting and generic responses.
        """
        # 1. Rate Limiting Check
        one_hour_ago = timezone.now() - timedelta(hours=1)
        recent_requests = PasswordResetLog.objects.filter(
            email=identifier, 
            action='REQUEST', 
            timestamp__gte=one_hour_ago
        ).count()
        
        if recent_requests >= 3:
            PasswordResetLog.objects.create(
                email=identifier,
                action='RATE_LIMIT_HIT',
                ip_address=request_meta.get('REMOTE_ADDR')
            )
            return False, "Too many requests. Please try again after an hour."

        # 2. Log Attempt
        PasswordResetLog.objects.create(
            email=identifier,
            action='REQUEST',
            ip_address=request_meta.get('REMOTE_ADDR')
        )

        try:
            from django.db.models import Q
            user = User.objects.get(Q(username=identifier) | Q(email=identifier))
        except User.DoesNotExist:
            # Generic response to prevent enumeration
            return True, "If an account exists with that email, an OTP has been sent."

        # 3. OTP Generation
        otp_code = str(random.randint(100000, 999999))
        expiry_minutes = int(os.getenv('OTP_EXPIRY_MINUTES', 5))
        expiry_time = timezone.now() + timedelta(minutes=expiry_minutes)

        # 4. Invalidate old OTPs for this email
        PasswordResetOTP.objects.filter(email=user.email).delete()

        # 5. Save new OTP
        PasswordResetOTP.objects.create(
            user=user,
            email=user.email,
            otp=otp_code,
            expiry_time=expiry_time
        )

        # 6. Send Email
        success, error_msg = EmailService.send_otp_email(user.email, user.username, otp_code, expiry_minutes)
        if not success:
            logger.error(f"OTP Email delivery failed for {user.email}: {error_msg}")
            PasswordResetLog.objects.create(
                email=user.email,
                action='EMAIL_SEND_FAIL',
                ip_address=request_meta.get('REMOTE_ADDR')
            )
        
        return True, "If an account exists with that email, an OTP has been sent."

    @staticmethod
    def verify_otp(identifier, otp_code, request_meta):
        """
        Verifies the provided OTP code.
        """
        try:
            from django.db.models import Q
            user = User.objects.get(Q(username=identifier) | Q(email=identifier))
            # Get active OTP
            otp_obj = PasswordResetOTP.objects.get(user=user, otp=otp_code)
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            PasswordResetLog.objects.create(
                email=identifier,
                action='VERIFY_FAIL',
                ip_address=request_meta.get('REMOTE_ADDR')
            )
            return False, "Invalid OTP or identifier."

        # 1. Check Expiry
        if otp_obj.expiry_time < timezone.now():
            otp_obj.delete()
            return False, "OTP has expired."

        # 2. Check Attempts
        max_attempts = int(os.getenv('OTP_MAX_ATTEMPTS', 3))
        if otp_obj.attempts >= max_attempts:
            otp_obj.delete()
            return False, "Maximum attempts reached. Please request a new OTP."

        # 3. Success Invalidation Strategy
        otp_obj.attempts += 1
        otp_obj.verified = True
        otp_obj.save()
        
        return True, "OTP verified successfully."

    @staticmethod
    def reset_password(identifier, otp_code, new_password):
        """
        Resets the password after successful OTP verification.
        Uses Django's set_password (hashes with PBKDF2/bcrypt).
        """
        try:
            from django.db.models import Q
            user = User.objects.get(Q(username=identifier) | Q(email=identifier))
            otp_obj = PasswordResetOTP.objects.get(user=user, otp=otp_code, verified=True)
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return False, "Invalid request or unverified OTP."

        if otp_obj.expiry_time < timezone.now():
            otp_obj.delete()
            return False, "Session expired. Please start again."

        # Perform Reset
        user.set_password(new_password)
        user.save()

        # Invalidate/Cleanup
        otp_obj.delete()
        
        return True, "Password reset successfully. You can now login with your new password."
