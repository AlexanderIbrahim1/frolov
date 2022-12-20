"""
Create a grid from which the six coordinates (u1, u2, u3, s3, t3, w3) can be
generated. Each parameter in the grid can be independently varied along its
own axis.

There are six different ways to structure the constraints on the perimetric
coordinates. We have chosen the way used in the limits of equation (37) in
the paper.
"""

from dataclasses import dataclass
from typing import Tuple

from frolov.coordinates import PerimetricCoordinate


# TODO
# - a function to generate the grid coordinates, given some information about
#   how the grid is structured; i.e. the maximum of grid_u1, the number of
#   divisions of each coordinate, etc.


@dataclass(frozen=True)
class GridCoordinate:
    grid_u1: float
    grid_u2: float
    grid_u3: float
    grid_t3: float
    grid_s3: float
    grid_w3: float

    def __post_init__(self) -> None:
        assert self.satisfies_grid_constraints()

    def unpack(self) -> Tuple[float, ...]:
        return (
            self.grid_u1,
            self.grid_u2,
            self.grid_u3,
            self.grid_t3,
            self.grid_s3,
            self.grid_w3,
        )

    def satisfies_grid_constraints(self) -> bool:
        return all(
            [
                self.grid_u1 >= 0,
                self.grid_u2 >= 0,
                self.grid_u3 >= 1,
                self.grid_t3 >= 1,
                1 >= self.grid_s3 >= 0,
                1 >= self.grid_w3 >= 0,
            ]
        )


def grid_to_perimetric(
    gridcoord: GridCoordinate,
) -> PerimetricCoordinate:
    """
    Perform the transformations that turn a grid coordinate into a perimetric
    coordinate.
    """

    u1 = gridcoord.grid_u1
    u2 = gridcoord.grid_u2
    u3 = gridcoord.grid_u3 * u2
    t3 = gridcoord.grid_t3 * u3
    s3 = gridcoord.grid_s3 * (u3 - u2) + u2
    w3 = gridcoord.grid_w3 * (u1 + u2) + (s3 - u2)

    return PerimetricCoordinate(u1, u2, u3, t3, s3, w3)
