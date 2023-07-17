# Standard Library
from http import HTTPStatus

# Third Party Library
from django.contrib.auth import get_user_model
from ingredientlist.tests.test_base import IngredientlistTestsBaseClass
from rest_framework.authtoken.models import Token

User = get_user_model()


class TestURLIngredientlist(IngredientlistTestsBaseClass):
    def test_get_ingredients(self):
        response = self.client.get(
            self.GET_INGREDIENTS_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_ingredients_anon(self):
        response = self.client.get(self.GET_INGREDIENTS_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_ingredient(self):
        url = self.GET_INGREDIENT_URL(ingredient_id=1)
        response = self.client.get(url, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_ingredient_anon(self):
        url = self.GET_INGREDIENT_URL(ingredient_id=1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_ingredient_invalid(self):
        url = self.GET_INGREDIENT_URL(ingredient_id=100)
        response = self.client.get(url, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_download_order_list(self):
        response = self.client.get(
            self.GET_ORDER_LIST_URL, headers=self.auth_headers
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_download_order_list_anon(self):
        response = self.client.get(self.GET_ORDER_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_add_recipe_to_order_list(self):
        url = self.ADD_REMOVE_RECIPE_ORDER_LIST_URL(recipe_id=1)
        response = self.client.post(url, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_add_recipe_to_order_list_error(self):
        url = self.ADD_REMOVE_RECIPE_ORDER_LIST_URL(recipe_id=1)
        self.client.post(url, headers=self.auth_headers)
        response = self.client.post(url, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_add_recipe_to_order_list_anon(self):
        url = self.ADD_REMOVE_RECIPE_ORDER_LIST_URL(recipe_id=1)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_remove_recipe_from_order_list(self):
        url = self.ADD_REMOVE_RECIPE_ORDER_LIST_URL(recipe_id=1)
        response = self.client.delete(url, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_remove_recipe_from_order_list_error(self):
        url = self.ADD_REMOVE_RECIPE_ORDER_LIST_URL(recipe_id=1)
        self.client.delete(url, headers=self.auth_headers)
        response = self.client.delete(url, headers=self.auth_headers)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_remove_recipe_from_order_list_anon(self):
        url = self.ADD_REMOVE_RECIPE_ORDER_LIST_URL(recipe_id=1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
