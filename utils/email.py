import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

BREVO_API_KEY = settings.BREVO_API_KEY

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = BREVO_API_KEY

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)

def send_email(to_email, subject, html_content, sender_email="nazirsherzad12345@gmail.com", sender_name="A1 Rugs"):
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email}],
        sender={"name": sender_name, "email": sender_email},
        subject=subject,
        html_content=html_content
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        return response
    except ApiException as e:
        print("Brevo error:", e)
        return None