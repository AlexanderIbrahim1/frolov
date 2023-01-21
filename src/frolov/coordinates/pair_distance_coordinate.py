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
