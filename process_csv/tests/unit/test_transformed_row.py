import unittest
import os
from decimal import Decimal
from process_csv.main import transform_row, load_configuration 



class TestTransformRow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_config_path = os.path.join('tests', 'data', 'test_config.json')
        cls.config = load_configuration(test_config_path)
    
    def test_valid_row_transformation(self):
        row = {
            "Order Number": "1000",
            "Year": "2017",
            "Month": "11",
            "Day": "26",
            "Product Number": "P-96840",
            "Product Name": "Spinach",
            "Count": "972.50"
        }
        expected_transformed_row = {
            "OrderID": 1000,
            "OrderDate": "2017-11-26",
            "ProductId": "P-96840",
            "ProductName": "Spinach",
            "Quantity": Decimal('972.50'),
            "Unit": "kg"
        }
        transformed_row = transform_row(row, self.config['fields'])

        # Instead of comparing the entire dictionaries, compare each expected field individually
        for key, expected_value in expected_transformed_row.items():
            self.assertIn(key, transformed_row, f"{key} is missing in the transformed row")
            self.assertEqual(transformed_row[key], expected_value, f"{key} does not match the expected value")


    def test_invalid_date_transformation(self):
        # Assuming transform_row returns None for invalid transformations
        row = {
            "Order Number": "1004",
            "Year": "2015",
            "Month": "02",
            "Day": "29",  # 2015 is not a leap year
            "Product Number": "P-28951",
            "Product Name": "Kale",
            "Count": "45.50"
        }
        transformed_row = transform_row(row, self.config['fields'])
        self.assertIsNone(transformed_row, "Expected transformation to fail due to invalid date")

if __name__ == '__main__':
    unittest.main()
