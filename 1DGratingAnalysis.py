import os
import numpy as np
import scipy.signal as sig
import Functions.Maths as math
import Functions.Organisation as org
import src.fileIO as fileIO


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


def dictionary_union(primary_dict,
                secondary_dict):
    '''
    Add one dictionary key and values to another dictionary.
    Args:
        primary_dict: <dict> intial dictionary to add keys to
        secondary_dict: <dict> dictionary of keys to add to primary
    Returns:
        primary_dict: <dict> initial dictionary with added keys and values
    '''
    return dict(primary_dict, **secondary_dict)


if __name__ == '__main__':

    ''' Organisation '''
    root = os.getcwd()
    rootpath = os.path.join(
        root,
        'TestImage')
    dirpath = org.FindThePath(
        default=rootpath,
        title='Select Target Directory',
        dir_path=True)
    txtfiles, imagefiles = org.FindDirFile(
        dir_path=dirpath,
        file_string='.txt',
        image_string='.bmp')

    for file in txtfiles:

        if f'{file[0: -4]}.bmp' in imagefiles:
            print(file)
            txtpath = os.path.join(
                dirpath,
                file)

            sem_parameters = fileIO.read_sem_log(file_path=txtpath)

            imagepath = os.path.join(
                dirpath,
                f'{file[0: -4]}.bmp')

            image = fileIO.read_image(file_path=imagepath)

            grating_region = trim_to_region_of_interest(
                image=image,
                height=sem_parameters['image_height'],
                width=sem_parameters['image_width'])
            distanceperpixel = calculate_distanceperpixel(
                distance_value=sem_parameters['calibration_distance_value'],
                distance_unit=sem_parameters['calibration_distance_unit'],
                number_of_pixels=sem_parameters['calibration_number_of_pixels'])

            periods = []
            frequencies = []
            for i in range(len(grating_region)):
                fourierfrequencies, fourierperiods = FourierTransformRow(
                    row=grating_region[i],
                    num_peaks=3,
                    distance_pixel=distanceperpixel)
                periods.append(fourierperiods)
                frequencies.append(fourierfrequencies)

            calculated_grating_properties = dictionary_union(
                primary_dict=sem_parameters,
                secondary_dict={
                    'Average_Periods_nm': [
                        np.sum(p) / len(p)
                        for p in np.array(periods).T],
                    'Period_Errors_nm': [
                        math.StandardErrorMean(x=p)
                        for p in np.array(periods).T],
                    'Average_Frequencies': [
                        np.sum(f) / len(f)
                        for f in np.array(frequencies).T],
                    'Frequencies_Errors': [
                        math.StandardErrorMean(x=f)
                        for f in np.array(frequencies).T]})

            fileIO.save_json(
                out_path=os.path.join(
                    dirpath,
                    f'{file[0: -4]}_Results.json'),
                dictionary=calculated_grating_properties)

        else:
            pass
