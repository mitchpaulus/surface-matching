import unittest
import surface_match

class TestSurfaceMatching(unittest.TestCase):

    def test_cross_product(self):
        p1 = surface_match.Point(1, 2, 3)
        p2 = surface_match.Point(4, 5, 6)

        cross_product2 = p1.cross(p2)

        # Should be [-3, 6, -3]
        self.assertEqual(cross_product2.x, -3)
        self.assertEqual(cross_product2.y, 6)
        self.assertEqual(cross_product2.z, -3)


    def test_dot_product(self):
        v1 = surface_match.Point(1, 2, 3)
        v2 = surface_match.Point(4, 5, 6)
        dot_product = v1.dot(v2)
        self.assertEqual(dot_product, 32)

    def test_equality(self):
        p1 = surface_match.Point(1, 0, 0)
        p2 = surface_match.Point(1, 1, 0)
        p3 = surface_match.Point(0, 1, 0)

        plane1 = surface_match.PlaneEq(p1, p2, p3)

        p4 = surface_match.Point(2, 2, 0)
        p5 = surface_match.Point(2, 3, 0)
        p6 = surface_match.Point(3, 3, 0)

        plane2 = surface_match.PlaneEq(p4, p5, p6)

        p7 = surface_match.Point(1,0,1)
        p8 = surface_match.Point(1,1,1)
        p9 = surface_match.Point(0,1,1)

        self.assertTrue(plane1 == plane2)

        plane3 = surface_match.PlaneEq(p7, p8, p9)
        self.assertFalse(plane1 == plane3)

    def test_match(self):
        p1 = surface_match.Point(1, 0, 0)
        p2 = surface_match.Point(1, 1, 0)
        p3 = surface_match.Point(0, 1, 0)

        plane1 = surface_match.Plane( surface_match.PlaneEq(p1, p2, p3), "Plane 1")

        p4 = surface_match.Point(2, 2, 0)
        p5 = surface_match.Point(2, 3, 0)
        p6 = surface_match.Point(3, 3, 0)

        plane2 = surface_match.Plane( surface_match.PlaneEq(p4, p5, p6), "Plane 2")

        p7 = surface_match.Point(1,0,1)
        p8 = surface_match.Point(1,1,1)
        p9 = surface_match.Point(0,1,1)

        plane3 = surface_match.Plane( surface_match.PlaneEq(p7, p8, p9), "Plane 3")

        p10 = p7 + surface_match.Point(0.5, 0.5, 0)
        p11 = p8 + surface_match.Point(0.5, 0.5, 0)
        p12 = p9 + surface_match.Point(0.5, 0.5, 0)

        print(p10)
        print(p11)
        print(p12)

        plane4 = surface_match.Plane( surface_match.PlaneEq(p10, p11, p12), "Plane 4")

        group = surface_match.group_planes([plane1, plane2, plane3, plane4])

        for g in group:
            if len(g) > 1:
                matches = surface_match.check_group(g)
                for m in matches:
                    print("Match:")
                    print(m)


        print(group)

    def test_matrix_inverse(self):
        col1 = [1, 2, 3]
        col2 = [0, 1, 4]
        col3 = [5, 6, 0]
        inverse = surface_match.inverse_3x3(col1, col2, col3)
        print("Inverse:")
        print(inverse)
        deter = surface_match.determinant_3x3(col1, col2, col3)
        print("Determinant:")
        print(deter)

        adjugate = surface_match.adjugate_3x3(col1, col2, col3)

        print("Adjugate:")
        print(adjugate)


