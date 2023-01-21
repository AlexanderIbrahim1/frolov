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


def pairdistance_distance_squared(c0: PairDistanceCoordinate, c1: PairDistanceCoordinate) -> float:
    """
    Calculating the sum of the squared differences between each coordinate.
    """
    return sum([(q0 - q1)**2 for (q0, q1) in zip(c0.unpack(), c1.unpack())])


def pairdistance_approx_eq(c0: PairDistanceCoordinate, c1: PairDistanceCoordinate, eps_sq: float = 1.0e-6) -> bool:
    """
    Checks if two coordinate instances are close enough to be essentially equal.
    """
    return pairdistance_distance_squared(c0, c1) < eps_sq
