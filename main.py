import datetime as dt
from Utils import DateUtils
from Generics import MarketEnvironment, ConstantShortRate
from Utils import RandomNumberUtils
dates = [dt.datetime(2023,1,1), dt.datetime(2023,3,31), dt.datetime(2023,6,30)]
print(DateUtils.get_year_deltas(dates))

constant_short_rate = ConstantShortRate.ConstantShortRate('csr', 0.01)
print(constant_short_rate.get_discount_factors(dates))

me = MarketEnvironment.MarketEnvironment('me_1', dt.datetime(2023, 1, 1))
me.addCurve('csr', constant_short_rate)

print(me.getCurves()['csr'])

constant_short_rate.setShortRate(0.2)

print(me.getCurves()['csr'])
print(RandomNumberUtils.generateStandardNormalRandom((2, 2, 3), fixed_seed=True, moment_match=False, antithetic=False))
