# crisp-takehome
takehome project for Crisp

# CSV Data Processing System

This system is designed to process CSV files by validating and transforming data according to rules defined in a JSON configuration file. It is capable of archiving previous runs, pre-validating input, transforming data, and post-validating the output.

## Project Structure

- `config/`: Contains configuration files.
- `input/`: Directory for input CSV files.
- `logs/`: Log files are saved here.
- `output/`: Transformed CSV files are stored in this directory.
- `process_csv/`: Contains the Python code for processing.
- `tests/`: Test suite for the project.
  - `data/`: Test datasets.
  - `integration/`: Integration tests.
  - `unit/`: Unit tests.

## Getting Started

### Prerequisites

- Python 3.8
- This project was developed and tested on Python 3.8.  It uses only standard library functions within Python 3.8 so it should run on higher Python versions. 

### Installation and Usage

1. Clone the repository:
   ```shell
   git clone https://github.com/lisac23/crisp-takehome.git
   ```
2. Place the config.json file in the /config directory
3. Place the sample_data.csv file in the /input directory
4. Navigate to the /process_csv directory and run 
   ```shell
   python process_csv/main.py
   ```

## Testing

### Test Execution

This program has a full test coverage suite for all functions used in the transformation process.  Tests can be run from the root directory using the command:
```shell
python -m unittest discover -s tests
```

## Usage Notes
- Ensure that the CSV files conform to the expected format as defined in the config.json.
- Check logs/err.log for any errors that may have occurred during processing.

