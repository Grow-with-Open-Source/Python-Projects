import sys

# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    print("Usage: python remove_empty_lines.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    # Open the input file for reading and the output file for writing
    with open(input_file, "r") as in_file, open(output_file, "w") as out_file:
        for line in in_file:
            # Check if the line is not empty (contains at least one non-space character)
            if line.strip():
                out_file.write(line)

    print(f"Empty lines removed and saved to {output_file}")
except FileNotFoundError:
    print("File not found. Please check the file paths.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
