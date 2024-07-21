#!/usr/bin/env python3

import sys

def calculate_viewbox(polygons):
    min_x: float = min(p[0] for poly in polygons.values() for p in poly)
    min_y: float = min(p[1] for poly in polygons.values() for p in poly)
    max_x: float = max(p[0] for poly in polygons.values() for p in poly)
    max_y: float = max(p[1] for poly in polygons.values() for p in poly)
    return f"{min_x} {min_y} {max_x - min_x} {max_y - min_y}"

def read_polygon_file(filelike, dimensions) -> dict[str, list[tuple[float, float]]]:
    """Expects a file with lines like (3d):
    name1, x1, y1, x2, y2, x3, y3, ...
    or (2d):
    name1, x1, y1, x2, y2, ...
    """
    polygons = {}
    #  with open(filename, 'r') as file:
    for line in filelike:
        if "\t" in line:
            parts = [p.strip() for p in line.split("\t")]
        else:
            parts = [p.strip() for p in line.split(",")]
        name = parts[0]
        coords = [float(x) for x in parts[1:]]
        # Negative is to flip the y-axis.
        polygons[name] = [(coords[i], -coords[i+1]) for i in range(0, len(coords), dimensions)]

    return polygons

def find_centroid(polygon: list[tuple[float, float]]):
    if len(polygon) < 3:
         raise ValueError(f'Polygon must contain at least three points. {polygon}')

    # Reference: https://stackoverflow.com/a/5271722/5932184

    # X = SUM[(Xi + Xi+1) * (Xi * Yi+1 - Xi+1 * Yi)] / 6 / A
    # Y = SUM[(Yi + Yi+1) * (Xi * Yi+1 - Xi+1 * Yi)] / 6 / A
    # A = 1/2 * SUM[(Xi * Yi+1 - Xi+1 * Yi)]

    # Just return average x and y for now.
    x = sum(x for x, y in polygon) / len(polygon)
    y = sum(y for x, y in polygon) / len(polygon)
    return x, y

    #  area = 0
    #  for i in range(len(polygon) - 1):
        #  x1, y1 = polygon[i]
        #  x2, y2 = polygon[i+1]
        #  area += x1 * y2 - x2 * y1

    #  area /= 2

    #  if area == 0:
        #  raise ValueError(f'Polygon has no area. {polygon}')

    #  x = 0
    #  y = 0
    #  for i in range(len(polygon) - 1):
        #  x1, y1 = polygon[i]
        #  x2, y2 = polygon[i+1]
        #  x += (x1 + x2) * (x1 * y2 - x2 * y1)
        #  y += (y1 + y2) * (x1 * y2 - x2 * y1)

    #  x /= 6 * area
    #  y /= 6 * area

    #  return x, y

def write_svg_file(polygons):
    lines = []
    viewbox = calculate_viewbox(polygons)
    lines.append('<?xml version="1.0" encoding="UTF-8" ?>\n')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="2560" height="1080" viewBox="{viewbox}">\n')

    font_size = 1

    for name, polygon in polygons.items():
        points_str = ' '.join([f'{x},{y}' for x, y in polygon])
        lines.append(f'  <polygon points="{points_str}" style="fill:none;stroke:black;stroke-width:0.1" />\n')

        centroid_x, centroid_y = find_centroid(polygon)
        lines.append(f'  <text text-anchor="middle" dominant-baseline="middle" x="{centroid_x}" y="{centroid_y}" font-family="Verdana" font-size="{font_size}" fill="black">{name}</text>\n')

    lines.append('</svg>\n')
    return "".join(lines)


def main():
    dimensions = 2

    filename = None

    idx = 1
    while (idx < len(sys.argv)):
        if (sys.argv[idx] == '-3'):
            dimensions = 3
            idx += 1
        else:
            filename = sys.argv[idx]
            idx += 1

    if filename is None and sys.stdin.isatty():
        print("Please specify a filename")
        sys.exit(1)
    elif not sys.stdin.isatty():
        polygons = read_polygon_file(sys.stdin, dimensions)
    elif filename is not None:
        with open(filename, 'r') as file:
            polygons = read_polygon_file(file, dimensions)
    else:
        raise ValueError("Should not be possible")


    print(f'Found {len(polygons)} polygons', file=sys.stderr)
    print(polygons, file=sys.stderr)

    output = write_svg_file(polygons)
    print(output)


if __name__ == '__main__':
    main()
