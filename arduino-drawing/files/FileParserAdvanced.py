import re

def parse(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                line = line.strip()

                if line.startswith('g0'):
                    line = line.replace('g0', 'U')
                elif line.startswith('g1'):
                    line = line.replace('g1', 'D')
                match = re.match(r"([UDG\d]+)\s+X(\d+\.?\d*)\s+Y(\d+\.?\d*).*", line)
                if match:
                    command = match.group(1)
                    x = int(round(float(match.group(2))))
                    y = int(round(float(match.group(3))))
                    outfile.write(f"{command} {x} {y}\n")
                elif line.startswith(('g21')):
                     outfile.write(line + '\n')

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")

input_file = "/Users/diamantelz/Downloads/optimised_IMG_1900-alt-ver-simple.gcode"
output_file = "/Users/diamantelz/Downloads/optimised_IMG_1900-alt-ver-simple-edited.gcode"
parse(input_file, output_file)