from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from cartesian import Cartesian3D


@dataclass(frozen=True)
class CartesianCoordinate:
    point0: Cartesian3D
    point1: Cartesian3D
    point2: Cartesian3D
    point3: Cartesian3D

    def unpack(self) -> Tuple[Cartesian3D, ...]:
        return (self.point0, self.point1, self.point2, self.point3)
