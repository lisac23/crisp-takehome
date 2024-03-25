import unittest
import os
from decimal import Decimal
from process_csv.main import load_configuration, post_validate_row

class TestPostValidateRow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_config_path = os.path.join('tests', 'data', 'test_config.json')
        cls.config = load_configuration(test_config_path)

    def test_post_validate_row_success(self):
        # Mock a transformed row that adheres to the post-validation rules
        transformed_row = {
            "OrderID": 1234,  # Integers only, should pass
            "OrderDate": "2021-03-15",  # Correct date format, should pass
            "ProductId": "P-00123",  # Starts with 'P-', should pass
            "ProductName": "Widget",  # Alphabetical, should pass
            "Quantity": Decimal("100.5"),  # Decimal format, should pass
            "Unit": "kg"  # Fixed value, no validation needed but should pass
        }
        self.assertTrue(post_validate_row(transformed_row, self.config))

    def test_post_validate_row_failure_due_to_date_format(self):
        # Mock a transformed row that fails due to incorrect date format
        transformed_row = {
            "OrderID": 1234,  # Correct integer format
            "OrderDate": "15-03-2021",  # Incorrect date format, should fail
            "ProductId": "P-00123",  # Correct product ID format
            "ProductName": "Widget",  # Correct product name format
            "Quantity": Decimal("100.5"),  # Correct decimal format
            "Unit": "kg"  # Correct fixed value
        }
        result = post_validate_row(transformed_row, self.config['fields'])
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
