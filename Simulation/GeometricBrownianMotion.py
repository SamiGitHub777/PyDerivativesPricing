from Generics.MarketEnvironment import MarketEnvironment
from Simulation.GenericSimulation import GenericSimulation
from Utils.RandomNumberUtils import *


class GeometricBrownianMotion(GenericSimulation):

    def __init__(self, name, marketEnv: MarketEnvironment, correlated=False):
        super(GeometricBrownianMotion, self).__init__(name, marketEnv, correlated)

    def generatePaths(self, fixed_seed=False, day_count=365.):
        if self._time_grid is None:
            self.generateTimeGrid()  # base class method

        M = len(self._time_grid)
        I = self._paths
        paths = np.zeros((M, I))
        paths[0] = self._initial_value
        if not self._correlated:
            rand = generateStandardNormalRandom((1, M, I), fixed_seed=fixed_seed)
        else:
            rand = self._random_numbers
        shortRate = self._discount_curve.getShortRate()
        for t in range(1, M):
            if not self._correlated:
                ran = rand[t]
            else:
                ran = np.dot(self._cholesky_matrix, rand[:, t, :])
                ran = ran[self._rn_set]
            dt = (self._time_grid[t] - self._time_grid[t - 1]).days / day_count
            paths[t] = paths[t - 1] * np.exp((shortRate - 0.5 * self._volatility ** 2) * dt +
                                             self._volatility * np.sqrt(dt) * ran)

        self._instrument_values = paths

    def update(self, initial_value=None, volatility=None, final_date=None):
        if initial_value is not None:
            self._initial_value = initial_value
        if volatility is not None:
            self._volatility = volatility
        if final_date is not None:
            self._final_date = final_date
        self._instrument_values = None