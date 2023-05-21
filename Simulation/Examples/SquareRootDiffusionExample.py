import datetime as dt

import matplotlib.pyplot as plt

from Generics.ConstantShortRate import ConstantShortRate
from Generics.MarketEnvironment import MarketEnvironment
from Generics.NamesEnum import NamesEnum
from Simulation.SquareRootDiffusion import SquareRootDiffusion

pricingDate = dt.datetime(2023, 1, 1)
finalDate = dt.datetime(2023, 9, 15)
constantShortRate = ConstantShortRate('csr', 0.05)

marketEnv = MarketEnvironment('market_env_square_root_diffusion', pricingDate)
marketEnv.addConstant(NamesEnum.INITIAL_VALUE, 0.26)
marketEnv.addConstant(NamesEnum.VOLATILITY, 0.2)
marketEnv.addConstant(NamesEnum.FINAL_DATE, finalDate)
marketEnv.addConstant(NamesEnum.CURRENCY, 'EUR')
marketEnv.addConstant(NamesEnum.FREQUENCY, 'M')
marketEnv.addConstant(NamesEnum.PATHS, 10000)
marketEnv.addConstant(NamesEnum.KAPPA, 4.)
marketEnv.addConstant(NamesEnum.THETA, 0.18)
marketEnv.addCurve(NamesEnum.DISCOUNT_CURVE, constantShortRate)


squareRootDiffusion = SquareRootDiffusion('squareRootDiffusion', marketEnv)
squareRootDiffusion.generateTimeGrid()
paths1 = squareRootDiffusion.getInstrumentValues()
print(paths1)

plt.figure(figsize=(9, 5))
plt.plot(squareRootDiffusion.getTimeGrid(), paths1[:, :10])
plt.axhline(marketEnv.getConstant(NamesEnum.THETA), color='r', ls='--', lw=2.0)
plt.grid(True)
plt.show()
