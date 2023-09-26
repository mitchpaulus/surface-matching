#!/usr/bin/env python3

from typing import List, Tuple, Iterable, Optional
from dataclasses import dataclass
from itertools import combinations
from math import sqrt
import sys

@dataclass
class Point:
    x: float
    y: float
    z: float

    # define addition and subtraction
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def distance(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalized(self) -> 'Point':
        d = self.distance()
        return Point(self.x / d, self.y / d, self.z / d)

    # Support 'array_like' for numpy. Implement iterable protocol
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def cross(self, other):
        # Cross product w/o numpy
        return Point(self.y * other.z - self.z * other.y,
                     self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x)

    def dot(self, other):
        # Dot product w/o numpy
        return self.x * other.x + self.y * other.y + self.z * other.z

    # Define equality, with 0.000001 tolerance, not using numpy
    def __eq__(self, other):
        return abs(self.x - other.x) < 0.000001 and abs(self.y - other.y) < 0.000001 and abs(self.z - other.z) < 0.000001

    def transform(self, transform_matrix: List[List[float]]) -> 'Point':
        # Matrix multiply.
        # Transformation matrix should be 3x3, outer list is rows, inner list is columns

        new_x = self.x * transform_matrix[0][0] + self.y * transform_matrix[0][1] + self.z * transform_matrix[0][2]
        new_y = self.x * transform_matrix[1][0] + self.y * transform_matrix[1][1] + self.z * transform_matrix[1][2]
        new_z = self.x * transform_matrix[2][0] + self.y * transform_matrix[2][1] + self.z * transform_matrix[2][2]

        return Point(new_x, new_y, new_z)

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __repr__(self):
        return self.__str__()


class PlaneEq:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        """
        Plane class
        :param p1: point 1
        :param p2: point 2
        :param p3: point 3
        """
        # Check that each point is 3D vector
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.v1 = p2 - p1
        self.v2 = p3 - p2

        self.normal_vec = self.v1.cross(self.v2)
        self.a: float = self.normal_vec.x
        self.b: float = self.normal_vec.y
        self.c: float = self.normal_vec.z
        self.d: float = -(self.normal_vec.dot(p3))


    def points(self) -> List[Point]:
        return [self.p1, self.p2, self.p3]

    def min_x(self) -> float:
        return min_x(self.points())

    def min_y(self) -> float:
        return min_y(self.points())

    def min_z(self) -> float:
        return min_z(self.points())

    def max_x(self) -> float:
        return max_x(self.points())

    def max_y(self) -> float:
        return max_y(self.points())

    def max_z(self) -> float:
        return max_z(self.points())


    def transform(self, transform_matrix: List[List[float]]) -> 'PlaneEq':
        # Matrix multiply.
        # Transformation matrix should be 3x3, outer list is rows, inner list is columns
        new_p1 = self.p1.transform(transform_matrix)
        new_p2 = self.p2.transform(transform_matrix)
        new_p3 = self.p3.transform(transform_matrix)
        return PlaneEq(new_p1, new_p2, new_p3)


    def overlap(self, other: 'PlaneEq') -> bool:
        # Assume that the 3 points are the corners of rectancles.
        # Check if the rectangles overlap
        # https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other
        # self totally to right of other
        if self.min_x() >= other.max_x():
            return False

        # self totally to left of other
        if self.max_x() <= other.min_x():
            return False

        # self totally above other
        if self.min_y() >= other.max_y():
            return False

        # self totally below other
        if self.max_y() <= other.min_y():
            return False

        return True

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        self.index += 1
        if self.index > 3:
            raise StopIteration
        if self.index == 0:
            return self.a
        if self.index == 1:
            return self.b
        if self.index == 2:
            return self.c
        if self.index == 3:
            return self.d

    # Define equality, with 0.000001 tolerance
    def __eq__(self, other):
        scalar = None
        for x, y in zip(self, other):
            if x == 0:
                if y != 0:
                    return False
                continue
            if y == 0:
                if x != 0:
                    return False
                continue
            current_scalar = y / x
            if scalar is None:
                scalar = current_scalar
            elif scalar != current_scalar:
                return False

        return True

    def __str__(self):
        return f'{self.a}x + {self.b}y + {self.c}z + {self.d} = 0'

    def __repr__(self):
        return f'{self.a}x + {self.b}y + {self.c}z + {self.d} = 0'


def min_x(points: Iterable[Point]) -> float:
    return min([p.x for p in points])

def min_y(points: Iterable[Point]) -> float:
    return min([p.y for p in points])

def min_z(points: Iterable[Point]) -> float:
    return min([p.z for p in points])

def max_x(points: Iterable[Point]) -> float:
    return max([p.x for p in points])

def max_y(points: Iterable[Point]) -> float:
    return max([p.y for p in points])

def max_z(points: Iterable[Point]) -> float:
    return max([p.z for p in points])


class Plane:
    def __init__(self, plane_eq: PlaneEq, name):
        """
        Plane class
        :param p1: point 1
        :param p2: point 2
        :param p3: point 3
        """
        self.plane_eq = plane_eq
        self.name = name

    def __str__(self):
        return f'{self.name}: {self.plane_eq}'

    def __repr__(self):
        return self.__str__()

def surface_match_lines(lines: list[str]) -> str:
    # Assume each line is tab separated values.
    # Col 1: Surface Name
    # Col 2-4: X, Y, Z coordinates for point 1
    # Col 5-7: X, Y, Z coordinates for point 2
    # Col 8-10: X, Y, Z coordinates for point 3
    # Cols ...: Additional columns are ignored
    # Assumed all points are on plane

    # Create list of planes
    planes = []
    for line in lines:
        line = line.split('\t')
        name = line[0]
        p1 = Point(float(line[1]), float(line[2]), float(line[3]))
        p2 = Point(float(line[4]), float(line[5]), float(line[6]))
        p3 = Point(float(line[7]), float(line[8]), float(line[9]))
        plane_eq = PlaneEq(p1, p2, p3)
        planes.append(Plane(plane_eq, name))

    # Group by plane equation
    grouped = group_planes(planes)
    return '\n'.join(['\t'.join([plane.name for plane in group]) for group in grouped])


def group_planes(planes: List[Plane]) -> List[List[Plane]]:
    # Group by plane equation

    grouped: List[List[Plane]] = []

    for plane in planes:
        # Check if plane equation is already in grouped
        for group in grouped:
            if plane.plane_eq == group[0].plane_eq:
                group.append(plane)
                break
        else:
            grouped.append([plane])

    return grouped


def determinant_2x2(a: float, b: float, c: float, d: float) -> float:
    # a b
    # c d
    return a * d - b * c


def determinant_3x3(col1, col2, col3):
    # a b c
    # d e f
    # g h i

    # Assign elements from columns to variables in row-major order
    a, d, g = col1
    b, e, h = col2
    c, f, i = col3

    # Calculate the determinant using determinant_2x2
    det = a * determinant_2x2(e, f, h, i) - b * determinant_2x2(d, f, g, i) + c * determinant_2x2(d, e, g, h)
    return det



def adjugate_3x3(col1, col2, col3):
    # a b c
    # d e f
    # g h i

    # Assign elements from columns to variables in row-major order
    a, d, g = col1
    b, e, h = col2
    c, f, i = col3

    # Calculate the adjugate matrix in row major order
    adjugate = [
        [determinant_2x2(e, f, h, i), -determinant_2x2(b, c, h, i), determinant_2x2(b, c, e, f)],
        [-determinant_2x2(d, f, g, i), determinant_2x2(a, c, g, i), -determinant_2x2(a, c, d, f)],
        [determinant_2x2(d, e, g, h), -determinant_2x2(a, b, g, h), determinant_2x2(a, b, d, e)]
    ]
    return adjugate


def inverse_3x3(col1, col2, col3) -> Optional[List[List[float]]]:
    # a b c
    # d e f
    # g h i

    # Calculate the determinant using determinant_2x2
    det = determinant_3x3(col1, col2, col3)

    # Check if the matrix is singular (non-invertible)
    if det == 0:
        return None

    # Calculate the adjugate matrix
    adjugate = adjugate_3x3(col1, col2, col3)

    # Calculate the inverse matrix by dividing the adjugate matrix by the determinant
    inverse = [[adjugate[0][0] / det, adjugate[0][1] / det, adjugate[0][2] / det],
               [adjugate[1][0] / det, adjugate[1][1] / det, adjugate[1][2] / det],
               [adjugate[2][0] / det, adjugate[2][1] / det, adjugate[2][2] / det]]

    return inverse


def check_group(planes: List[Plane]) -> List[Tuple[Plane, Plane]]:
    test_cases = list(combinations(planes, 2))

    # Create new basis vector from first plane to transform from 3D to 2D
    # Use v1 and normal, take cross product to get 3rd vector


    v1 = planes[0].plane_eq.v1.normalized()
    norm_normal = planes[0].plane_eq.normal_vec.normalized()
    v2 = v1.cross(norm_normal).normalized()

    transform_matrix = inverse_3x3(v1, v2, norm_normal)
    if transform_matrix is None:
        return []

    # Assert that transformation matrix is area perserving, determinant should be 1 or -1.
    d = determinant_3x3(v1, v2, norm_normal)
    assert abs(abs(d) - 1) < 0.000001

    matches = []
    # Create 2D points
    for plane1, plane2 in test_cases:
        # Transform points to 2D
        plane1_2d = plane1.plane_eq.transform(transform_matrix)
        plane2_2d = plane2.plane_eq.transform(transform_matrix)

        # Check if 2D points overlap, z coordinates should equal
        assert abs(plane1_2d.p1.z - plane2_2d.p1.z) < 0.000001

        # Now check for overlap
        if plane1_2d.overlap(plane2_2d):
            matches.append((plane1, plane2))

    return matches


def main():

    # Check if arguments contains '-2' flag, meaning print both directions of match.
    # If not, print only one direction
    print_both = False

    only_first = True

    if any([arg == '-2' for arg in sys.argv]):
        print_both = True

    if any([arg == "--all" or arg == "-a" for arg in sys.argv]):
        only_first = False

    # Read input from stdin, assume TSV
    planes = []

    for line in sys.stdin:
        split_line =  [f.strip() for f in line.split('\t')]

        if len(split_line) < 10:
            continue

        name = split_line[0]
        p1 = Point(float(split_line[1]), float(split_line[2]), float(split_line[3]))
        p2 = Point(float(split_line[4]), float(split_line[5]), float(split_line[6]))
        p3 = Point(float(split_line[7]), float(split_line[8]), float(split_line[9]))

        plane_eq = PlaneEq(p1, p2, p3)
        planes.append(Plane(plane_eq, name))


    # Group by plane equation
    grouped = group_planes(planes)

    # Check each group for matches
    matches: list[Tuple[Plane, Plane]] = []
    for group in grouped:
        group_matches = check_group(group)

        if not print_both:
            matches.extend(check_group(group))
        else:
            matches.extend(group_matches)
            matches.extend([(b, a) for a, b in group_matches])

    # Print matches
    for match in matches:
        print(f'{match[0].name}\t{match[1].name}')

    pass


if __name__ == "__main__":
    main()
