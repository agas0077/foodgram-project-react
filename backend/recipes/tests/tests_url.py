# Standard Library
from http import HTTPStatus

# Third Party Library
from django.contrib.auth import get_user_model
from recipes.tests.tests_base import RecipeTestsBaseClass
from rest_framework.authtoken.models import Token

User = get_user_model()


class RecipeURLTests(RecipeTestsBaseClass):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.data = {
            # "ingredients": [{"id": 1123, "amount": 10}],
            "tags": [1, 2],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1,
        }

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
        response = self.client.get(
            self.RECIPES_DETAIL_ID, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipe_patch(self):
        data = self.data.copy()
        data["name"] = "new name"
        response = self.client.patch(
            self.RECIPES_DETAIL_ID, data=data, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipe_patch_wrong_user(self):
        new_user = User.objects.create_user(username="new_user")
        token, _ = Token.objects.get_or_create(user=new_user)
        auth_headers = {"AUTHORIZATION": f"Token {token.key}"}

        response = self.client.patch(
            self.RECIPES_DETAIL_ID, data=self.data, headers=auth_headers
        )

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_recipe_patch_anon(self):
        response = self.client.patch(self.RECIPES_DETAIL_ID, data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_recipe_patch_id_invalid(self):
        response = self.client.patch(
            self.RECIPES_DETAIL_ID_INVALID,
            data=self.data,
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_recipe_delete_anon(self):
        response = self.client.delete(self.RECIPES_DETAIL_ID)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_recipe_delete_wrong_user(self):
        new_user = User.objects.create_user(username="new_user")
        token, _ = Token.objects.get_or_create(user=new_user)
        auth_headers = {"AUTHORIZATION": f"Token {token.key}"}

        response = self.client.delete(
            self.RECIPES_DETAIL_ID, headers=auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

    def test_recipe_delete_id_invalid(self):
        response = self.client.delete(
            self.RECIPES_DETAIL_ID_INVALID, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_recipe_delete(self):
        response = self.client.delete(
            self.RECIPES_DETAIL_ID, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
