#!/usr/bin/env python3
import sys
import math

class Zone:
    def __init__(self, name, rotation, x_origin, y_origin, z_origin) -> None:
        self.name = name
        self.rotation = float(rotation)
        self.x_origin = x_origin
        self.y_origin = y_origin
        self.z_origin = z_origin

class Surface:
    def __init__(self, name: str, construction: str, zone: str, points) -> None:
        self.name = name
        self.construction = construction
        self.points = points
        self.zone = zone

def main():

    construction_filter = None
    idx = 1
    while idx < len(sys.argv):
        if sys.argv[idx] == '-h':
            print('Usage: idf_surfaces.py < input.idf > output.idf')
            sys.exit(0)
        elif sys.argv[idx] == "-c":
            if idx + 1 >= len(sys.argv):
                print('Missing construction name after -c')
                sys.exit(1)
            construction_filter = sys.argv[idx + 1]
            idx += 2
        else:
            print('Unrecognized option: ' + sys.argv[idx])
            sys.exit(1)

    zones = []
    surfaces = []

    for line in sys.stdin:
        split_line = [f.strip() for f in line.split('\t')]

        if split_line[0] == 'Zone':
            z = Zone(split_line[1], split_line[2], split_line[3], split_line[4], split_line[5])
            zones.append(z)

        elif split_line[0] == 'Wall:Detailed':
            s = Surface(split_line[1], split_line[2], split_line[3], split_line[11:])
            surfaces.append(s)

        elif split_line[0] == 'Floor:Detailed':
            s = Surface(split_line[1], split_line[2], split_line[3], split_line[11:])
            surfaces.append(s)

        elif split_line[0] == 'RoofCeiling:Detailed':
            s = Surface(split_line[1], split_line[2], split_line[3], split_line[11:])
            surfaces.append(s)

    zone_dict = { z.name: z for z in zones }

    for s in surfaces:
        if construction_filter is not None and s.construction != construction_filter:
            continue

        z = zone_dict[s.zone]

        if abs(z.rotation) > 0.001:
            # Do counter-clockwise rotation first on X-Y coordinates
            current_x = None
            current_y = None
            for i in range(len(s.points)):
                mod_value = i % 3
                if mod_value == 0:
                    current_x = float(s.points[i])
                elif mod_value == 1:
                    current_y = float(s.points[i])
                elif mod_value == 2:
                    if current_x is None or current_y is None:
                        raise Exception('Unexpected error')

                    radians = math.radians(-z.rotation)
                    cos = math.cos(radians)
                    sin = math.sin(radians)

                    new_x = current_x * cos - current_y * sin
                    new_y = current_x * sin + current_y * cos
                    s.points[i - 2] = new_x
                    s.points[i - 1] = new_y


        for i in range(len(s.points)):
            mod_value = i % 3
            if mod_value == 0:
                s.points[i] = float(s.points[i]) + float(z.x_origin)
            elif mod_value == 1:
                s.points[i] = float(s.points[i]) + float(z.y_origin)
            elif mod_value == 2:
                s.points[i] = float(s.points[i]) + float(z.z_origin)

    for s in surfaces:
        if construction_filter is not None and s.construction != construction_filter:
            continue

        fields = [s.name]
        for p in s.points:
            fields.append(str(p))

        print('\t'.join(fields))

if __name__ == "__main__":
    main()
