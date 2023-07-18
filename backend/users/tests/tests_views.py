# Third Party Library
from django.contrib.auth import get_user_model
from users.tests.tests_url import (
    SubscriptionTestsBaseClass,
    UserTestsBaseClass,
)

User = get_user_model()


class UserViewsTests(UserTestsBaseClass):
    def test_all_users_view(self):
        response = self.client.get(self.ALL_USER_URL, headers=self.auth_headers)

        for field in self.PAGINATION_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)

        for field in self.USER_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data["results"][0])

    def test_user_sign_up_anon(self):
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "Qwerty1231231",
        }
        user_count_before = User.objects.all().count()

        response = self.guest_client.post(self.ALL_USER_URL, data)
        user_count_before += 1

        user_count_after = User.objects.all().count()

        self.assertEqual(user_count_before, user_count_after)

        for field in self.SIGN_UP_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)

    def test_user_id_view(self):
        response = self.client.get(self.ID_USER_URL, headers=self.auth_headers)
        for field in self.USER_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)

    def test_user_me_view(self):
        response = self.client.get(self.CURRENT_USER_URL, headers=self.auth_headers)

        for field in self.USER_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)
                if field == "username":
                    self.assertEqual(
                        response.data.get("username"), self.FORCE_USER_NAME
                    )

    def test_user_change_password_and_auth_view(self):
        self.client.post(
            self.CHANGE_PASSWORD_URL,
            self.CHANGE_PASSWORD_DATA,
            headers=self.auth_headers,
        )

        data = {
            "password": self.FORCE_NEW_PASSWORD,
            "email": self.FORCE_USER_EMAIL,
        }
        response = self.guest_client.post(self.LOGIN_URL, data)
        self.assertIn("auth_token", response.data)


class SubscriptionViewsTests(SubscriptionTestsBaseClass):
    def test_my_subscriptions(self):
        response = self.client.get(self.MY_SUBSCRIPIONS_URL, headers=self.auth_headers)
        for field in self.PAGINATION_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)

        for field in self.SUBSCRIPION_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data["results"][0])

    def test_subscribe(self):
        subscripion_count_before = User.objects.get(
            pk=self.force_user.id
        ).subscriptions.count()
        response = self.client.post(self.UN_SUB_SCRIBE_URL, headers=self.auth_headers)
        subscripion_count_after = User.objects.get(
            pk=self.force_user.id
        ).subscriptions.count()
        for field in self.SUBSCRIPION_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)

        self.assertEqual(subscripion_count_before + 1, subscripion_count_after)

    def test_unsubscribe(self):
        subscripion_count_before = User.objects.get(
            pk=self.force_user.id
        ).subscriptions.count()
        self.client.post(self.UN_SUB_SCRIBE_URL, headers=self.auth_headers)
        subscripion_count_after = User.objects.get(
            pk=self.force_user.id
        ).subscriptions.count()
        self.assertEqual(subscripion_count_before - 1, subscripion_count_after)
