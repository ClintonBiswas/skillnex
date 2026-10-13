from django.conf import settings

from ..models import SMSSettings
from .sms import send_sms


def get_sms_settings():

    return SMSSettings.objects.first()


def send_student_enrollment_sms(enrollment):

    message = (
        f"Skillnex: Your enrollment request for "
        f"{enrollment.course.name} has been received. "
        f"We will contact you shortly."
    )

    return send_sms(
        enrollment.phone,
        message
    )


def send_admin_enrollment_sms(enrollment):

    sms_settings = get_sms_settings()

    if not sms_settings:
        return {
            "success": False,
            "message": "SMS settings not configured."
        }

    if not sms_settings.is_active:
        return {
            "success": False,
            "message": "SMS notifications are disabled."
        }

    message = (
        f"Skillnex: New enrollment received. "
        f"{enrollment.name} applied for "
        f"{enrollment.course.name}. "
        f"Phone: {enrollment.phone}"
    )

    return send_sms(
        sms_settings.admin_phone,
        message
    )


STATUS_MESSAGES = {
    "pending": (
        "Your enrollment request is currently pending. "
        "Our team will contact you shortly."
    ),

    "contacted": (
        "Our Skillnex team has contacted you regarding "
        "your course enrollment."
    ),

    "payment_pending": (
        "Your Skillnex enrollment is awaiting payment. "
        "Please follow the payment instructions provided by our team."
    ),

    "confirmed": (
        "Congratulations! Your Skillnex course enrollment "
        "has been confirmed."
    ),

    "cancelled": (
        "Your Skillnex course enrollment has been cancelled. "
        "Please contact our team if you need assistance."
    ),
}


def send_enrollment_status_sms(enrollment):

    message = STATUS_MESSAGES.get(
        enrollment.status
    )

    if not message:
        return {
            "success": False,
            "message": "No SMS message configured for this status."
        }

    message = (
        f"Skillnex: {message} "
        f"Course: {enrollment.course.name}"
    )

    return send_sms(
        enrollment.phone,
        message
    )
