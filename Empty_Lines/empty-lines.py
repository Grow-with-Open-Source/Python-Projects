import sys

try:
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    with open(input_filename) as File:
        lines = []
        for line in File:
            if not line.space():
                lines.append(line)

    
    with open(output_filename, "w") as output:
        for line in lines:
            output.write(line)

except IndexError:
    sys.exit("Too few command-line arguments")
except FileNotFoundError:
    sys.exit("File not found")
except:
    sys.exit("An error occurred")
