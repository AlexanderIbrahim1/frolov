"""
Create a collection of GridCoordinate instances, transform them to CartesianCoordinate
instances, and visualize the change in the CartesianCoordinate instances as a scatter
plot in 3D.
"""

from __future__ import annotations

from typing import Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from frolov.coordinates.cartesian_coordinate import CartesianCoordinate
from frolov.coordinates.grid_coordinate import GridCoordinate
from frolov.coordinates.pairdistance_coordinate import PairDistanceCoordinate
from frolov.coordinates.perimetric_coordinate import PerimetricCoordinate

from frolov.conversions import cartesian_to_pairdistance
from frolov.conversions import pairdistance_to_cartesian
from frolov.conversions import pairdistance_to_perimetric
from frolov.conversions import perimetric_to_pairdistance
from frolov.conversions import perimetric_to_grid
from frolov.conversions import grid_to_perimetric


class ColorGradientPicker:
    """"""
    RGBAColor = Tuple[float, float, float, float]

    def __init__(self, cmap_name: str, n_colors: int) -> None:
        assert n_colors > 1
        self.cmap = matplotlib.cm.get_cmap(cmap_name)
        self.cmap_normalizer = matplotlib.colors.Normalize(vmin=0.0, vmax=n_colors)

    def get_rgba(self, i_color: int) -> self.RGBAColor:
        color_value = self.cmap_normalizer(i_color)
        color = self.cmap(color_value)

        return color


def grid_to_cartesian(grid_coord: GridCoordinate) -> CartesianCoordinate:
    peri_coord = grid_to_perimetric(grid_coord)
    print(peri_coord)
    pair_coord = perimetric_to_pairdistance(peri_coord)
    print(pair_coord)
    cart_coord = pairdistance_to_cartesian(pair_coord)

    return cart_coord


XYZArrays = Tuple[np.ndarray[4], np.ndarray[4], np.ndarray[4]]
def unwrap_cartesian(cart_coord: CartesianCoordinate) -> XYZArrays:
    xdata = np.array([point[0] for point in cart_coord.unpack()])
    ydata = np.array([point[1] for point in cart_coord.unpack()])
    zdata = np.array([point[2] for point in cart_coord.unpack()])

    return (xdata, ydata, zdata)


def get_grid_coordinates() -> list[GridCoordinate]:
    return [GridCoordinate(1.0, 1.0, 1.0, 1.0, 1.0, x) for x in np.linspace(0.177219044405, 0.9, 11)]

# PLAN:
# - select the path in 'grid' space to create points for



def plot_grid_to_cartesian():
    
    grid_coords = get_grid_coordinates()   # TODO
    cart_coords = [grid_to_cartesian(grid_coord) for grid_coord in grid_coords]

    color_gradient_picker = ColorGradientPicker('viridis', len(cart_coords)-1)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for i_coord, cart_coord in enumerate(cart_coords):
        xdata, ydata, zdata = unwrap_cartesian(cart_coord)
        color = color_gradient_picker.get_rgba(i_coord)
        ax.scatter(xdata, ydata, zdata, marker='o', color=color)

    plt.show()


if __name__ == "__main__":
    plot_grid_to_cartesian()
