import math

from cartesian import Cartesian3D
from cartesian.measure import euclidean_distance

from frolov.coordinates.cartesian_coordinate import CartesianCoordinate
from frolov.coordinates.grid_coordinate import GridCoordinate
from frolov.coordinates.pairdistance_coordinate import PairDistanceCoordinate
from frolov.coordinates.perimetric_coordinate import PerimetricCoordinate


def cartesian_to_pairdistance(points: CartesianCoordinate) -> PairDistanceCoordinate:
    """Calculate the 6 relative pair distances from the 4 Cartesian points."""
    point0, point1, point2, point3 = points.unpack()

    r01 = euclidean_distance(point0, point1)
    r02 = euclidean_distance(point0, point2)
    r03 = euclidean_distance(point0, point3)
    r12 = euclidean_distance(point1, point2)
    r13 = euclidean_distance(point1, point3)
    r23 = euclidean_distance(point2, point3)

    return PairDistanceCoordinate(r01, r02, r03, r12, r13, r23)


def pairdistance_to_cartesian(pairdists: PairDistanceCoordinate) -> CartesianCoordinate:
    """
    This function uses the 6 relative pair distances between the four points to
    recover four Cartesian points in 3D space.

    The four points returned satisfy the following properties:
     - point0 is at the origin
     - point1 lies on the positive x-axis
     - point2 satisfies (y >= 0, z == 0)
     - point3 satisfies (x >= 0, y >= 0, z >= 0)

    The 'pairdistance_to_cartesian()' and the 'cartesian_to_pairdistance()' functions
    are not inverses. We lose information when using the 'cartesian_to_pairdistance()'
    transformation. The relative pair distances only have 6 degrees of freedom (DOF) of
    information to work with, but the four Cartesian points have 12 DOF.

    The three DOF describing the centre of mass position of the four-body system are
    lost when converting from relative pair distances to Cartesian coordinates. The
    three DOF describing the orientation in space of the four-body system are also lost.
    """
    r01, r02, r03, r12, r13, r23 = pairdists.unpack()

    cos_theta102 = (r01**2 + r02**2 - r12**2) / (2.0 * r01 * r02)

    x2 = r02 * cos_theta102
    y2 = math.sqrt(r02**2 - x2**2)
    z2 = 0.0

    x3 = (r03**2 - r13**2 + r01**2) / (2.0 * r01)
    y3 = (r03**2 - r23**2 + r02**2 - 2.0 * x2 * x3) / (2.0 * y2)
    z3 = math.sqrt(r03**2 - x3**2 - y3**2)

    point0 = Cartesian3D(0.0, 0.0, 0.0)
    point1 = Cartesian3D(r01, 0.0, 0.0)
    point2 = Cartesian3D(x2, y2, z2)
    point3 = Cartesian3D(x3, y3, z3)

    return CartesianCoordinate(point0, point1, point2, point3)


def pairdistance_to_perimetric(
    pairdists: PairDistanceCoordinate,
) -> PerimetricCoordinate:
    """
    Calculate the 6 perimetric coordinates from the 6 relative pair distances.

    These conversions are taken directly from equation (24) in the paper.
    """
    r01, r02, r03, r12, r13, r23 = pairdists.unpack()

    u1 = 0.5 * (r02 + r01 - r12)
    u2 = 0.5 * (r01 + r12 - r02)
    u3 = 0.5 * (r12 + r02 - r01)
    t3 = 0.5 * (r13 + r03 - r01)
    s3 = 0.5 * (r23 + r12 - r13)
    w3 = 0.5 * (r23 + r02 - r03)

    return PerimetricCoordinate(u1, u2, u3, t3, s3, w3)


def perimetric_to_pairdistance(
    perimetric: PerimetricCoordinate,
) -> PairDistanceCoordinate:
    """
    Calculate the 6 relative pair distance coordinates from the 6 perimetric
    coordinates.

    These conversions are taken directly from equation (25) in the paper.
    """
    u1, u2, u3, t3, s3, w3 = perimetric.unpack()

    r12 = u1 + u2
    r13 = u1 + u3
    r14 = u1 + s3 + t3 - w3
    r23 = u2 + u3
    r24 = u2 + w3 + t3 - s3
    r34 = t3 + w3 + s3 - u3

    return PairDistanceCoordinate(r12, r13, r14, r23, r24, r34)


def perimetric_to_grid(perimetric: PerimetricCoordinate) -> GridCoordinate:
    """Perform the inverse transformations of 'grid_to_perimetric()'"""
    u1, u2, u3, t3, s3, w3 = perimetric.unpack()

    grid_u1 = u1
    grid_u2 = u2
    grid_s3 = s3 / u2
    grid_u3 = u3 / s3
    grid_t3 = t3 / u3
    grid_w3 = (w3 - s3 + u2) / (u1 + u2)

    return GridCoordinate(grid_u1, grid_u2, grid_u3, grid_t3, grid_s3, grid_w3)


def grid_to_perimetric(gridcoord: GridCoordinate) -> PerimetricCoordinate:
    """Perform the transformations that turn a grid coordinate into a perimetric coordinate."""
    grid_u1, grid_u2, grid_u3, grid_t3, grid_s3, grid_w3 = gridcoord.unpack()

    u1 = grid_u1
    u2 = grid_u2
    s3 = grid_s3 * u2
    u3 = grid_u3 * s3
    t3 = grid_t3 * u3
    w3 = grid_w3 * (u1 + u2) + (s3 - u2)

    return PerimetricCoordinate(u1, u2, u3, t3, s3, w3)
