
import unittest
import os
from process_csv.main import load_configuration

class TestLoadConfiguration(unittest.TestCase):
    def test_load_configuration(self):
        # Define the path to your test configuration file
        test_config_path = os.path.join('tests', 'data', 'test_config.json')
        
        # Load the configuration using your function
        config = load_configuration(test_config_path)
        
        # Assert that the returned object is a dictionary
        self.assertIsInstance(config, dict)
        
        # Assert specific values and structures based on your test_config.json content
        self.assertIn('fields', config)
        self.assertIsInstance(config['fields'], list)

if __name__ == '__main__':
    unittest.main()
