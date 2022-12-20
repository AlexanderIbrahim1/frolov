import pytest

from frolov.coordinates import PerimetricCoordinate
from frolov.grid import GridCoordinate
from frolov.grid import grid_to_perimetric


class TestGridCoordinate:
    def test_basic_functionality(self):
        gc = GridCoordinate(0.1, 0.2, 1.3, 1.4, 0.5, 0.6)

        # make sure everything is set as expected
        assert gc.grid_u1 == pytest.approx(0.1)
        assert gc.grid_u2 == pytest.approx(0.2)
        assert gc.grid_u3 == pytest.approx(1.3)
        assert gc.grid_t3 == pytest.approx(1.4)
        assert gc.grid_s3 == pytest.approx(0.5)
        assert gc.grid_w3 == pytest.approx(0.6)
        
        pc = grid_to_perimetric(gc)
        assert pc.satisfies_inequalities()
