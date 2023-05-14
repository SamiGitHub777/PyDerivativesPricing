import datetime as dt

import matplotlib.pyplot as plt

from Generics.ConstantShortRate import ConstantShortRate
from Generics.MarketEnvironment import MarketEnvironment
from Generics.NamesEnum import NamesEnum
from Simulation.JumpDiffusion import JumpDiffusion

pricingDate = dt.datetime(2023, 1, 1)
finalDate = dt.datetime(2023, 9, 15)
constantShortRate = ConstantShortRate('csr', 0.05)

marketEnv = MarketEnvironment('market_env_jump_diffusion', pricingDate)
marketEnv.addConstant(NamesEnum.INITIAL_VALUE, 100.)
marketEnv.addConstant(NamesEnum.VOLATILITY, 0.2)
marketEnv.addConstant(NamesEnum.FINAL_DATE, finalDate)
marketEnv.addConstant(NamesEnum.CURRENCY, 'EUR')
marketEnv.addConstant(NamesEnum.FREQUENCY, 'M')
marketEnv.addConstant(NamesEnum.PATHS, 10000)
marketEnv.addCurve(NamesEnum.DISCOUNT_CURVE, constantShortRate)
marketEnv.addConstant(NamesEnum.LAMBDA, 0.3)
marketEnv.addConstant(NamesEnum.DELTA, 0.1)
marketEnv.addConstant(NamesEnum.MU, -0.75) # negative jumps


jumpDiffusion = JumpDiffusion('jumpDiffusion', marketEnv)
jumpDiffusion.generateTimeGrid()
paths1 = jumpDiffusion.getInstrumentValues()
print(paths1)
jumpDiffusion.update(lambd=0.8)
paths2 = jumpDiffusion.getInstrumentValues()

plt.figure(figsize=(9, 5))
plot1 = plt.plot(jumpDiffusion.getTimeGrid(), paths1[:, :10], 'g')
plot2 = plt.plot(jumpDiffusion.getTimeGrid(), paths2[:, :10], 'r-.')
legend = plt.legend([plot1[0], plot2[0]], ['low intensity jumps', 'high intensity jumps'], loc=3)
plt.gca().add_artist(legend)
plt.grid(True)
plt.show()
