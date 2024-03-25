import csv
import logging
import re
import json
import os
import sys
import shutil
from decimal import Decimal
from datetime import datetime

# Handle files from previous runs

def archive_file(file_path):
    """ Archives the file by renaming it with a timestamp. """
    if os.path.exists(file_path):
        base, extension = os.path.splitext(file_path)
        new_name = f"{base}_{datetime.now():%Y%m%d%H%M%S}{extension}"
        shutil.move(file_path, new_name)

# Archive the log and output files when the script initializes
archive_file(os.path.join('logs','err.log'))
archive_file(os.path.join('output', 'transformed_data.csv'))

# Handle configuration file errors
def handle_configuration_error(e):
    logging.error(e)
    print(e)
    sys.exit(1)

# Setup logging
log_file_path = os.path.join('logs','err.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config_path = os.path.join('config','config.json')

def load_configuration(config_path):
    # Check if the config file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"The configuration file does not exist: {config_path}")
    
    # Try to open and load the configuration file
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except json.JSONDecodeError as e:
        raise ValueError(f"Configuration file contains invalid JSON: {e}")
    except Exception as e:
        raise IOError(f"An error occurred while reading the configuration file: {e}")

try:
    config = load_configuration(config_path)
except (FileNotFoundError, ValueError, IOError) as e:
    handle_configuration_error(e)

#Pre-compiling the patterns increases performance 
compiled_patterns = {field['name']: re.compile(field['pre_validation']) for field in config['fields'] if 'pre_validation' in field}

def validate_field(value, compiled_pattern):
    """Use pre-compiled regex patterns for validation."""
    return compiled_pattern.match(value) if value else False

def pre_validate_row(row, fields_config):
    """Perform pre-validation for each field in the row based on the config."""
    for field_config in fields_config:
        if 'name' in field_config and 'pre_validation' in field_config:
            field_name = field_config['name']
            # Use the compiled regex pattern from the compiled_patterns dictionary
            compiled_pattern = compiled_patterns[field_name]
            field_value = row.get(field_name, '')
            if not validate_field(field_value, compiled_pattern):
                # Include "Pre-validation" in the log message
                logging.info(f"Row failed pre-validation for {field_name}: {row}")
                return False  # Indicates validation failure
    return True  # Indicates all validations passed

def transform_row(row, fields_config):
    """Apply transformations based on the config, with integrated date validation."""
    transformed_row = {}
    for field_config in fields_config:
        if 'transform' in field_config:
            transform = field_config['transform']
            # Handle different transformation types
            if transform['type'] == 'int':
                transformed_row[transform['new_name']] = int(row[field_config['name']])
            elif transform['type'] == 'str':
                transformed_row[transform['new_name']] = str(row[field_config['name']])
            elif transform['type'] == 'title':
                transformed_row[transform['new_name']] = row[field_config['name']].title()
            elif transform['type'] == 'Decimal':
                transformed_row[transform['new_name']] = Decimal(row[field_config['name']])
            elif transform['type'] == 'fixed':
                transformed_row[transform['new_name']] = transform['value']
            elif transform['type'] == 'date':
                date_str = '-'.join([row[f] for f in transform['fields']])
                try:
                    valid_date = datetime.strptime(date_str, transform['format'])
                    transformed_row[transform['new_name']] = valid_date.strftime(transform['format'])
                except ValueError as e:
                    # Log the error and skip the row by returning None
                    logging.info(f"Invalid date encountered for {transform['fields']}: {date_str}. Error: {e}")
                    return None
        else:
            # Carry over fields that do not require transformation
            if 'name' in field_config:
                transformed_row[field_config['name']] = row[field_config['name']]
    return transformed_row

def post_validate_row(transformed_row, fields_config):
    """Perform post-validation for the transformed row."""
    for field_config in fields_config:
        if 'transform' in field_config and 'post_validation' in field_config:
            new_name = field_config['transform']['new_name']
            validation_pattern = field_config['post_validation']
            if new_name not in transformed_row or not re.match(validation_pattern, transformed_row[new_name]):
                logging.info(f"Row failed post-validation for {new_name}: {transformed_row}")
                return False
    return True

# Open the CSV file and validate, transform, and again validate each row
def process_csv(input_file_path, output_file_path, config):
    with open(input_file_path, mode='r', newline='', encoding='utf-8') as csvfile, \
         open(output_file_path, mode='w', newline='', encoding='utf-8') as outputfile:
        reader = csv.DictReader(csvfile)
        fieldnames = [trans['transform']['new_name'] for trans in config['fields'] if 'transform' in trans]
        writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            if not pre_validate_row(row, config['fields']):
                continue  # Skip this row if it fails pre-validation
            
            transformed_row = transform_row(row, config['fields'])
            if transformed_row is None:
                continue  # Skip this row if transformation failed (e.g., due to invalid date)

            # Filter transformed_row to only include keys in writer.fieldnames
            filtered_row = {key: value for key, value in transformed_row.items() if key in writer.fieldnames}
            
            if not post_validate_row(filtered_row, config['fields']):
                continue  # Skip this row if it fails post-validation
            
            writer.writerow(filtered_row)  # Write the valid transformed row to the output file

if __name__ == '__main__':
    try:
        config_path = os.path.join('config', 'config.json')
        input_csv_path = os.path.join('input', 'sample_data.csv')
        output_csv_path = os.path.join('output', 'transformed_data.csv')
        
        config = load_configuration(config_path)
        process_csv(input_csv_path, output_csv_path, config)
    except (FileNotFoundError, ValueError, IOError) as e:
        handle_configuration_error(e)



