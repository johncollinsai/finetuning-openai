# File paths
input_file_path = "/home/john/finetuning-openai/df_data_AAPL.txt"
output_file_path = "/home/john/finetuning-openai/100_lines_AAPL.txt"

# Read the first 500 lines and write to the new file
with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
    for _ in range(250):
        line = infile.readline()
        if not line:
            break  # Break if there are fewer than 10,000 lines
        outfile.write(line)

output_file_path