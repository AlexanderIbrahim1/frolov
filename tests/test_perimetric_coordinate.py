import pytest

import math

from cartesian import Cartesian3D

from frolov.conversions import cartesian_to_pairdistance
from frolov.conversions import pairdistance_to_perimetric
from frolov.coordinates.cartesian_coordinate import CartesianCoordinate

from randomgen import random_cartesian_coordinate


class TestPerimetricCoordinate:
    @pytest.mark.skip
    def test_basic_functionality(self):
        pass

    @pytest.mark.skip
    def test_raises_negative_value(self, index):
        pass


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


def test_inequality_satisfaction():
    """
    The perimetric coordinates must always satisfy the inequalities given in
    equation (32) of the paper. Check if this works by generating four points
    at random, converting them to perimetric coordinates. The success of the
    construction of a PerimetricCoordinate instance implies the satisfaction
    of the inequalities.

    The points will all lie within a cube.
    """

    cube_sidelen = 1.0

    n_attempts = 10000
    for _ in range(n_attempts):
        cartcoord = random_cartesian_coordinate(cube_sidelen)
        pairdists = cartesian_to_pairdistance(cartcoord)
        pairdistance_to_perimetric(pairdists)
