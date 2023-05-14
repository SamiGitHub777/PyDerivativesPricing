import datetime as dt

import matplotlib.pyplot as plt

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
paths1 = geometricBrownianMotion.getInstrumentValues()
print(paths1)
geometricBrownianMotion.update(volatility=0.5)
paths2 = geometricBrownianMotion.getInstrumentValues()

plt.figure(figsize=(9, 5))
plot1 = plt.plot(geometricBrownianMotion.getTimeGrid(), paths1[:, :10], 'g')
plot2 = plt.plot(geometricBrownianMotion.getTimeGrid(), paths2[:, :10], 'r-.')
legend = plt.legend([plot1[0], plot2[0]], ['low vol', 'high vol'], loc=3)
plt.gca().add_artist(legend)
plt.grid(True)
plt.show()
