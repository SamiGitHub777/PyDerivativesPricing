from Derivatives.GenericValuation import GenericValuation
import numpy as np

from Generics.MarketEnvironment import MarketEnvironment
from Simulation.GenericSimulation import GenericSimulation


class ValuationMCSEuropean(GenericValuation):
    '''
    Class to value European options with arbitrary payoff by single-factor Monte Carlo simulation.
    '''

    def __init__(self, name, underlying: GenericSimulation, marketEnv: MarketEnvironment, payoffFuc=''):
        super().__init__(name, underlying, marketEnv, payoffFuc)
    def generatePayoff(self, fixed_seed=False):
        try:
            strike = self._strike
        except:
            pass
        paths = self._underlying.getInstrumentValues(fixed_seed=
                                                     fixed_seed)
        timeGrid = self._underlying.getTimeGrid()
        timeIndex = len(timeGrid) - 1
        try:
            timeIndex = np.where(timeGrid == self._maturity)[0]
            timeIndex = int(timeIndex)
        except:
            print('Maturity date is not in the underlying time grid')
        maturityValue = paths[timeIndex]
        # for asian (lookback)
        meanValue = np.mean(paths[:timeIndex], axis=1)
        maxValue = np.amax(paths[:timeIndex], axis=1)[-1]
        minValue = np.amin(paths[:timeIndex], axis=1)[-1]
        try:
            payoff = eval(self._payoff_func)
            return payoff
        except:
            print('Error while evaluating payoff function')

    def presentValue(self, accuracy=6, fixed_seed=False, full=False):
        cashFlow = self.generatePayoff(fixed_seed=fixed_seed)
        discountFactor = self._discount_curve.get_discount_factors((self._pricing_date, self._maturity))[0, 1]
        result = discountFactor * np.sum(cashFlow) / len(cashFlow)
        if full:
            return round(result, accuracy), discountFactor*cashFlow
        else:
            return round(result, accuracy)