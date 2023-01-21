"""
This module contains functions used to randomly generate coordinates, which are
used in various tests.
"""

import random

from cartesian import Cartesian3D

from frolov.coordinates.cartesian_coordinate import CartesianCoordinate
from frolov.coordinates.grid_coordinate import GridCoordinate


def random_grid_coordinate(maximum_grid_value: float = 10.0) -> GridCoordinate:
    """
    Create a random GridCoordinate instance that satisfies the grid constraints. The
    chosen maximum is arbitary, and should not affect the test this function is used in.
    """
    assert maximum_grid_value > 1.0

    grid_u1 = random.uniform(0.0, maximum_grid_value)
    grid_u2 = random.uniform(0.0, maximum_grid_value)
    grid_u3 = random.uniform(1.0, maximum_grid_value)
    grid_t3 = random.uniform(1.0, maximum_grid_value)
    grid_s3 = random.uniform(1.0, maximum_grid_value)
    grid_w3 = random.uniform(0.0, 1.0)

    return GridCoordinate(grid_u1, grid_u2, grid_u3, grid_t3, grid_s3, grid_w3)


def random_cartesian_coordinate(cube_sidelen: float = 1.0) -> CartesianCoordinate:
    """Generate four points in Cartesian3D space inside a box"""
    p0 = random_point_in_positive_octant_box(cube_sidelen)
    p1 = random_point_in_positive_octant_box(cube_sidelen)
    p2 = random_point_in_positive_octant_box(cube_sidelen)
    p3 = random_point_in_positive_octant_box(cube_sidelen)

    return CartesianCoordinate(p0, p1, p2, p3)


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
