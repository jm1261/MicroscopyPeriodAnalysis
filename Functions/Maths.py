import math
import statistics


def StandardDeviation(x):
    '''
    Calculate standard deviation of array.
    Args:
        x: <array> data array
    Returns:
        stdev: <float> standard deviation of x
    '''
    return statistics.stdev(x)


def StandardErrorMean(x):
    '''
    Standard error of the mean of an array.
    Args:
        x: <array> data array
    Returns:
        SEOM: <float> standard error of the mean of x
    '''
    return statistics.stdev(x) / math.sqrt(len(x) - 1)


def QuadratureError(x,
                    y,
                    z,
                    delta_x,
                    delta_y):
    '''
    Quadrature error for z array, calculated from x and y.
    Args:
        x: <array> x-data array
        y: <array> y-data array
        z: <array> z-data array
        delta_x: <array> error x-data array
        delta_y: <array> error y-data array
    Returns:
        delta_z: <array> error z-data array
    '''
    deltaz = z * math.sqrt(((delta_x / x) ** 2) + ((delta_y / y) ** 2))
    return deltaz
