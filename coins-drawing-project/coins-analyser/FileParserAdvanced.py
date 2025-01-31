import re

def parse(input_filename, output_filename):
    try:
        with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
            for line in infile:
                line = line.strip()

                if line.startswith('G0'):
                    line = line.replace('G0', 'U')
                elif line.startswith('G1'):
                    line = line.replace('G1', 'D')
                match = re.match(r"([UDG\d]+)\s+X(\d+\.?\d*)\s+Y(\d+\.?\d*).*", line)
                if match:
                    command = match.group(1)
                    x = int(round(float(match.group(2))))
                    y = int(round(float(match.group(3))))
                    outfile.write(f"{command} {x} {y}\n")
                elif line.startswith(('G2322')):
                     outfile.write(line + '\n')

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")

input_file = "/Users/diamantelz/Desktop/coins/drawing-coin-add.gcode"
output_file = "/Users/diamantelz/Desktop/coins/drawing-coin-add-edited-edited.gcode"
parse(input_file, output_file)