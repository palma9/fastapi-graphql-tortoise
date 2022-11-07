import requests

GOOGLE_VERIFY_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def google_auth(access_token: str) -> dict:
    """Verify Google access token

    Args:
        access_token (str): Google access token

    Returns:
        dict: Google user data
    """
    headers: dict = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(GOOGLE_VERIFY_URL, headers=headers)

    response.raise_for_status()
    return response.json()
