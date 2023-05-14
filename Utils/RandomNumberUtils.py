import numpy as np


def generateStandardNormalRandom(shape: tuple, fixed_seed=True, moment_match=True, antithetic=True):
    '''
    :param shape: tuple
    :param fixed_seed: boolean
        fix the seed
    :param moment_match: boolean
        first and second moment matching
    :param antithetic: boolean
        generate antithetic variates

    :return: array
        of shape shape pseudo random numbers
    '''
    if fixed_seed:
        np.random.seed(10000)
    first, second, third = shape
    if antithetic:
        res = np.random.standard_normal((first, second, int(third / 2)))
        res = np.concatenate((res, -res), axis=2)
    else:
        res = np.random.standard_normal(shape)
    if moment_match:
        res = res - np.mean(res)
        res = res / np.std(res)
    if shape[0] == 1:
        return res[0]
    else:
        return res
