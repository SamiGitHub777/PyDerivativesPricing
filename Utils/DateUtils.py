import numpy as np


def get_year_deltas(date_list, year_nb_days=365.):
    '''

    :param date_list: list or array
        collection of datetime objects
    :param year_nb_days: floar
        number od days in a year
    :return: array
        year fractions
    '''
    return np.array([(date - date_list[0]).days / year_nb_days
                     for date in date_list])
