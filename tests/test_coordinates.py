import pytest

import itertools
import math
import random

from cartesian import Cartesian3D
from cartesian.measure import euclidean_distance as distance

from frolov.coordinates import CartesianCoordinate
from frolov.coordinates import cartesian_to_pairdistance
from frolov.coordinates import pairdistance_to_perimetric


def tetrahedron_points(sidelen: float) -> CartesianCoordinate:
    assert sidelen > 0.0

    return CartesianCoordinate(
        Cartesian3D(-0.5 * sidelen, 0.0, 0.0),
        Cartesian3D(0.5 * sidelen, 0.0, 0.0),
        Cartesian3D(0.0, math.sqrt(3.0 / 4.0) * sidelen, 0.0),
        Cartesian3D(
            0.0, math.sqrt(1.0 / 12.0) * sidelen, math.sqrt(2.0 / 3.0) * sidelen
        ),
    )


def random_point_in_positive_octant_box(box_length: float) -> Cartesian3D:
    """
    Generate a random Cartesian3D point, where the x-, y-, and z-coordinates all
    lie between 0.0 and 'box_length'.
    """
    return Cartesian3D(
        random.uniform(0.0, box_length),
        random.uniform(0.0, box_length),
        random.uniform(0.0, box_length),
    )


def test_tetrahedron_side_lengths():
    """
    Make sure all the side lengths of the tetrahedron I generated are equal.
    I want to make sure I actually created a tetrahedron.
    """
    points = tetrahedron_points(1.0)
    sidelengths = [
        distance(p0, p1) for (p0, p1) in itertools.combinations(points.unpack(), 2)
    ]

    for sidelen in sidelengths:
        assert sidelen == pytest.approx(1.0)


@pytest.mark.parametrize("sidelen", [0.5, 1.0, 2.0])
def test_tetrahedron(sidelen):
    """
    The tetrahedron should have all perimetric coordinates equal to half of
    the side length of the tetrahedron.
    """
    points = tetrahedron_points(sidelen)
    pairdists = cartesian_to_pairdistance(points)
    perimetrics = pairdistance_to_perimetric(pairdists)

    for peri_coord in perimetrics.unpack():
        assert peri_coord == pytest.approx(sidelen / 2.0)

    assert perimetrics.satisfies_inequalities()


def test_square():
    """
    NOTE: the perimetric coordinates will change if you change the other of the
    points. The perimetric coordinates chosen for this test only work for this
    set of points.
    """

    sidelen = 1.0
    points = CartesianCoordinate(
        Cartesian3D(0.0, sidelen, 0.0),
        Cartesian3D(sidelen, sidelen, 0.0),
        Cartesian3D(sidelen, 0.0, 0.0),
        Cartesian3D(0.0, 0.0, 0.0),
    )
    pairdists = cartesian_to_pairdistance(points)
    perimetrics = pairdistance_to_perimetric(pairdists)

    assert perimetrics.u1 == pytest.approx(sidelen / math.sqrt(2.0))
    assert perimetrics.u2 == pytest.approx(sidelen * (1.0 - math.sqrt(0.5)))
    assert perimetrics.u3 == pytest.approx(sidelen / math.sqrt(2.0))
    assert perimetrics.t3 == pytest.approx(sidelen / math.sqrt(2.0))
    assert perimetrics.s3 == pytest.approx(sidelen * (1.0 - math.sqrt(0.5)))
    assert perimetrics.w3 == pytest.approx(sidelen / math.sqrt(2.0))
    assert perimetrics.satisfies_inequalities()


def test_inequality_satisfaction():
    """
    The perimetric coordinates must always satisfy the inequalities given in
    equation (32) of the paper. Check if this works by generating four points
    at random, converting them to perimetric coordinates, and checking if they
    satisfy the inequalities.

    The points will all lie within a cube.
    """

    cube_sidelen = 1.0

    n_attempts = 10000
    for _ in range(n_attempts):
        p0 = random_point_in_positive_octant_box(cube_sidelen)
        p1 = random_point_in_positive_octant_box(cube_sidelen)
        p2 = random_point_in_positive_octant_box(cube_sidelen)
        p3 = random_point_in_positive_octant_box(cube_sidelen)

        cartesians = CartesianCoordinate(p0, p1, p2, p3)
        pairdists = cartesian_to_pairdistance(cartesians)
        perimetrics = pairdistance_to_perimetric(pairdists)

        assert perimetrics.satisfies_inequalities()
