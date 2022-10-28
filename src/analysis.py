import math
import numpy as np
import scipy.signal as sig
from src.plotting import multi_xsys_plot, multiy_plot


def mean_array(x):
    '''
    Calculate mean of array.
    Args:
        x: <array> data array
    Returns:
        mean: <float> mean value of x
    '''
    return np.sum(x) / len(x)


def standard_deviation(x):
    '''
    Calculate standard deviation of array.
    Args:
        x: <array> data array
    Returns:
        stdev: <float> standard deviation of x
    '''
    return np.std(x)


def standard_error_mean(x):
    '''
    Standard error of the mean of an array.
    Args:
        x: <array> data array
    Returns:
        SEOM: <float> standard error of the mean of x
    '''
    return np.std(x) / math.sqrt(len(x) - 1)


def standard_quadrature(x,
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


def trim_img_to_roi(image,
                    height,
                    width):
    '''
    Trim pixel array to specific region of interest.
    Args:
        image: <array> array of pixels
        height: <int> number of pixels in vertical axis
        width: <int> number of pixels in horizontal axis
    Returns:
        region_of_interest: <array> trimmed pixel array
    '''
    region_of_interest = image[0: height, 0: width]
    return region_of_interest


def calc_distance_per_pixel(distance_value,
                            distance_unit,
                            number_of_pixels):
    '''
    Calculate distance each pixel represents in SEM image. Distance is set to
    micrometer scale. Pulls data from parameters dictionary and calculates from
    array.
    Args:
        distance_value: <int> distance represented by bar in SEM image
        distance_unit: <string> units of distance marker from SEM image
        number_of_pixels: <string> number of pixels represented by distance mark
    Returns:
        distanceperpixel: <float> distance in um per pixel
    '''
    unit_scalar = {
        'mm': 1E3,
        'um': 1,
        'nm': 1E-3}
    scalar = unit_scalar[distance_unit]
    distanceperpixel = (distance_value * scalar) / int(number_of_pixels)
    return distanceperpixel


def pixel_threshold(raw_row,
                    threshold):
    '''
    Turn analog pixel data in binary signal. Any data above set threshold set to
    maximum pixel value (255), anything below set to 0.
    Args:
        raw_row: <array> pixel values for image row
        threshold: <float/int> pixel value for thresholding
    Returns:
        binary_row: <array> binary row pixel data
    '''
    binary_row = []
    for pixel in raw_row:
        if pixel < threshold:
            binary_row.append(0)
        if pixel >= threshold:
            binary_row.append(255)
    return binary_row


def calc_row_freqs(row):
    '''
    Calculate Fourier transform of image row.
    Args:
        row: <array> pixel values for image row
    Returns:
        sample_size: <int> length of row (sample length)
        frequency_coordinates: <array> frequency space x-axis array
        absolute_intensity: <array> magnitude of pixel data fourier transform
    '''
    sample_size = len(row)
    frequency_coordinates = np.fft.rfftfreq(sample_size, 1)
    frequency_intensities = np.fft.rfft(row)
    absolute_intensity = np.abs(frequency_intensities)
    return sample_size, frequency_coordinates, absolute_intensity


def row_fftsignalprocessing(frequency_coordinates,
                            absolute_intensity,
                            micrometers_per_pixel,
                            sample_size,
                            number_of_frequencies):
    '''
    Process fourier transform of image row to find periods and frequencies.
    Args:
        frequency_coordinates: <array> frequency space x-axis array
        absolute_intensity: <array> magnitude of pixel data fourier transform
        micrometers_per_pixel: <float> distance in um per pixel
        sample_size: <int> length of row (sample length)
        number_of_frequencies: <int> number of peaks to pull from fourier
                                transform (number of periods to analyse)
    Returns:
        frequenies: <array> fourier space frequency values of period peaks
        periods: <array> signal periods from fourier transform in nm
    '''
    peak_locations, _ = sig.find_peaks(x=absolute_intensity)
    prominences, _, _ = sig.peak_prominences(
        x=absolute_intensity,
        peaks=peak_locations)
    prominence_sorted_locations = np.array(
        np.argsort(prominences)[-number_of_frequencies:][::-1])
    selected_peak_locations = peak_locations[prominence_sorted_locations]
    frequency_steps = [
        p / (micrometers_per_pixel * sample_size)
        for p in selected_peak_locations]
    periods = [(1 / f) * 1E3 for f in frequency_steps]
    frequencies = frequency_coordinates[prominence_sorted_locations]
    return frequencies, periods


def calculate_grating_frequency(grating,
                                distance_per_pixel,
                                threshold='None',
                                save_figure=False,
                                figure_outpath=False,
                                file_name=False):
    '''
    Process grating frequency coordinates and periods, average and calculate the
    errors using standard error on the mean. Pull 10 rows and plot the fourier
    transform to ensure the code works as intended, default is not to plot.
    Args:
        grating: <array> pixel array of grating region/analysis region
        distance_per_pixel: <float> distance in um per pixel
        threshold: <string> None - no threshold will be applied
                            Mean - a mean threshold will be applied, anything
                                    above mean will be 255, below 0
                            StdDev - a mean-stddev threshold will be applied,
                                    anything above will be 255, below 0
        save_figure: <bool> if True, saves raw fourier transform (x10) for check
        figure_outpath: <bool/string> if save_figure, figure_outpath is a
                        directory path to save figure out
        file_name: <bool/string> if save_figure, file_name is a name assigned
                    to figure
    Returns:
        results: <dictionary> dictionary containing average period, period
                errors, average frequency coordinates, frequency errors from the
                fourier transform calculation
    '''
    periods = []
    frequencies = []
    frequency_coordinates = []
    absolute_intensities = []
    rows = []
    for index, raw_row in enumerate(grating):
        if threshold == 'Mean':
            row = pixel_threshold(
                raw_row=raw_row,
                threshold=mean_array(x=raw_row))
        elif threshold == 'Mean+StdDev':
            row = pixel_threshold(
                raw_row=raw_row,
                threshold=mean_array(x=raw_row) + standard_deviation(x=raw_row))
        elif threshold == 'Mean-StdDev':
            row = pixel_threshold(
                raw_row=raw_row,
                threshold=mean_array(x=raw_row) - standard_deviation(x=raw_row))
        else:
            row = raw_row
        sample_size, freq_coords, abs_intensity = calc_row_freqs(row=row)
        grating_frequencies, grating_periods = row_fftsignalprocessing(
            frequency_coordinates=freq_coords,
            absolute_intensity=abs_intensity,
            micrometers_per_pixel=distance_per_pixel,
            sample_size=sample_size,
            number_of_frequencies=5)
        periods.append(grating_periods)
        frequencies.append(grating_frequencies)
        if index % (len(grating) / 100):
            frequency_coordinates.append(freq_coords)
            absolute_intensities.append(abs_intensity)
            rows.append(row)

    period_average = [mean_array(x=p) for p in np.array(periods).T]
    period_errors = [standard_error_mean(
        x=p) for p in np.array(periods).T]
    frequency_average = [mean_array(x=f) for f in np.array(frequencies).T]
    frequency_errors = [standard_error_mean(
        x=f) for f in np.array(frequencies).T]

    if save_figure:
        multi_xsys_plot(
            xs=frequency_coordinates,
            ys=absolute_intensities,
            x_label='Frequency',
            y_label='Absolute Intensity',
            title=file_name,
            out_path=figure_outpath[0])
        multiy_plot(
            ys=rows,
            x_label='Pixels',
            y_label='Pixel Intensity',
            title=file_name,
            out_path=figure_outpath[1])

    return {
        'Average_Periods_nm': period_average,
        'Period_Errors_nm': period_errors,
        'Average_Frequencies': frequency_average,
        'Frequencies_Errors': frequency_errors}
