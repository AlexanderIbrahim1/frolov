from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PairDistanceCoordinate:
    r01: float
    r02: float
    r03: float
    r12: float
    r13: float
    r23: float

    def __postinit__(self) -> None:
        assert self._are_all_nonnegative()

    def unpack(self) -> Tuple[float, ...]:
        return (self.r01, self.r02, self.r03, self.r12, self.r13, self.r23)

    def _are_all_nonnegative(self) -> bool:
        """It does not make physical sense for a pair distance to be negative"""
        return all([pairdist >= 0.0 for pairdist in self.unpack()])


def pairdistance_distance_squared(p0: GridCoordinate, p1: GridCoordinate) -> float:
    """
    Calculating the mean of the squared differences between each coordinate.

    It is important to note that this function makes the (possibly) unsubstantiated
    assumption that all 6 grid coordinate elements should all be weighted equally.
    """
    return sum([(c0 - c1)**2 for (c0, c1) in zip(p0.unpack(), p1.unpack())])


def pairdistance_approx_eq(p0: GridCoordinate, p1: GridCoordinate, eps_sq: float = 1.0e-6) -> bool:
    """
    Checks if two coordinate instances are close enough to be essentially equal.
    """
    return grid_distance_squared(p0, p1) < eps_sq
