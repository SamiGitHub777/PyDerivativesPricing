
class MarketEnvironment(object):
    '''
    Class to store constant parameters, lists of objects, curves
    Stores :
        initial_value : Constant
            Mandatory
            initial value of the process at pricing_date
        volatility : Constant
            Mandatory
            vol coeff of the process
        final_date : Constant
            Mandatory
            simulation end date
        currency : Constant
            Mandatory
            Currenty of the financial instrument
        frequency : Constant
            Mandatory
            pandas freq date_range parameter
        paths : Constant
            Mandatory
            number of paths to be simulated
        discount_curve : Curve
            Mandatory
            instance of ConstantShortRate
        time_grid : List
            Not mandatory
            time grid of relevant dates (in portfolio context)
        random_numbers: List
            Not mandatory
            random number array (in case of correlated objects)
        cholesky_matrix : List
            Not mandatory
            Cholesky matrix for (in case of correlated objects)
        rn_set : List
            Not mandatory
            dict object with pointer to relevant random number set
    '''

    def __init__(self, name, pricing_date):
        self.__name = name
        self.__pricing_date = pricing_date
        self.__curves = {}
        self.__lists = {}
        self.__constants = {}

    def getName(self):
        return self.__name

    def getPricingDate(self):
        return self.__pricing_date

    def addCurve(self, key, curve):
        self.__curves[key] = curve

    def getCurve(self, key):
        return self.__curves[key]

    def getCurves(self):
        return self.__curves

    def addList(self, key, list):
        self.__lists[key] = list

    def getList(self, key):
        return self.__lists[key]

    def getLists(self):
        return self.__lists

    def addConstant(self, key, constant):
        self.__constants[key] = constant

    def getConstant(self, key):
        return self.__constants[key]

    def getConstants(self):
        return self.__constants

    def overwriteEnv(self, env):
        for key in env.getCurves():
            self.__curves[key] = env.getCurve(key)
        for key in env.getLists():
            self.__curves[key] = env.getList(key)
        for key in env.getConstants():
            self.__curves[key] = env.getConstant(key)



