import numpy as np
import pandas as pd
from Generics import MarketEnvironment
from Generics.NamesEnum import NamesEnum


class GenericSimulation(object):

    #TODO : add sanity checks
    def __init__(self, name: str, marketEnv: MarketEnvironment, correlated: bool):
        try:
            self._name = name
            self._pricing_date = marketEnv.getPricingDate()
            self._initial_value = marketEnv.getConstant(NamesEnum.INITIAL_VALUE)
            self._volatility = marketEnv.getConstant(NamesEnum.VOLATILITY)
            self._final_date = marketEnv.getConstant(NamesEnum.FINAL_DATE)
            self._frequency = marketEnv.getConstant(
                NamesEnum.FREQUENCY)  # pandas date_range : 'B' for Business Day, 'W' for Weekly, 'M' for Monthly
            self._currency = marketEnv.getConstant(NamesEnum.CURRENCY)
            self._paths = marketEnv.getConstant(NamesEnum.PATHS)
            self._discount_curve = marketEnv.getCurve(NamesEnum.DISCOUNT_CURVE)
            try:
                self._special_dates = marketEnv.getList(NamesEnum.SPECIAL_DATES)
            except:
                self._special_dates = None
            try:
                self._time_grid = marketEnv.getList(NamesEnum.TIME_GRID)
            except:
                self._time_grid = None
            self._instrument_values = None
            self._correlated = correlated
            # risky factors correlated
            if correlated:
                self._cholesky_matrix = marketEnv.getList(NamesEnum.CHOLESKY_MATRIX)
                self._rn_set = marketEnv.getList(NamesEnum.RN_SET)[self._name]
                self._random_numbers = marketEnv.getList(NamesEnum.RANDOM_NUMBERS)
        except:
            print('Error while parsing market environement')

    def generateTimeGrid(self):
        start = self._pricing_date
        end = self._final_date
        time_grid = list(pd.date_range(start=start, end=end, freq=self._frequency).to_pydatetime())
        if start not in time_grid:
            time_grid.insert(0, start)
        if end not in time_grid:
            time_grid.append(end)
        if self._special_dates is not None and len(self._special_dates) > 0:
            time_grid.extend(self._special_dates)
            time_grid = list(set(time_grid))
            time_grid.sort()
        self._time_grid = np.array(time_grid)

    def getInstrumentValues(self, fixed_seed=True):
        if self._instrument_values is None:
            # only initiate simulation
            self.generatePaths(fixed_seed=fixed_seed, day_count=365.)
        elif fixed_seed is False:
            # also initiate resimulation when fixed_seed is False
            self.generatePaths(fixed_seed=fixed_seed, day_count=365.)
        return self._instrument_values

    def getTimeGrid(self):
        return self._time_grid
