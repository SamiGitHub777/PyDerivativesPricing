# from enum import StrEnum
# from enum import auto
from strenum import StrEnum


class NamesEnum(StrEnum):
    INITIAL_VALUE = 'initial_value'  # auto()
    VOLATILITY = 'volatility',
    FINAL_DATE = 'final_date',
    CURRENCY = 'currency',
    FREQUENCY = 'frequency',
    PATHS = 'paths',
    DISCOUNT_CURVE = 'discount_factor',
    TIME_GRID = 'time_grid',
    SPECIAL_DATES = 'special_dates',
    CHOLESKY_MATRIX = 'cholesky_matrix',
    RANDOM_NUMBERS = 'random_numbers',
    LAMBDA = 'lambda',  # Poisson
    MU = 'mu',  # jump diffusion
    DELTA = 'delta', # jump diffusion
    KAPPA='kappa', # square root diffusion
    THETA='theta', # square root diffusion
    STRIKE='strike',
    MATURITY='maturity',
    RN_SET = 'rn_set'
