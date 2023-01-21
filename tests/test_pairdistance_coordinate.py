import pytest


from frolov.coordinates.pairdistance_coordinate import PairDistanceCoordinate


class TestPairDistanceCoordinate:
    def test_basic_functionality(self):
        pd = PairDistanceCoordinate(1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

        # make sure everything is set as expected
        assert pd.r01 == pytest.approx(1.0)
        assert pd.r02 == pytest.approx(2.0)
        assert pd.r03 == pytest.approx(3.0)
        assert pd.r12 == pytest.approx(4.0)
        assert pd.r13 == pytest.approx(5.0)
        assert pd.r23 == pytest.approx(6.0)

    @pytest.mark.parametrize("index", range(6))
    def test_raises_negative_value(self, index):
        sidelengths = [0.1, 0.2, 1.3, 1.4, 1.1, 0.6]
        sidelengths[index] = -1.0

        with pytest.raises(AssertionError):
            PairDistanceCoordinate(*sidelengths)
