import pytest

import math

from cartesian import Cartesian3D

from frolov.coordinates.cartesian_coordinate import CartesianCoordinate
from frolov.coordinates.cartesian_coordinate import cartesian_distance_squared
from frolov.coordinates.cartesian_coordinate import cartesian_approx_eq


def tetrahedron_points(sidelen: float) -> list[Cartesian3D]:
    assert sidelen > 0.0

    return [
        Cartesian3D(-0.5 * sidelen, 0.0, 0.0),
        Cartesian3D(0.5 * sidelen, 0.0, 0.0),
        Cartesian3D(0.0, math.sqrt(3.0 / 4.0) * sidelen, 0.0),
        Cartesian3D(
            0.0, math.sqrt(1.0 / 12.0) * sidelen, math.sqrt(2.0 / 3.0) * sidelen
        ),
    ]


class TestCartesianCoordinate:
    def test_basic_functionality(self):
        points = tetrahedron_points(1.0)
        cartcoord = CartesianCoordinate(*points)

        assert cartcoord.point0 == points[0]
        assert cartcoord.point1 == points[1]
        assert cartcoord.point2 == points[2]
        assert cartcoord.point3 == points[3]

    def test_equality(self):
        points = tetrahedron_points(1.0)
        cartcoord0 = CartesianCoordinate(*points)
        cartcoord1 = CartesianCoordinate(*points)

        assert cartesian_approx_eq(cartcoord0, cartcoord1)

    def test_distance_squared(self):
        """
        Move the entire tetrahedron +1 along the x-axis, and check that the distance
        between the two CartesianCoordinate instances is 4 * 1.0 = 4.0.
        """
        points = tetrahedron_points(1.0)
        points_shifted_right = [p + Cartesian3D(1.0, 0.0, 0.0) for p in points]

        cartcoord0 = CartesianCoordinate(*points)
        cartcoord1 = CartesianCoordinate(*points_shifted_right)

        expected_dist_sq = 4 * 1.0
        assert cartesian_distance_squared(cartcoord0, cartcoord1) == pytest.approx(
            expected_dist_sq
        )
