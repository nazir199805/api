from django.core.mail.backends.base import BaseEmailBackend
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings


class BrevoEmailBackend(BaseEmailBackend):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = settings.BREVO_API_KEY

        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        sent_count = 0

        for message in email_messages:
            try:
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                    to=[{"email": email} for email in message.to],
                    subject=message.subject,
                    html_content=message.body,
                    sender={
                        "name": getattr(settings, "EMAIL_SENDER_NAME", "A1 Rugs"),
                        "email": settings.DEFAULT_FROM_EMAIL
                    },
                )

                self.api_instance.send_transac_email(send_smtp_email)
                sent_count += 1

            except ApiException as e:
                print("Brevo Email Error:", e)

        return sent_count