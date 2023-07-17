from ingredientlist.tests.test_base import IngredientlistTestsBaseClass


class IngredientlistViewsTests(IngredientlistTestsBaseClass):
    def test_get_ingredients(self)
        response = self.client.get(self.GET_INGREDIENTS_URL, headers=self.auth_headers)
        for field in self.INGREDIENT_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data[0])

    def test_get_ingredient(self):
        url = self.GET_INGREDIENT_URL(ingredient_id=1)
        response = self.client.get(url, headers=self.auth_headers)
        for field in self.INGREDIENT_FIELDS:
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        
    def TODO_test_get_order_list_download(self):
        pass

    def test_add_recipe_to_order_list(self):
        url = self.ADD_REMOVE_RECIPE_ORDER_LIST_URL(recipe_id=1)
        order_list_before = User.objects.get()
        response = self.client.post(url, headers=self.auth_headers)
