import requests

from django.conf import settings
from django.utils.html import escape


def send_contact_inquiry_email(inquiry):
    """
    Send a new contact inquiry notification
    to the Skillnex team using Mailgun API.
    """

    subject = (
        f"New {inquiry.get_inquiry_type_display()} Inquiry "
        f"from {inquiry.name}"
    )

    inquiry_type = inquiry.get_inquiry_type_display()

    service_name = (
        inquiry.service.name
        if inquiry.service
        else "Not selected"
    )

    course_name = (
        inquiry.course.name
        if inquiry.course
        else "Not selected"
    )

    training_purpose = (
        inquiry.get_training_purpose_display()
        if inquiry.training_purpose
        else "Not specified"
    )

    contact_method = (
        inquiry.get_preferred_contact_method_display()
        if inquiry.preferred_contact_method
        else "Not specified"
    )

    submitted_at = inquiry.created_at.strftime(
        "%d %B %Y, %I:%M %p"
    )

    # -----------------------------------------
    # Plain text email
    # -----------------------------------------

    text_content = f"""
    New contact inquiry received from Skillnex website.

    Name:
    {inquiry.name}

    Email:
    {inquiry.email}

    Phone / WhatsApp:
    {inquiry.phone}

    Inquiry Type:
    {inquiry_type}

    Service:
    {service_name}

    Course:
    {course_name}

    Training Purpose:
    {training_purpose}

    Preferred Contact Method:
    {contact_method}

    Message:
    {inquiry.message}

    Submitted:
    {submitted_at}
    """

    # -----------------------------------------
    # HTML email
    # -----------------------------------------

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>New Contact Inquiry</title>
    </head>

    <body style="
        margin: 0;
        padding: 30px;
        background: #f4f7ff;
        font-family: Arial, Helvetica, sans-serif;
        color: #1f2937;
    ">

        <div style="
            max-width: 650px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        ">

            <!-- Header -->

            <div style="
                padding: 24px 28px;
                background: #fb8900;
                color: #ffffff;
            ">

                <h2 style="
                    margin: 0;
                    font-size: 24px;
                ">
                    New Contact Inquiry
                </h2>

                <p style="
                    margin: 8px 0 0;
                    opacity: 0.9;
                    font-size: 14px;
                ">
                    Skillnex IT Academy
                </p>

            </div>


            <!-- Content -->

            <div style="padding: 28px;">

                <h3 style="
                    margin-top: 0;
                    color: #111827;
                ">
                    Contact Information
                </h3>


                <table
                    width="100%"
                    cellpadding="8"
                    cellspacing="0"
                    style="
                        border-collapse: collapse;
                        font-size: 14px;
                    "
                >

                    <tr>
                        <td>
                            <strong>Name</strong>
                        </td>
                        <td>
                            {escape(inquiry.name)}
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <strong>Email</strong>
                        </td>
                        <td>
                            {escape(inquiry.email)}
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <strong>Phone</strong>
                        </td>
                        <td>
                            {escape(inquiry.phone)}
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <strong>Inquiry</strong>
                        </td>
                        <td>
                            {escape(inquiry_type)}
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <strong>Service</strong>
                        </td>
                        <td>
                            {escape(service_name)}
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <strong>Course</strong>
                        </td>
                        <td>
                            {escape(course_name)}
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <strong>Training Purpose</strong>
                        </td>
                        <td>
                            {escape(training_purpose)}
                        </td>
                    </tr>

                    <tr>
                        <td>
                            <strong>Preferred Contact</strong>
                        </td>
                        <td>
                            {escape(contact_method)}
                        </td>
                    </tr>

                </table>


                <hr style="
                    margin: 24px 0;
                    border: 0;
                    border-top: 1px solid #e5e7eb;
                ">


                <h3 style="
                    color: #111827;
                ">
                    Message
                </h3>


                <div style="
                    padding: 16px;
                    background: #f8fafc;
                    border-radius: 8px;
                    line-height: 1.7;
                    white-space: pre-line;
                ">
                    {escape(inquiry.message)}
                </div>


                <p style="
                    margin-top: 24px;
                    color: #6b7280;
                    font-size: 13px;
                ">
                    Submitted: {escape(submitted_at)}
                </p>

            </div>

        </div>

    </body>
    </html>
    """

    # -----------------------------------------
    # Send through Mailgun API
    # -----------------------------------------

    mailgun_url = (
        f"https://api.mailgun.net/v3/"
        f"{settings.MAILGUN_DOMAIN}/messages"
    )

    response = requests.post(
        mailgun_url,
        auth=(
            "api",
            settings.MAILGUN_API_KEY,
        ),
        data={
            "from": settings.MAILGUN_FROM_EMAIL,
            "to": settings.CONTACT_NOTIFICATION_EMAIL,
            "subject": subject,
            "text": text_content,
            "html": html_content,
            "h:Reply-To": inquiry.email,
        },
        timeout=15,
    )

    print("MAILGUN STATUS:", response.status_code)
    print("MAILGUN RESPONSE:", response.text)

    response.raise_for_status()

    return response.json()