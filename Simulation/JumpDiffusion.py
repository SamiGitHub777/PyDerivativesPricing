from Generics.MarketEnvironment import MarketEnvironment
from Generics.NamesEnum import NamesEnum
from Simulation.GenericSimulation import GenericSimulation
from Utils.RandomNumberUtils import *


class JumpDiffusion(GenericSimulation):
    # TODO: add sanity checks
    def __init__(self, name, marketEnv: MarketEnvironment, correlated=False):
        super(JumpDiffusion, self).__init__(name, marketEnv, correlated)
        try:
            self._lambd = marketEnv.getConstant(NamesEnum.LAMBDA)
            self._mu = marketEnv.getConstant(NamesEnum.MU)
            self._delta = marketEnv.getConstant(NamesEnum.DELTA)
        except:
            print('Error while parsing market environement')

    def update(self, initial_value=None, volatility=None, lambd=None,
               mu=None, delta=None, final_data=None):
        if initial_value is not None:
            self._initial_value = initial_value
        if volatility is not None:
            self._volatility = volatility
        if lambd is not None:
            self._lambd = lambd
        if mu is not None:
            self._mu = mu
        if delta is not None:
            self._delta = delta
        if final_data is not None:
            self._final_date = final_data
        self._instrument_values = None

    def generatePaths(self, fixed_seed=False, day_count=365.):
        if self._time_grid is None:
            self.generateTimeGrid()
        M = len(self._time_grid)
        I = self._paths
        paths = np.zeros((M, I), dtype=float)
        paths[0] = self._initial_value
        if self._correlated is False:
            sn1 = generateStandardNormalRandom((1, M, I), fixed_seed=fixed_seed)
        else:
            sn1 = self._random_numbers
        sn2 = generateStandardNormalRandom((1, M, I), fixed_seed=fixed_seed)  # for the jump component
        rj = self._lambd * (np.exp(self._mu + 0.5 * self._delta ** 2) - 1)
        shortRate = self._discount_curve.getShortRate()
        for t in range(1, M):
            if not self._correlated:
                ran = sn1[t]
            else:
                ran = np.dot(self._cholesky_matrix, sn1[:, t, :])
                ran = ran[self._rn_set]
            dt = (self._time_grid[t] - self._time_grid[t - 1]).days / day_count
            poisson = np.random.poisson(self._lambd * dt, I)  # for jump component
            paths[t] = paths[t - 1] * (np.exp((shortRate - rj - 0.5 * self._volatility ** 2) * dt
                                              + self._volatility * np.sqrt(dt) * ran)
                                       + (np.exp(self._mu + self._delta *sn2[t]) - 1) * poisson)
        self._instrument_values = paths
