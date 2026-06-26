import unittest
from securepass.password import generate_number_only, generate_letters_only, password_report

class TestPassword(unittest.TestCase):
    def test_generate_number_only(self):
        length = 10
        result = generate_number_only(length)
        self.assertEqual(len(result), length)
        self.assertTrue(result.isdigit())

    def test_generate_letters_only(self):
        length = 10
        result = generate_letters_only(length)
        self.assertEqual(len(result), length)
        self.assertTrue(result.isalpha())

    def test_password_report(self):
        result = password_report("a1B!")
        self.assertIn("4 characters", result)
        self.assertIn("1 uppercase", result)
        self.assertIn("1 lowercase", result)
        self.assertIn("1 number", result)
        self.assertIn("1 symbol", result)

if __name__ == '__main__':
    unittest.main()
