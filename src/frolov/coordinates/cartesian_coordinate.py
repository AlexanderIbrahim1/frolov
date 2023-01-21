"""
A CartesianCoordinate instance represents the four Cartesian3D instances that
make up a four-body geometry.

The naming is somewhat unfortunate, as the four points in each CartesianCoordinate
instance are also themselves coordinates (of type Cartesian3D). The naming was
chosen to maintain consistency with the other coordinate types (GridCoordinate, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from cartesian import Cartesian3D
from cartesian.measure import euclidean_distance


@dataclass(frozen=True)
class CartesianCoordinate:
    point0: Cartesian3D
    point1: Cartesian3D
    point2: Cartesian3D
    point3: Cartesian3D

    def unpack(self) -> Tuple[Cartesian3D, ...]:
        return (self.point0, self.point1, self.point2, self.point3)


def cartesian_distance_squared(
    c0: CartesianCoordinate, c1: CartesianCoordinate
) -> float:
    """
    Calculate the sum of the euclidean distance between each corresponding pair
    of points between the two CartesianCoordinate instances.
    """
    return sum(
        [euclidean_distance(q0, q1) for (q0, q1) in zip(c0.unpack(), c1.unpack())]
    )


def cartesian_approx_eq(
    c0: CartesianCoordinate, c1: CartesianCoordinate, eps_sq: float = 1.0e-6
) -> bool:
    """
    Checks if two coordinate instances are close enough to be essentially equal.
    """
    return cartesian_distance_squared(c0, c1) < eps_sq
