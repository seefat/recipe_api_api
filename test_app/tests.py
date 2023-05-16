from django.test import TestCase, SimpleTestCase
from . import calc

# Create your tests here.

class CalcTest(SimpleTestCase):
    def test_add_numbers(self):
        res = calc.add(5,6)

        self.assertEqual(res,11)

    def test_subtract_numbers(self):
        res = calc.subtract(10,15)

        self.assertEqual(res, -5)
