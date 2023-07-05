# Standard Library
from http import HTTPStatus

# Third Party Library
from users.tests.tests_base import UserTestsBaseClass


class UserURLTests(UserTestsBaseClass):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_all_users_url(self):
        response = self.authorized_client.get(
            self.ALL_USER_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_sign_up_url_anon(self):
        data = {
            "email": "example@aaa.ert",
            "username": "username_example",
            "first_name": "name_example",
            "last_name": "ln_example",
            "password": "Kalina3333!",
        }
        response = self.guest_client.post(self.ALL_USER_URL, data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        data.pop("email")
        response = self.guest_client.post(self.ALL_USER_URL, data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_id_user_url_anon(self):
        response = self.guest_client.get(self.ID_USER_URL)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_id_user_url(self):
        response = self.authorized_client.get(
            self.ID_USER_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.authorized_client.get(
            self.INVALID_ID_USER_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_current_user_url_anon(self):
        response = self.guest_client.get(self.CURRENT_USER_URL)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_current_user_url(self):
        response = self.authorized_client.get(
            self.CURRENT_USER_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_change_password_url_anon(self):
        response = self.guest_client.post(
            self.CHANGE_PASSWORD_URL, self.CHANGE_PASSWORD_DATA
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_change_password_url(self):
        data = self.CHANGE_PASSWORD_DATA.copy()
        data.pop("new_password")
        response = self.authorized_client.post(
            self.CHANGE_PASSWORD_URL,
            data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        response = self.authorized_client.post(
            self.CHANGE_PASSWORD_URL,
            self.CHANGE_PASSWORD_DATA,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_login_anon(self):
        data = {
            "email": self.FORCE_USER_EMAIL,
            "password": self.FORCE_CURRENT_PASSWORD,
        }
        response = self.guest_client.post(self.LOGIN_URL, data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_logout_anon(self):
        response = self.guest_client.post(self.LOGOUT_URL)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_logout(self):
        response = self.authorized_client.post(
            self.LOGOUT_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
