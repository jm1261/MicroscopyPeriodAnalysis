import numpy as np
import scipy.signal as sig
import math
import statistics


def calculate_grating_frequencies(grating, distanceperpixel):
    periods = []
    frequencies = []
    for row in grating:
        grating_frequencies, grating_periods = calculate_row_frequencies(
            row=row,
            number_of_frequencies=3,
            micrometers_per_pixel=distanceperpixel)
        periods.append(grating_periods)
        frequencies.append(grating_frequencies)
    periods = np.array(periods).T
    frequencies = np.array(frequencies).T

    period_average = [np.sum(p) / len(p) for p in periods]
    period_errors = [StandardErrorMean(x=p) for p in periods]
    frequency_average = [np.sum(f) / len(f) for f in frequencies]
    frequency_errors = [StandardErrorMean(x=f) for f in frequencies]

    return {
        'Average_Periods_nm': period_average,
        'Period_Errors_nm': period_errors,
        'Average_Frequencies': frequency_average,
        'Frequencies_Errors': frequency_errors}


def calculate_row_frequencies(row,
                          number_of_frequencies,
                          micrometers_per_pixel):
    '''
    Calculate fourier transform of image row.
    Args:
        row: <array> pixel values for image row
        number_of_frequencies: <int> number of peaks to pull from fourier transform (number
                    of periods to analyse)
        micrometers_per_pixel: <float> distance in um per pixel
    Returns:
        frequencies: <array> fourier space frequency values of period peaks
        periods: <array> signal periods from fourier transform converted from um
                    to nm
    '''
    frequency_intensities = np.fft.rfft(row)
    absolute_frequency_intensities = np.abs(frequency_intensities)

    peak_locations, _ = sig.find_peaks(x=absolute_frequency_intensities)
    prominences, _, _ = sig.peak_prominences(
        x=absolute_frequency_intensities,
        peaks=peak_locations)
    locations_sorted_by_prominence = np.array(
        np.argsort(prominences)[-number_of_frequencies:][::-1])
    selected_peak_locations = peak_locations[locations_sorted_by_prominence]

    samplesize = len(row)
    frequency_coordinates = np.fft.rfftfreq(samplesize, 1)
    frequencies = frequency_coordinates[locations_sorted_by_prominence]

    frequency_steps = [p / (micrometers_per_pixel * samplesize)
                       for p in selected_peak_locations]
    periods = [(1 / f) * 1E3 for f in frequency_steps]

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
