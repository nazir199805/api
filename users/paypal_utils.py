import requests
from django.conf import settings

def get_paypal_access_token():
    url = f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token"
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}

    res = requests.post(url, headers=headers, data=data, auth=auth)
    res.raise_for_status()
    return res.json()["access_token"]
