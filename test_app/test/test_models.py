from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from test_app import models

def create_user(email='user@gmail.com',password='testpass123'):
    return get_user_model().objects.create(email=email,password=password)


class ModelTest(TestCase):

    def test_create_user_with_email_successfully(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test123@xyz.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            'test@example.com',
            'test123',
        )
        recipe = models.Recipe.objects.create(
            user = user,
            title = 'simple title name',
            time_minutes=5,
            price = Decimal('5.5'),
            description = 'Simple Recipe description',
        )

        self.assertEqual(str(recipe),recipe.title)

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user,name='tag1')

        self.assertEqual(str(tag),tag.name)

    def test_create_ingredient(self):
        user = create_user()

        ingredient = models.Ingredient.objects.create(user=user,name='ingredient_1')

        self.assertEqual(str(ingredient),ingredient.name)

    @patch('test_app.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')
        print('files----------', file_path)
        self.assertEqual(file_path, f'uploads\\recipe\\{uuid}.jpg')