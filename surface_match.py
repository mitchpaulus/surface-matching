#!/usr/bin/env python3

import numpy as np
from typing import List, Tuple


class Plane:
    def __init__(self, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray):
        """
        Plane class
        :param p1: point 1
        :param p2: point 2
        :param p3: point 3
        """
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.a, self.b, self.c, self.d = get_plane_equation(p1, p2, p3)

    def normalize(self) -> None:
        """
        Normalize plane equation
        :return: None
        """
        self.a = self.a / self.d
        self.b = self.b / self.d
        self.c = self.c / self.d
        self.d = 1

    # Define equality, with 0.000001 tolerance
    def __eq__(self, other):
        return np.allclose([self.a, self.b, self.c, self.d], [other.a, other.b, other.c, other.d], atol=0.000001)



def get_plane_equation(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> Tuple[float, float, float, float]:
    """
    Get plane equation from three points
    :param p1: point 1
    :param p2: point 2
    :param p3: point 3
    :return: plane equation
    """
    v1 = p3 - p1
    v2 = p2 - p1
    normal_vec = np.cross(v1, v2)
    a, b, c = normal_vec
    d = -np.dot(normal_vec, p3)

    # Normalize to make d = 1
    a = a / d
    b = b / d
    c = c / d
    d = 1

    return a, b, c, d
