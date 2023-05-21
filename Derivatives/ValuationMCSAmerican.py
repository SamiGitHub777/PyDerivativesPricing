import numpy as np

from Derivatives.GenericValuation import GenericValuation
from Generics.MarketEnvironment import MarketEnvironment
from Simulation.GenericSimulation import GenericSimulation


class ValuationMCSAmerican(GenericValuation):
    ''' Class to value American options with arbitrary payoff by single-factor Monte Carlo simulation.
    '''

    def __init__(self, name, underlying: GenericSimulation, marketEnv: MarketEnvironment, payoffFuc=''):
        super().__init__(name, underlying, marketEnv, payoffFuc)
    def generatePayoff(self, fixed_seed=False):
        try:
            strike = self._strike
        except:
            pass
        paths = self._underlying.getInstrumentValues(fixed_seed=fixed_seed)
        timeGrid = self._underlying.getTimeGrid()
        timeIndexStart = 0
        timeIndexEnd = len(timeGrid) - 1
        try:
            timeIndexStart = int(np.where(timeGrid == self._pricing_date)[0])
            timeIndexEnd = int(np.where(timeGrid == self._maturity)[0])
        except:
            print("Maturity date not in underlying time grid")
        instrumentValues = paths[timeIndexStart:timeIndexEnd + 1]
        try:
            payoff = eval(self._payoff_func)
            return instrumentValues, payoff, timeIndexStart, timeIndexEnd
        except:
            print("Error while evaluating payoff function")


    def presentValue(self, accuracy=6, fixed_seed=False, bf=5, full=False):
        instrumentValues, innerValues, timeIndexStart, timeIndexEnd = self.generatePayoff(fixed_seed=fixed_seed)
        timeList = self._underlying.getTimeGrid()[timeIndexStart:timeIndexEnd+1]
        discountFactors = self._discount_curve.get_discount_factors(timeList, is_dt_objects=True)
        V = innerValues[-1]
        for t in range(len(timeList)-2, 0, -1):
            # relevant discount factor for given time interval
            df = discountFactors[t, 1] / discountFactors[t+1, 1]
            # regression
            rg = np.polyfit(instrumentValues[t], V*df, bf)
            # compute continuation values per path
            C = np.polyval(rg, instrumentValues[t])
            # optimal decision step:
            # if condition satisfied (inner value > regressed continuatuon value)
            # then take inner value; take actual cont. value otherwise
            V = np.where(innerValues[t] > C, innerValues[t], V*df)
        df = discountFactors[0,1] / discountFactors[1, 1]
        result = df * np.sum(V) / len(V)
        if full:
            return round(result, accuracy), df * V
        else:
            return round(result, accuracy)