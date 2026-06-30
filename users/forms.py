from django.conf import settings
from dj_rest_auth.forms import AllAuthPasswordResetForm
from dj_rest_auth.forms import user_pk_to_url_str


def frontend_url_generator(request, user, temp_key):
    uid = user_pk_to_url_str(user)

    return (
        f"{settings.FRONTEND_URL}"
        f"/reset-password/{uid}/{temp_key}/"
    )


class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        kwargs["url_generator"] = frontend_url_generator
        return super().save(request, **kwargs)