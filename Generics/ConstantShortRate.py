import numpy as np

from Utils import DateUtils


class ConstantShortRate(object):
    def __init__(self, name, short_rate):
        '''
        :param name: string
            object's name
        :param short_rate: float > 0
            constant rate for discounting
        '''
        self.__name = name
        self.__short_rate = short_rate
        if short_rate < 0:
            raise ValueError('Short rate is negative.')



    def get_discount_factors(self, date_list, is_dt_objects=True):
        '''

        :param date_list: list/array
            of datetime object or year fractions
        :param is_dt_objects: relevant to date_list type
        :return: array
            discount factors
        '''
        if is_dt_objects:
            dt_list = DateUtils.get_year_deltas(date_list)
        else:
            dt_list = np.array(date_list)
        df_list = np.exp(self.__short_rate * np.sort(-dt_list))
        return np.array((date_list, df_list)).T

    def getShortRate(self):
        return self.__short_rate

    def setShortRate(self, shortRate):
        self.__short_rate = shortRate

    def getName(self):
        return self.__name

    def __str__(self):
        return f'Constant Short Rate : {self.__name} value is {self.__short_rate}'