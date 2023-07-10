# Standard Library
from http import HTTPStatus

# Third Party Library
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from recipes.models import Recipe
from recipes.tests.tests_base import RecipeTestsBaseClass, TagTestsBaseClass
from rest_framework.authtoken.models import Token

User = get_user_model()


class RecipeViewsTests(RecipeTestsBaseClass):
    def test_recipes_get(self):
        self._create_recipe_and_get_url()
        response = self.client.get(self.RECIPES_ALL, headers=self.auth_headers)
        for field in self.PAGINATION_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)

        for field in self.RECIPE_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data.get("results")[0])

    def test_recipe_create(self):
        response = self.client.post(
            self.RECIPES_ALL, data=self.data, headers=self.auth_headers
        )
        for field in self.RECIPE_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)

    def test_recipe_id_get(self):
        url = self._create_recipe_and_get_url()
        response = self.client.get(url, headers=self.auth_headers)

        for field in self.RECIPE_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)

    def test_recipe_patch(self):
        url = self._create_recipe_and_get_url()
        response = self.client.get(url, headers=self.auth_headers)
        check_not_equal = response.data["name"]
        data = self.data.copy()
        data["name"] = "blah"
        response = self.client.patch(
            url,
            data=data,
            headers=self.auth_headers,
            content_type="application/json",
        )
        self.assertEqual(response.data["name"], data["name"])
        self.assertNotEqual(response.data["name"], check_not_equal)

    def test_recipe_delete(self):
        before = Recipe.objects.all().count()
        url = self._create_recipe_and_get_url()
        check_post = Recipe.objects.all().count()
        if before != check_post:
            self.client.delete(url, headers=self.auth_headers)
            after = Recipe.objects.all().count()
            self.assertEqual(before, after)


class TagViewsTests(TagTestsBaseClass):
    def test_tags_get(self):
        response = self.client.get(
            self.ALL_TAGS_URL, headers=self.auth_headers
        )
        for field in self.TAGS_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data[0])

    def test_tag_id_get(self):
        response = self.client.get(self.TAG_ID_URL, headers=self.auth_headers)
        for field in self.TAGS_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)
