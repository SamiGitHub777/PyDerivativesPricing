
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

from Derivatives.OptionStatsPlot import plotOptionStats
from Derivatives.ValuationMCSAmerican import ValuationMCSAmerican
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
marketEnv.addConstant(NamesEnum.PATHS, 30000)
marketEnv.addCurve(NamesEnum.DISCOUNT_CURVE, constantShortRate)

geometricBrownianMotion = GeometricBrownianMotion('gbm', marketEnv)
geometricBrownianMotion.generateTimeGrid()
paths = geometricBrownianMotion.getInstrumentValues()

marketEnvCallAmerican = MarketEnvironment('market_env_call_american', pricingDate)
marketEnvCallAmerican.addConstant(NamesEnum.STRIKE, 110.)
marketEnvCallAmerican.addConstant(NamesEnum.MATURITY, dt.datetime(2023, 9, 15))
marketEnvCallAmerican.addConstant(NamesEnum.CURRENCY, 'EUR')

payoffFunc = 'np.maximum(instrumentValues - strike, 0)'
americanCall = ValuationMCSAmerican(name='americanCall', underlying=geometricBrownianMotion, marketEnv=marketEnvCallAmerican, payoffFuc=payoffFunc)
print(f'American Call price {americanCall.presentValue()}')
print(f'American Call delta {americanCall.delta()}')
print(f'American Call vega {americanCall.vega()}')

s_list = np.arange(100., 120., 2.)
p_list = []; d_list = []; v_list = []
for s in s_list:
    americanCall.update(initial_value=s)
    p_list.append(americanCall.presentValue(fixed_seed=True))
    d_list.append(americanCall.delta())
    v_list.append(americanCall.vega())

plotOptionStats(s_list, p_list, d_list, v_list)