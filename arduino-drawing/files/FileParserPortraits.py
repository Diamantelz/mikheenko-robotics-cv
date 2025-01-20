import re
import numpy as np
import rdp

def simplify_gcode(input_filename, output_filename):
    points = []
    commands = []
    other_lines = []

    with open(input_filename, 'r') as infile:
        for line in infile:
            match = re.match(r'(g0|g1) x([\-\d\.]+) y([\-\d\.]+)', line)
            if match:
                command = match.group(1)
                x = float(match.group(2))
                y = float(match.group(3))
                points.append((x, y))
                commands.append(command)
            else:
                other_lines.append(line)

    if not points:
        with open(output_filename, 'w') as outfile:
            for line in other_lines:
                outfile.write(line)
        return

    points_np = np.array(points)

    tolerance = 0.9
    simplified_points = rdp.rdp(points_np, epsilon=tolerance)

    simplified_commands = []
    points_np_list = list(map(tuple, points_np))
    for point in simplified_points:
        closest_index = points_np_list.index(tuple(point))
        simplified_commands.append(commands[closest_index])

    with open(output_filename, 'w') as outfile:
        for line in other_lines:
            outfile.write(line)
        for i, (x, y) in enumerate(simplified_points):
            outfile.write(f"{simplified_commands[i]} X{x:.3f} Y{y:.3f}\n")

simplify_gcode("/Users/diamantelz/Downloads/optimised_draw_parsed.gcode",
               "/Users/diamantelz/Downloads/draw-portrait-simple.gcode")
