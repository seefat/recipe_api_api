from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from test_app.models import Recipe, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

User = get_user_model()

RECIPES_URL = reverse('recipe:recipe-list')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


def detail_url(recipe_id):
    return reverse('recipe:recipe_detail', args=[recipe_id])

def create_recipe(user,**params):

    defaults = {
        'title': 'Simple RecipeAPI title',
        'time_minutes':22,
        'price': Decimal('10.4'),
        'description': 'Simple Recipe Description',
        'link':'http://example.com/recipe.pdf'
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user,**defaults)
    return recipe

class PublicRecipeAPITests(TestCase):
    def SetUP(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITests(TestCase):
    def setUP(self):
        self.client = APIClient()

        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        create_recipe(user=self.user)
        #create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

#     def test_recipe_list_limited_to_user(self):
#         other_user = create_user(
#             email='other@example.com',
#             password='testother123',
#         )

#         create_recipe(user = other_user)
#         create_recipe(user = self.user)

#         res = self.client.get(RECIPES_URL)
#         recipes = Recipe.objects.filter(user = self.user)
#         serializer = RecipeSerializer(recipes, many=True)
#         self.assertEqual(res.status_code,status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)

#     def test_get_recipe_detail(self):
#         recipe = create_recipe(user = self.user)
#         url = detail_url(recipe.id)
#         res = self.client.get(url)


#         serializer = RecipeDetailSerializer(recipe)
#         self.asserEqual(res.data, serializer.data)

#     def test_create_recipe(self):
#         payload = {
#             'title':'Simple Title',
#             'time_minutes':20,
#             'price':Decimal('12.5'),
#         }

#         res = self.client.post(RECIPES_URL,payload)

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)

#         recipe = Recipe.objects.get(id=res.data['id'])
#         for k,v in payload.items():
#             self.assertEqual(getattr(recipe,k),v)
#         self.assertEqual(self.user,recipe.user)

#     def test_create_recipe_with_new_tags(self):
#         payload = {
#             'title':'Thai Prawn',
#             'time_minutes':25,
#             'price':Decimal('5.5'),
#             'tags':[{'name':'Thai','name':'dinner'}]
#         }
#         res = self.client.post(RECIPES_URL, payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipes = Recipe.objects.filter(user=self.user)

#         self.assertEqual(recipes.count(),1)
#         recipe = recipes[0]
#         self.assertEqual(recipe.tags.count(),2)

#         for tag in payload['tags']:
#             exists = recipe.tags.filter(
#                 name = tag['name'],
#                 user = self.user,
#             ).exists()
#             self.assertTrue(exists)

#     def test_create_recipe_with_existing_tags(self):
#         tag_indian = Tag.objects.create(user=self.user, name='Indian')
#         payload = {
#             'title':'Pongal',
#             'time_minutes':55,
#             'price':Decimal('5.5'),
#             'tags':[{'name':'Indian'},{'name':'Breakfast'}]
#         }
#         res = self.client.post(RECIPES_URL, payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         recipes = Recipe.objects.filter(user=self.user)
#         print('++++++++++++++++',res.data)
#         self.assertEqual(recipes.count(),1)
#         recipe = recipes[0]
#         print(recipe)
#         self.assertEqual(recipe.tags.count(),2)
#         self.assertIn(tag_indian, recipe.tag.all() )
#         for tag in payload['tags']:
#             exists = recipe.tags.filter(
#                 name = tag['name'],
#                 user = self.user,
#             ).exists()
#             self.assertTrue(exists)