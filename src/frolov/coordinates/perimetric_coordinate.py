from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PerimetricCoordinate:
    u1: float
    u2: float
    u3: float
    t3: float
    s3: float
    w3: float

    def __postinit__(self) -> None:
        assert self._satisfies_s3_inequality()
        assert self._satisfies_w3_inequality()
        assert self._are_all_nonnegative()

    def unpack(self) -> Tuple[float, ...]:
        return (self.u1, self.u2, self.u3, self.t3, self.s3, self.w3)

    def _satisfies_s3_inequality(self) -> bool:
        """Check if 's3' satisfies the inequality in equation (32) of the paper."""
        lower_limit = max(0.0, self.u3 - self.t3)
        upper_limit = self.u2 + self.u3

        return lower_limit <= self.s3 <= upper_limit

    def _satisfies_w3_inequality(self) -> bool:
        """Check if 'w3' satisfies the inequality in equation (32) of the paper."""
        lower_limit = max(0.0, self.u3 - self.t3, self.s3 - self.u2)
        upper_limit = min(self.u1 + self.u3, self.u1 + self.s3)

        return lower_limit <= self.w3 <= upper_limit

    def _are_all_nonnegative(self) -> bool:
        """None of the coordinates, as constructed in the paper, can be negative."""
        return all([peri >= 0.0 for peri in self.unpack()])


def perimetric_distance_squared(c0: PerimetricCoordinate, c1: PerimetricCoordinate) -> float:
    """
    Calculating the sum of the squared differences between each coordinate.

    It is important to note that this function makes the (possibly) unsubstantiated
    assumption that all 6 coordinate elements should all be weighted equally.
    """
    return sum([(q0 - q1)**2 for (q0, q1) in zip(c0.unpack(), c1.unpack())])


def perimetric_approx_eq(c0: PerimetricCoordinate, c1: PerimetricCoordinate, eps_sq: float = 1.0e-6) -> bool:
    """
    Checks if two coordinate instances are close enough to be essentially equal.
    """
    return perimetric_distance_squared(c0, c1) < eps_sq
