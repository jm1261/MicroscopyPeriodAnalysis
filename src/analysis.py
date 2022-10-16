import numpy as np
import scipy.signal as sig
import math
import statistics


def FourierTransformRow(row,
                        num_peaks,
                        distance_pixel):
    '''
    Calculate fourier transform of image row.
    Args:
        row: <array> pixel values for image row
        num_peaks: <int> number of peaks to pull from fourier transform (number
                    of periods to analyse)
        distance_pixel: <float> distance in um per pixel
    Returns:
        frequencies: <array> fourier space frequency values of period peaks
        periods: <array> signal periods from fourier transform converted from um
                    to nm
    '''
    samplesize = len(row)
    xspace = range(0, samplesize, 1)
    fspace = np.fft.rfftfreq(len(xspace), 1)
    fft = np.fft.rfft(row)
    magnitude = np.abs(fft)
    peaks, _ = sig.find_peaks(x=magnitude)
    prominences, _, _ = sig.peak_prominences(
        x=magnitude,
        peaks=peaks)
    indices = np.array(np.argsort(prominences)[-num_peaks:][::-1])
    periodpeaks = peaks[indices]
    fsteps = [p / (distance_pixel * samplesize) for p in periodpeaks]
    periods = [(1 / f) * 1E3 for f in fsteps]
    frequencies = fspace[indices]
    return frequencies, periods

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


def calculate_distanceperpixel(distance_value, distance_unit, number_of_pixels):
    '''
    Calaculate the distance each pixel represents in SEM image. Distance is
    set to micrometer scale, i.e. if image file returns um as unit, the scalar
    returns 1, mm is a 1000x more and nm is 1000x less. Pulls data from params
    dictionary and calculates from array. Ensure arguments are individual array
    elements.
    Args:
        distance: <string> of the form '123nm'
        number_of_pixels: <int>
    Returns:
        distanceperpixel: <float> distance in um per pixel
    '''
    unit_scalar_map = {
        'mm': 1E3,
        'um': 1,
        'nm': 1E-3}
    scalar = unit_scalar_map[distance_unit]
    distanceperpixel = (distance_value * scalar) / int(number_of_pixels)
    return distanceperpixel

def trim_to_region_of_interest(image,
                               height,
                               width):
    '''
    Trim numpy array to specified region of interest.
    Args:
        image: <np.array> array of pixels
        height: <int> number of pixels in vertical axis
        width: <int> number of pixels in horizontal axis
    Returns:
        pixels: <array> pixel array of image
        regionofinterest: <array> trimmed pixel array to region of interest
    '''
    region_of_interest = image[0: height, 0: width]
    return region_of_interest