import pytest


from frolov.coordinates.grid_coordinate import GridCoordinate
from frolov.coordinates.grid_coordinate import grid_distance_squared
from frolov.coordinates.grid_coordinate import grid_approx_eq

from randomgen import random_grid_coordinate


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

    @pytest.mark.parametrize(
        "index, invalid_value",
        [
            (0, -0.1),
            (1, -0.1),
            (2, 0.5),
            (3, 0.7),
            (4, 0.8),
            (5, -0.1),
            (5, 1.1),
        ],
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

    def test_approx_eq(self):
        n_attempts = 100
        for _ in range(n_attempts):
            gridcoord0 = random_grid_coordinate()
            gridcoord1 = gridcoord0
            assert grid_approx_eq(gridcoord0, gridcoord1)

    def test_distance_squared(self):
        """
        Create a random grid point, then increase the first 5 coordinates by 1 each.
        The distance between the two should be 5.0.

        We only use the first five because they are unbounded from above, whereas the
        last coordinate is not.
        """
        n_attempts = 100
        for _ in range(n_attempts):
            gridcoord0 = random_grid_coordinate()
            gridcoord1 = GridCoordinate(
                gridcoord0.grid_u1 + 1.0,
                gridcoord0.grid_u2 + 1.0,
                gridcoord0.grid_u3 + 1.0,
                gridcoord0.grid_t3 + 1.0,
                gridcoord0.grid_s3 + 1.0,
                gridcoord0.grid_w3,
            )

            expected_dist_sq = 5 * 1.0
            assert grid_distance_squared(gridcoord0, gridcoord1) == pytest.approx(
                expected_dist_sq
            )
