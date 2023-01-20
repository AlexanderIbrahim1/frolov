import pytest

import math
import random

from frolov.coordinates import PerimetricCoordinate
from frolov.grid import GridCoordinate
from frolov.grid import grid_to_perimetric
from frolov.grid import perimetric_to_grid


def approx_eq(g0: GridCoordinate, g1: GridCoordinate, eps: float) -> bool:
    grid_distance_sq = sum([
        (grid_coord0 - grid_coord1)**2
        for (grid_coord0, grid_coord1) in zip(g0.unpack(), g1.unpack())
    ])

    return math.sqrt(grid_distance_sq) < eps


def random_grid_coordinate() -> GridCoordinate:
    """
    Create a random GridCoordinate instance that satisfies the grid constraints. The
    chosen maximum is arbitary, and should not affect the test this function is used in.
    """
    maximum_grid_value = 10.0

    grid_u1 = random.uniform(0.0, maximum_grid_value)
    grid_u2 = random.uniform(0.0, maximum_grid_value)
    grid_u3 = random.uniform(1.0, maximum_grid_value)
    grid_t3 = random.uniform(1.0, maximum_grid_value)
    grid_s3 = random.uniform(1.0, maximum_grid_value)
    grid_w3 = random.uniform(0.0, 1.0)

    return GridCoordinate(grid_u1, grid_u2, grid_u3, grid_t3, grid_s3, grid_w3)



class TestGridCoordinate:
    def test_basic_functionality(self):
        gc = GridCoordinate(0.1, 0.2, 1.3, 1.4, 1.1, 0.6)

        # make sure everything is set as expected
        assert gc.grid_u1 == pytest.approx(0.1)
        assert gc.grid_u2 == pytest.approx(0.2)
        assert gc.grid_u3 == pytest.approx(1.3)
        assert gc.grid_t3 == pytest.approx(1.4)
        assert gc.grid_s3 == pytest.approx(1.1)
        assert gc.grid_w3 == pytest.approx(0.6)
        
        pc = grid_to_perimetric(gc)
        assert pc.satisfies_inequalities()

    @pytest.mark.parametrize(
        'index, invalid_value',
        [
            (0, -0.1),
            (1, -0.1),
            (2, 0.5),
            (3, 0.7),
            (4, 0.8),
            (5, -0.1),
            (5, 1.1),
        ]
    )
    def test_raises_invalid_grid_constraints(self, index, invalid_value):
        """
        Make sure the GridCoordinate instance cannot be constructed when a value is
        invalid; start with a collection of valid values, and, and swap a valid value
        with an invalid one.
        """
        coordinates = [0.1, 0.2, 1.3, 1.4, 1.1, 0.6]
        coordinates[index] = invalid_value

        with pytest.raises(AssertionError):
            GridCoordinate(*coordinates)

    def test_grid_perimetric_inversion(self):
        n_attempts = 1000
        eps_tolerance = 1.0e-12

        for _ in range(n_attempts):
            original_grid_coord = random_grid_coordinate()
            perimetric_coord = grid_to_perimetric(original_grid_coord)
            recovered_grid_coord = perimetric_to_grid(perimetric_coord)

            assert approx_eq(original_grid_coord, recovered_grid_coord, eps_tolerance)
