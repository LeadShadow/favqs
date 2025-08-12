import pytest
from faker import Faker
from custom_errors import FavQsAuthError

fake = Faker()


class TestFavQsCli:
    @classmethod
    def unique_user_data(cls, client, max_attempts=5):
        for _ in range(max_attempts):
            login, email, password = fake.user_name(), fake.unique.email(), fake.password(length=12)
            resp = client.create_user(login, email, password)
            if resp.get("login") == login:
                return login, email, password
            if "exists" in resp.get("error", "").lower():
                continue
            pytest.fail(f"Unexpected error from API: {resp}")
        pytest.fail("Could not create a unique user after several attempts")

    def test_create_and_get_user(self, client):
        login, email, _ = self.unique_user_data(client)
        assert client.user_token
        user_info = client.get_user()
        assert user_info.get("login") == login
        assert user_info.get("account_details", {}).get("email") == email

    def test_update_user(self, client):
        self.unique_user_data(client)
        new_login, new_email = fake.user_name(), fake.unique.email()
        client.update_user(new_login=new_login, new_email=new_email)
        user_info = client.get_user(login=new_login)
        assert user_info.get("login") == new_login
        assert user_info.get("account_details", {}).get("email") == new_email

    @pytest.mark.parametrize(
        "dup_field",
        ["login", "email"],
        ids=["existing_login", "existing_email"]
    )
    def test_create_user_with_existing_field(self, client, dup_field):
        login, email, password = self.unique_user_data(client)
        kwargs = {"login": fake.user_name(), "email": fake.unique.email()}
        kwargs[dup_field] = login if dup_field == "login" else email
        resp = client.create_user(**kwargs, password=password)
        assert resp.get("error_code") == 31
        assert resp.get("message") == "User session already present."

    @pytest.mark.parametrize(
        "method,args",
        [
            ("get_user", {"login": fake.user_name()}),
            ("update_user", {"new_login": fake.user_name()})
        ],
        ids=["get_user_without_auth", "update_user_without_auth"]
    )
    def test_methods_without_auth(self, client, method, args):
        client._user_token = None
        with pytest.raises(FavQsAuthError):
            getattr(client, method)(**args)
