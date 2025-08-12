import os
import requests
from dotenv import load_dotenv

from custom_errors import FavQsConfigError, FavQsAuthError

load_dotenv()


class FavQsCli:
    """Client for FavQs API."""

    BASE_URL = "https://favqs.com/api"

    def __init__(self, api_token: str = None):
        self._api_token = api_token or os.getenv("FAVQS_API_KEY")
        if not self._api_token:
            raise FavQsConfigError()

        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/vnd.favqs.v2+json;"
        })

        self._user_token = None
        self._login = None

    # ----------- Properties -----------

    @property
    def user_token(self) -> str | None:
        return self._user_token

    @property
    def login(self) -> str | None:
        return self._login

    def _headers(self, extra_headers: dict = None) -> dict:
        """Get headers with auth."""
        headers = {
            "Authorization": f'Token token="{self._api_token}"',
            **self._session.headers
        }
        if self._user_token:
            headers["User-Token"] = self._user_token
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def _request(self, method: str, endpoint: str, json: dict = None, extra_headers: dict = None) -> requests.Response:
        """Request to API with auth."""
        url = f"{self.BASE_URL}{endpoint}"
        resp = self._session.request(method, url, json=json, headers=self._headers(extra_headers))
        resp.raise_for_status()
        return resp

    def _require_auth(self) -> None:
        if not self._user_token:
            raise FavQsAuthError("User is not authenticated. Please log in or create a user first.")

    def create_user(self, login: str, email: str, password: str) -> dict:
        """Create user."""
        payload = {"user": {"login": login, "email": email, "password": password}}
        data = self._request("POST", "/users", json=payload).json()

        self._user_token = data.get("User-Token") or data.get("user_token")
        self._login = data.get("login") or login
        return data

    def get_user(self, login: str = None) -> dict:
        """Retrieve user data."""
        self._require_auth()
        return self._request("GET", f"/users/{login or self._login}").json()

    def update_user(self, new_login: str = None, new_email: str = None) -> dict:
        """Update user data."""
        self._require_auth()

        body = {"user": {}}
        if new_login:
            body["user"]["login"] = new_login
        if new_email:
            body["user"]["email"] = new_email

        data = self._request("PUT", f"/users/{self._login}", json=body).json()
        if new_login:
            self._login = new_login
        return data
