import re

# Input and output file paths
input_file_path = 'sigg instruments/raw_html_etfs.txt'
output_file_path = 'valid_tickers.txt'

# Regular expression pattern to match lines with ticker symbols
pattern = r'<tr id="instrument_(\w+)">'

# Open the input and output files
with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    # Read each line from the input file
    for line in input_file:
        # Use regex to find ticker symbols in the line
        matches = re.findall(pattern, line)
        
        # If there are matches, write them to the output file
        if matches:
            for match in matches:
                output_file.write(match + '\n')
