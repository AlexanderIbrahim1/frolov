"""
Calculate the six perimetric coordinates from 4 points in 3D Cartesian space.

We refer to the coordinates (u1, u2, u3, s3, t3, w3) given in the paper.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from cartesian.measure import euclidean_distance as distance
from cartesian import Cartesian3D


@dataclass
class CartesianCoordinate:
    point0: Cartesian3D
    point1: Cartesian3D
    point2: Cartesian3D
    point3: Cartesian3D

    def unpack(self) -> Tuple[Cartesian3D, ...]:
        return (self.point0, self.point1, self.point2, self.point3)


@dataclass
class PairDistanceCoordinate:
    r01: float
    r02: float
    r03: float
    r12: float
    r13: float
    r23: float

    def unpack(self) -> Tuple[float, ...]:
        return (self.r01, self.r02, self.r03, self.r12, self.r13, self.r23)


@dataclass
class PerimetricCoordinate:
    u1: float
    u2: float
    u3: float
    t3: float
    s3: float
    w3: float

    def unpack(self) -> Tuple[float, ...]:
        return (self.u1, self.u2, self.u3, self.t3, self.s3, self.w3)

    def satisfies_inequalities(self) -> bool:
        """Check if all the constraints put on the perimetric coordinates are satisfied."""
        return (
            self.satisfies_s3_inequality()
            and self.satisfies_w3_inequality()
            and self.are_all_positive()
        )

    def satisfies_s3_inequality(self) -> bool:
        """Check if 's3' satisfies the inequality in equation (32) of the paper."""
        lower_limit = max(0.0, self.u3 - self.t3)
        upper_limit = self.u2 + self.u3

        return lower_limit <= self.s3 <= upper_limit

    def satisfies_w3_inequality(self) -> bool:
        """Check if 'w3' satisfies the inequality in equation (32) of the paper."""
        lower_limit = max(0.0, self.u3 - self.t3, self.s3 - self.u2)
        upper_limit = min(self.u1 + self.u3, self.u1 + self.s3)

        return lower_limit <= self.w3 <= upper_limit

    def are_all_positive(self) -> bool:
        return all([peri >= 0.0 for peri in self.unpack()])


def cartesian_to_pairdistance(points: CartesianCoordinate) -> PairDistanceCoordinate:
    """Calculate the 6 relative pair distances from the 4 Cartesian points."""
    point0, point1, point2, point3 = points.unpack()

    r01 = distance(point0, point1)
    r02 = distance(point0, point2)
    r03 = distance(point0, point3)
    r12 = distance(point1, point2)
    r13 = distance(point1, point3)
    r23 = distance(point2, point3)

    return PairDistanceCoordinate(r01, r02, r03, r12, r13, r23)


def pairdistance_to_perimetric(
    pairdists: PairDistanceCoordinate,
) -> PerimetricCoordinate:
    """Calculate the 6 perimetric coordinates from the 6 relative pair distances."""
    r01, r02, r03, r12, r13, r23 = pairdists.unpack()

    u1 = 0.5 * (r02 + r01 - r12)
    u2 = 0.5 * (r01 + r12 - r02)
    u3 = 0.5 * (r12 + r02 - r01)
    t3 = 0.5 * (r13 + r03 - r01)
    s3 = 0.5 * (r23 + r12 - r13)
    w3 = 0.5 * (r23 + r02 - r03)

    return PerimetricCoordinate(u1, u2, u3, t3, s3, w3)
