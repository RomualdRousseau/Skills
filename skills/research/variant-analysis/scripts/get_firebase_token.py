import os
import json
import requests
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# Configuration from .env
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
API_KEY = os.getenv("FIREBASE_API_KEY")
CLIENT_SECRET_PATH = os.getenv("GOOGLE_CLIENT_SECRET_PATH")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


def exchange_google_for_firebase(google_id_token):
    """Exchanges a Google ID Token for a Firebase ID Token."""
    firebase_redirect_uri = f"https://{PROJECT_ID}.firebaseapp.com/__/auth/handler"
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={API_KEY}"
    payload = {
        "postBody": f"id_token={google_id_token}&providerId=google.com",
        "requestUri": firebase_redirect_uri,
        "returnIdpCredential": True,
        "returnSecureToken": True,
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        return None
    return response.json().get("idToken")


def get_token():
    # 1. Try to load existing credentials (includes refresh token)
    creds = None
    cache_dir = os.path.expanduser("~/.cache/gemini-variant-analysis")
    os.makedirs(cache_dir, exist_ok=True)
    token_cache_path = os.path.join(cache_dir, "google_token_cache.json")

    if os.path.exists(token_cache_path):
        creds = Credentials.from_authorized_user_file(token_cache_path, SCOPES)

    # 2. If no valid creds or expired or missing id_token, refresh or login
    if not creds or not creds.valid or not getattr(creds, "id_token", None):
        if creds and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None  # Force re-login if refresh fails

        if not creds or not getattr(creds, "id_token", None):
            # Use path from .env or fallback to searching
            client_secret_file = None
            if CLIENT_SECRET_PATH:
                # Check both current and parent dir
                if os.path.exists(CLIENT_SECRET_PATH):
                    client_secret_file = CLIENT_SECRET_PATH
            if not client_secret_file:
                print(
                    "Error: Client secret file not found. Check GOOGLE_CLIENT_SECRET_PATH in .env",
                    file=sys.stderr,
                )
                return None

            # Determine port based on client type
            with open(client_secret_file, "r") as f:
                config = json.load(f)
                is_web = "web" in config

            # Use 8081 for web (must be registered in Console), 0 for desktop (auto)
            port = 8081 if is_web else 0

            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            creds = flow.run_local_server(port=port, prompt="consent")

        # Save the credentials for next time
        if creds:
            with open(token_cache_path, "w") as f:
                f.write(creds.to_json())

    # 3. Exchange for Firebase Token
    if not creds or not creds.id_token:  # type: ignore
        print("Error: Failed to obtain Google ID token", file=sys.stderr)
        return None

    firebase_token = exchange_google_for_firebase(creds.id_token)  # type: ignore

    if firebase_token:
        return firebase_token
    return None


if __name__ == "__main__":
    try:
        token = get_token()
        if token:
            # Output ONLY the token so the skill can capture it
            print(token)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        sys.exit(1)
