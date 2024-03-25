import unittest
import os
from process_csv.main import load_configuration, pre_validate_row


class TestPreValidation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_config_path = os.path.join('tests', 'data', 'test_config.json')
        cls.config = load_configuration(test_config_path)

    def test_valid_row(self):
        valid_row = {
            'Order Number': '1000', 
            'Year': '2017', 
            'Month': '11', 
            'Day': '26', 
            'Product Number': 'P-96840', 
            'Product Name': 'Spinach', 
            'Count': '972.50'
        }
        self.assertTrue(pre_validate_row(valid_row, self.config['fields']))

    def test_invalid_row(self):
        invalid_row = {
            'Order Number': 'XYZ1002', 
            'Year': 'abcd', 
            'Month': '13', 
            'Day': '32', 
            'Product Number': 'P28951', 
            'Product Name': 'Egg Noodles 1', 
            'Count': '12.50'
        }
        self.assertFalse(pre_validate_row(invalid_row, self.config['fields']))

if __name__ == '__main__':
    unittest.main()
