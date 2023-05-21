
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

from Derivatives.OptionStatsPlot import plotOptionStats
from Derivatives.ValuationMCSEuropean import ValuationMCSEuropean
from Generics.ConstantShortRate import ConstantShortRate
from Generics.MarketEnvironment import MarketEnvironment
from Generics.NamesEnum import NamesEnum
from Simulation.GeometricBrownianMotion import GeometricBrownianMotion

pricingDate = dt.datetime(2023, 1, 1)
finalDate = dt.datetime(2023, 9, 15)
constantShortRate = ConstantShortRate('csr', 0.05)

marketEnv = MarketEnvironment('my_market_env', pricingDate)
marketEnv.addConstant(NamesEnum.INITIAL_VALUE, 100.)
marketEnv.addConstant(NamesEnum.VOLATILITY, 0.2)
marketEnv.addConstant(NamesEnum.FINAL_DATE, finalDate)
marketEnv.addConstant(NamesEnum.CURRENCY, 'EUR')
marketEnv.addConstant(NamesEnum.FREQUENCY, 'M')
marketEnv.addConstant(NamesEnum.PATHS, 10000)
marketEnv.addCurve(NamesEnum.DISCOUNT_CURVE, constantShortRate)

geometricBrownianMotion = GeometricBrownianMotion('gbm', marketEnv)
geometricBrownianMotion.generateTimeGrid()
paths = geometricBrownianMotion.getInstrumentValues()

marketEnvCall = MarketEnvironment('market_env_call', pricingDate)
marketEnvCall.addConstant(NamesEnum.STRIKE, 110.)
marketEnvCall.addConstant(NamesEnum.MATURITY, dt.datetime(2023, 9, 15))
marketEnvCall.addConstant(NamesEnum.CURRENCY, 'EUR')

payoffFunc = 'np.maximum(maturityValue - strike, 0)'
eurCall = ValuationMCSEuropean(name='eurCall', underlying=geometricBrownianMotion, marketEnv=marketEnvCall, payoffFuc=payoffFunc)
print(f'European Call price {eurCall.presentValue()}')
print(f'European Call delta {eurCall.delta()}')
print(f'European Call vega {eurCall.vega()}')

s_list = np.arange(80., 150., 2.)
p_list = []; d_list = []; v_list = []
for s in s_list:
    eurCall.update(initial_value=s)
    p_list.append(eurCall.presentValue(fixed_seed=True))
    d_list.append(eurCall.delta())
    v_list.append(eurCall.vega())

plotOptionStats(s_list, p_list, d_list, v_list)