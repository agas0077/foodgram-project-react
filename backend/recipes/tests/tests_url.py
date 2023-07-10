# Standard Library
from http import HTTPStatus

# Third Party Library
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from recipes.models import Recipe
from recipes.tests.tests_base import RecipeTestsBaseClass, TagTestsBaseClass
from rest_framework.authtoken.models import Token

User = get_user_model()


class RecipeURLTests(RecipeTestsBaseClass):
    def test_recipes_get(self):
        response = self.client.get(self.RECIPES_ALL, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipes_post(self):
        response = self.client.post(
            self.RECIPES_ALL, data=self.data, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_recipes_post_error_data(self):
        data = self.data.copy()
        del data["name"]
        response = self.client.post(
            self.RECIPES_ALL, data=data, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_recipes_post_anon(self):
        response = self.client.post(self.RECIPES_ALL, data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_recipe_get(self):
        url = self._create_recipe_and_get_url()
        response = self.client.get(url, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipe_patch(self):
        data = self.data.copy()
        data["name"] = "new name"
        url = self._create_recipe_and_get_url()
        response = self.client.patch(
            url,
            data=data,
            headers=self.auth_headers,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipe_patch_wrong_user(self):
        new_user = User.objects.create_user(username="new_user")
        token, _ = Token.objects.get_or_create(user=new_user)
        auth_headers = {"AUTHORIZATION": f"Token {token.key}"}
        url = self._create_recipe_and_get_url()
        response = self.client.patch(
            url,
            data=self.data,
            headers=auth_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_recipe_patch_anon(self):
        response = self.client.patch(
            self.RECIPES_DETAIL_ID,
            data=self.data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_recipe_patch_id_invalid(self):
        response = self.client.patch(
            self.RECIPES_DETAIL_ID_INVALID,
            data=self.data,
            headers=self.auth_headers,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_recipe_delete_anon(self):
        response = self.client.delete(self.RECIPES_DETAIL_ID)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_recipe_delete_wrong_user(self):
        new_user = User.objects.create_user(username="new_user")
        token, _ = Token.objects.get_or_create(user=new_user)
        auth_headers = {"AUTHORIZATION": f"Token {token.key}"}
        url = self._create_recipe_and_get_url()
        response = self.client.delete(url, headers=auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_recipe_delete_id_invalid(self):
        response = self.client.delete(
            self.RECIPES_DETAIL_ID_INVALID, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_recipe_delete(self):
        url = self._create_recipe_and_get_url()
        response = self.client.delete(url, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)


class TagURLTests(TagTestsBaseClass):
    def test_tags_get(self):
        response = self.client.get(
            self.ALL_TAGS_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tag_id_get(self):
        response = self.client.get(self.TAG_ID_URL, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tags_get_anon(self):
        response = self.client.get(self.ALL_TAGS_URL)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_tag_id_get_anon(self):
        response = self.client.get(self.TAG_ID_URL)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_tag_id_invalid_get(self):
        response = self.client.get(
            self.TAG_ID_URL_INVALID, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
