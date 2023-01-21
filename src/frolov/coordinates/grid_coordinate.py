"""
Create a grid from which the six coordinates (u1, u2, u3, s3, t3, w3) can be
generated. Each parameter in the grid can be independently varied along its
own axis.

There are six different ways to structure the constraints on the perimetric
coordinates. We have chosen the way used in the limits of equation (37) in
the paper.

However, we have rearranged the order in which the coordinates are set. The
original way of arranging the limits would cause 'grid_s3' to be undefined
in the case where u2 == u3.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class GridCoordinate:
    grid_u1: float
    grid_u2: float
    grid_u3: float
    grid_t3: float
    grid_s3: float
    grid_w3: float

    def __post_init__(self) -> None:
        assert self._satisfies_grid_constraints()

    def unpack(self) -> Tuple[float, ...]:
        return (
            self.grid_u1,
            self.grid_u2,
            self.grid_u3,
            self.grid_t3,
            self.grid_s3,
            self.grid_w3,
        )

    def _satisfies_grid_constraints(self) -> bool:
        return all(
            [
                self.grid_u1 >= 0,
                self.grid_u2 >= 0,
                self.grid_u3 >= 1,
                self.grid_t3 >= 1,
                self.grid_s3 >= 1,
                1 >= self.grid_w3 >= 0,
            ]
        )


def grid_distance_squared(c0: GridCoordinate, c1: GridCoordinate) -> float:
    """
    Calculating the sum of the squared differences between each coordinate.

    It is important to note that this function makes the (possibly) unsubstantiated
    assumption that all 6 grid coordinate elements should all be weighted equally.
    """
    return sum([(q0 - q1)**2 for (q0, q1) in zip(c0.unpack(), c1.unpack())])


def grid_approx_eq(c0: GridCoordinate, c1: GridCoordinate, eps_sq: float = 1.0e-6) -> bool:
    """
    Checks if two coordinate instances are close enough to be essentially equal.
    """
    return grid_distance_squared(c0, c1) < eps_sq
