# Standard Library
from http import HTTPStatus

# Third Party Library
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from users.tests.tests_base import (
    SubscriptionTestsBaseClass,
    UserTestsBaseClass,
)

User = get_user_model()


class UserURLTests(UserTestsBaseClass):
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


class SubscriptionURLTests(SubscriptionTestsBaseClass):
    def test_anon(self):
        urls = [
            self.UN_SUB_SCRIBE_URL,
            self.MY_SUBSCRIPIONS_URL,
            self.UN_SUB_SCRIBE_URL_INVALID_URL,
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_my_subscriptions(self):
        response = self.authorized_client.get(
            self.MY_SUBSCRIPIONS_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_subscribe_ok(self):
        response = self.authorized_client.post(
            self.UN_SUB_SCRIBE_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_unsubscribe_ok(self):
        self.authorized_client.post(self.UN_SUB_SCRIBE_URL, headers=self.auth_headers)
        response = self.authorized_client.delete(
            self.UN_SUB_SCRIBE_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_un_subscribe_error(self):
        for method, url in self.UN_SUBSCRIBE_URLS.items():
            with self.subTest(url=url):
                if method == "post":
                    self.authorized_client.post(url, headers=self.auth_headers)
                    response = self.authorized_client.post(
                        url, headers=self.auth_headers
                    )
                elif method == "delete":
                    self.authorized_client.delete(url, headers=self.auth_headers)
                    response = self.authorized_client.delete(
                        url, headers=self.auth_headers
                    )
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_un_subscribe_invalid_user(self):
        for method, url in self.UN_SUBSCRIBE_INVALID_URLS.items():
            with self.subTest(url=url):
                if method == "post":
                    response = self.authorized_client.post(
                        url, headers=self.auth_headers
                    )
                elif method == "delete":
                    response = self.authorized_client.delete(
                        url, headers=self.auth_headers
                    )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_cant_subscribe_to_yourself(self):
        user = User.objects.create(username="selfsubscriber")
        token, _ = Token.objects.get_or_create(user=user)
        auth_headers = {"AUTHORIZATION": f"Token {token.key}"}

        url = self.UN_SUB_SCRIBE_URL.replace(str(self.SUBSCRIBE_USER_ID), str(user.id))
        response = self.authorized_client.post(url, headers=auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
