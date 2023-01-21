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
