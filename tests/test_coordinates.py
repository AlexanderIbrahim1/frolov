import pytest

import itertools
import math
from typing import Tuple

from cartesian import Cartesian3D
from cartesian.measure import euclidean_distance as distance

from frolov.coordinates import CartesianCoordinate
from frolov.coordinates import PairDistanceCoordinate
from frolov.coordinates import PerimetricCoordinate
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
