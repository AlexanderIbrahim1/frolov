from frolov.conversions import cartesian_to_pairdistance
from frolov.conversions import pairdistance_to_cartesian
from frolov.conversions import pairdistance_to_perimetric
from frolov.conversions import perimetric_to_pairdistance
from frolov.conversions import perimetric_to_grid
from frolov.conversions import grid_to_perimetric

from frolov.coordinates.cartesian_coordinate import cartesian_approx_eq
from frolov.coordinates.grid_coordinate import grid_approx_eq
from frolov.coordinates.pairdistance_coordinate import pairdistance_approx_eq
from frolov.coordinates.perimetric_coordinate import perimetric_approx_eq

from randomgen import random_cartesian_coordinate
from randomgen import random_grid_coordinate


def test_cartesian_to_pairdistance_and_back():
    """
    Check if the 'cartesian_to_pairdistance()' and 'pairdistance_to_cartesian()'
    functions are invertible.

    NOTE: The first time a 4 points in Cartesian3D space are reduced to their relative
    pair distances, information about the system's position and overall orientation in
    space is lost.

    However, the subsequent transformations back and forth between the instances of
    CartesianCoordinate and PairDistanceCoordinate instances should maintain all the
    relevant information.
    """
    cube_sidelen = 1.0

    n_attempts = 1000
    for _ in range(n_attempts):
        init_cartcoord = random_cartesian_coordinate(cube_sidelen)

        original_pairdistcoord = cartesian_to_pairdistance(init_cartcoord)
        original_cartcoord = pairdistance_to_cartesian(original_pairdistcoord)
        recovered_pairdistcoord = cartesian_to_pairdistance(original_cartcoord)
        recovered_cartcoord = pairdistance_to_cartesian(recovered_pairdistcoord)

        assert cartesian_approx_eq(original_cartcoord, recovered_cartcoord)
        assert pairdistance_approx_eq(original_pairdistcoord, recovered_pairdistcoord)


def test_pairdistance_to_perimetric_and_back():
    """
    Check if the 'pairdistance_to_perimetric()' and 'perimetric_to_pairdistance()'
    functions are invertible.
    """
    cube_sidelen = 1.0

    n_attempts = 1000
    for _ in range(n_attempts):
        init_cartcoord = random_cartesian_coordinate(cube_sidelen)

        original_pairdistcoord = cartesian_to_pairdistance(init_cartcoord)
        original_pericoord = pairdistance_to_perimetric(original_pairdistcoord)
        recovered_pairdistcoord = perimetric_to_pairdistance(original_pericoord)
        recovered_pericoord = pairdistance_to_perimetric(recovered_pairdistcoord)

        assert pairdistance_approx_eq(original_pairdistcoord, recovered_pairdistcoord)
        assert perimetric_approx_eq(original_pericoord, recovered_pericoord)


def test_perimetric_to_grid_and_back():
    """
    Check if the 'perimetric_to_grid()' and 'grid_to_perimetric()' functions are
    invertible.
    """

    n_attempts = 1000
    for _ in range(n_attempts):
        original_gridcoord = random_grid_coordinate()
        original_pericoord = grid_to_perimetric(original_gridcoord)
        recovered_gridcoord = perimetric_to_grid(original_pericoord)
        recovered_pericoord = grid_to_perimetric(recovered_gridcoord)

        assert grid_approx_eq(original_gridcoord, recovered_gridcoord)
        assert perimetric_approx_eq(original_pericoord, recovered_pericoord)
