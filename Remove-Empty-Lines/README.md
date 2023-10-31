
# Remove Empty Lines from Text File

This Python script removes empty lines from a text file using command-line arguments. 

## Usage

1. Run the script with:

   ```
   python remove_empty_lines.py input_file output_file
   ```

   Replace `input_file` with the input file path and `output_file` with the output file path.

2. The script processes `input_file`, removes empty lines, and saves the result in `output_file`.

## Example

```shell
python remove_empty_lines.py input.txt output.txt
```

This command processes `input.txt` and saves the cleaned content to `output.txt`.

## Error Handling

- Handles incorrect usage with a usage message and exit.
- Gracefully handles file not found errors and other exceptions, providing informative messages.


