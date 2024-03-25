import unittest
import os
from process_csv.main import process_csv, load_configuration

class TestProcessCSVIntegration(unittest.TestCase):
    def setUp(self):
        # Specify the paths to your actual input CSV, configuration JSON, and expected output CSV
        self.input_csv_path = os.path.join('tests','data','test_sample_data.csv') 
        self.config_json_path = os.path.join('tests','data','test_config.json')
        self.expected_output_csv_path = os.path.join('tests','data','test_expected_output.csv')
        
        # Path for the actual output of the test, ensure this does not overwrite important data
        self.test_output_csv_path = os.path.join('tests','data','test_output.csv')

    def test_process_csv_integration(self):
        # Load the configuration
        config = load_configuration(self.config_json_path)

        # Process the CSV
        process_csv(self.input_csv_path, self.test_output_csv_path, config)

        # Verify the output file content matches expected content
        with open(self.test_output_csv_path, 'r') as test_output_file:
            test_output_content = test_output_file.read()
        
        with open(self.expected_output_csv_path, 'r') as expected_output_file:
            expected_output_content = expected_output_file.read()

        self.assertEqual(test_output_content.strip(), expected_output_content.strip())

    def tearDown(self):
        # Optionally, clean up the output file after the test
        os.remove(self.test_output_csv_path)

if __name__ == '__main__':
    unittest.main()
