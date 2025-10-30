#!/usr/bin/env python3

import sys

class Polygon:
    def __init__(self, name: str, points: list[tuple[float, float]]) -> None:
        self.name = name
        self.points = points
    def min_x(self):
        return min(p[0] for p in self.points)
    def min_y(self):
        return min(p[1] for p in self.points)
    def max_x(self):
        return max(p[0] for p in self.points)
    def max_y(self):
        return max(p[1] for p in self.points)

    def __str__(self):
        return f'Polygon {self.name} ({len(self.points)})'

    def __repr__(self):
        return self.__str__()

def calculate_viewbox(polygons):
    min_x: float = min(p.min_x() for p in polygons)
    min_y: float = min(p.min_y() for p in polygons)
    max_x: float = max(p.max_x() for p in polygons)
    max_y: float = max(p.max_y() for p in polygons)
    return f"{min_x} {min_y} {max_x - min_x} {max_y - min_y}"

def read_polygon_file(filelike, dimensions) -> list[Polygon]:
    """Expects a file with lines like (3d):
    name1, x1, y1, x2, y2, x3, y3, ...
    or (2d):
    name1, x1, y1, x2, y2, ...
    """
    polygons = []
    #  with open(filename, 'r') as file:
    for line in filelike:
        if "\t" in line:
            parts = [p.strip() for p in line.split("\t")]
        else:
            parts = [p.strip() for p in line.split(",")]
        name = parts[0]
        coords = [float(x) for x in parts[1:]]

        points = [(coords[i], -coords[i+1]) for i in range(0, len(coords), dimensions)]
        polygons.append(Polygon(name, points))

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

def write_svg_file(polygons: list[Polygon]) -> str:
    lines = []
    viewbox = calculate_viewbox(polygons)
    lines.append('<?xml version="1.0" encoding="UTF-8" ?>\n')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="2560" height="1080" viewBox="{viewbox}">\n')

    font_size = 1

    for p in polygons:
        points_str = ' '.join([f'{x},{y}' for x, y in p.points])
        lines.append(f'  <polygon points="{points_str}" style="fill:none;stroke:black;stroke-width:0.1" />\n')

        centroid_x, centroid_y = find_centroid(p.points)
        lines.append(f'  <text text-anchor="middle" dominant-baseline="middle" x="{centroid_x}" y="{centroid_y}" font-family="Verdana" font-size="{font_size}" fill="black">{p.name}</text>\n')

    lines.append('</svg>\n')
    return "".join(lines)


def main():

    dimensions = 2

    filename = None

    idx = 1
    while (idx < len(sys.argv)):
        a = sys.argv[idx]
        if (sys.argv[idx] == '-3'):
            dimensions = 3
            idx += 1
        elif a == "-h" or a == "--help":
            print("Usage: idf_surface_draw.py [-3] [filename]")
            print("filename: The name of file with contents like: ")
            print("3d")
            print("name1, x1, y1, x2, y2, x3, y3, ...")
            print("2d")
            print("name1, x1, y1, x2, y2, ...")
            sys.exit(0)
        else:
            filename = sys.argv[idx]
            idx += 1

    if filename is not None:
        with open(filename, 'r') as file:
            polygons = read_polygon_file(file, dimensions)
    elif filename is None and sys.stdin.isatty():
        print("Please specify a filename")
        sys.exit(1)
    elif not sys.stdin.isatty():
        polygons = read_polygon_file(sys.stdin, dimensions)
    else:
        raise ValueError("Should not be possible")


    print(f'Found {len(polygons)} polygons', file=sys.stderr)
    print(polygons, file=sys.stderr)

    output = write_svg_file(polygons)
    print(output)


if __name__ == '__main__':
    main()
