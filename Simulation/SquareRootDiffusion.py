from Generics.MarketEnvironment import MarketEnvironment
from Generics.NamesEnum import NamesEnum
from Simulation.GenericSimulation import GenericSimulation
from Utils.RandomNumberUtils import *

class SquareRootDiffusion(GenericSimulation):
    # TODO: add sanity checks
    def __init__(self, name, marketEnv: MarketEnvironment, correlated=False):
        super(SquareRootDiffusion, self).__init__(name, marketEnv, correlated)
        try:
            self._kappa = marketEnv.getConstant(NamesEnum.KAPPA)
            self._theta = marketEnv.getConstant(NamesEnum.THETA)
        except:
            print('Error while parsing market environement')

    def update(self, initial_value=None, volatility=None, kappa=None, theta=None, final_date=None):
        if initial_value is not None:
            self._initial_value = initial_value
        if volatility is not None:
            self._volatility = volatility
        if kappa is not None:
            self._kappa = kappa
        if theta is not None:
            self._theta = theta
        if final_date is not None:
            self._final_date = final_date
        self._instrument_values = None

    def generatePaths(self, fixed_seed=True, day_count=365.):
        if self._time_grid is None:
            self.generateTimeGrid()
        M = len(self._time_grid)
        I = self._paths
        paths = np.zeros((M, I))
        paths_ = np.zeros_like(paths)
        paths[0] = self._initial_value
        paths_[0] = self._initial_value
        if self._correlated is False:
            rand = generateStandardNormalRandom((1, M, I),
                                     fixed_seed=fixed_seed)
        else:
            rand = self._random_numbers
        for t in range(1, M):
            dt = (self._time_grid[t] - self._time_grid[t - 1]).days / day_count
            if self._correlated is False:
                ran = rand[t]
            else:
                ran = np.dot(self._cholesky_matrix, rand[:, t, :])
                ran = ran[self._rn_set]
            paths_[t] = (paths_[t - 1] + self._kappa
                         * (self._theta - np.maximum(0, paths_[t - 1, :])) * dt
                         + np.sqrt(np.maximum(0, paths_[t - 1, :]))
                         * self._volatility * np.sqrt(dt) * ran)
            paths[t] = np.maximum(0, paths_[t])
        self._instrument_values = paths