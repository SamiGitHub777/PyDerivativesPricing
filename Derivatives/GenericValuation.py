from Generics.MarketEnvironment import MarketEnvironment
from Generics.NamesEnum import NamesEnum
from Simulation.GenericSimulation import GenericSimulation


class GenericValuation(object):
    '''
    Parent class for single factor valuation
    '''

    def __init__(self, name, underlying: GenericSimulation, marketEnv: MarketEnvironment, payoffFuc=''):
        try:
            self._name = name
            self._pricing_date = marketEnv.getPricingDate()
            try:
                self._strike = marketEnv.getConstant(NamesEnum.STRIKE)
            except:
                pass
            self._maturity = marketEnv.getConstant(NamesEnum.MATURITY)
            self._currency = marketEnv.getConstant(NamesEnum.CURRENCY)
            self._frequency = underlying.getFrequency()  # from simulation obj
            self._paths = underlying.getPaths()
            self._discount_curve = underlying.getDiscountCurve()
            self._payoff_func = payoffFuc
            self._underlying = underlying
            self._underlying.extendSpecialDates([self._pricing_date,
                                                 self._maturity])
        except:
            print('Error while parsing market environement')

    def update(self, initial_value=None, volatility=None, strike=None, maturity=None):
        if initial_value is not None:
            self._underlying.update(initial_value=initial_value)
        if volatility is not None:
            self._underlying.update(volatility=volatility)
        if strike is not None:
            self._strike = strike
        if maturity is not None:
            self._maturity = maturity
            if not maturity in self._underlying.getTimeGrid():
                self._underlying.extendSpecialDates(maturity)
                self._underlying.resetInstrumentValues()

    def delta(self, interval= None, accuracy=4):
        if interval is None:
            interval = self._underlying.getInitialValue() / 50.
        value_left = self.presentValue(fixed_seed=True)
        initial_del = self._underlying.getInitialValue() + interval
        self._underlying.update(initial_value=initial_del)
        value_right = self.presentValue(fixed_seed=True)
        self._underlying.update(initial_value=initial_del - interval)  # reset initial value of udl simulation
        delta = (value_right - value_left) / interval
        # correct for potential numerical errors
        if delta < -1.0:
            return -1.0
        elif delta > 1.0:
            return 1.0
        else:
            return round(delta, accuracy)

    def vega(self, interval=0.01, accuracy=4):
        if interval < self._underlying.getVolatility() / 50.:
            interval = self._underlying.getVolatility() / 50.
        value_left = self.presentValue(fixed_seed=True)
        vola_del = self._underlying.getVolatility() + interval
        # update the simulation object
        self._underlying.update(volatility=vola_del)
        # calculate the right value for numerical Vega
        value_right = self.presentValue(fixed_seed=True)
        # reset volatility value of simulation object
        self._underlying.update(volatility=vola_del - interval)
        vega = (value_right - value_left) / interval
        return round(vega, accuracy)

    def presentValue(self, fixed_seed):
        pass
