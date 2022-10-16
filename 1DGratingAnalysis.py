import os
import numpy as np
import scipy.signal as sig
import Functions.Maths as math
import Functions.Organisation as org
from PIL import Image


def readSemLog(file_path):
    '''
    Read .txt file output from SEM image output. Removes $ and \n characters
    from line.
    Args:
        file_path: <string> path to file
    Returns:
        line: <array> array of stripped lines
    '''
    with open(file_path) as infile:
        alllines = infile.readlines()
        lines = [
            (line.translate({ord('$'): None}))[0: -1]
            for line in alllines]
    return lines


def SEMDict(lines):
    '''
    Read lines from SEM output txt file and pulls important parameters into
    dictionary. To further add parameters, simply add names and keys to the
    sample dictionary in this function. Remember FULL_SIZE parameter is [width,
    height].
    Args:
        lines: <array> array of lines from txt file, stripped of '$' and '\n'
    Returns:
        parameterdict: <dict> parameter dictionary
    '''
    parameterdict = {
        'SM_EMI_CURRENT': None,
        'CM_ACCEL_VOLT': None,
        'SM_WD': None,
        'CM_MAG': None,
        'CM_BRIGHTNESS': None,
        'CM_CONTRAST': None,
        'CM_FULL_SIZE': None,
        'SM_MICRON_BAR': None,
        'SM_MICRON_MARKER': None}
    for line in lines:
        splitline = line.split(' ')
        if splitline[0] in parameterdict.keys():
            parameterdict[f'{splitline[0]}'] = splitline[1:]
    return parameterdict


def OpenImgFile(file_path):
    '''
    Loads image file.
    Args:
        file_path: <string> path to file
    Returns:
        image: <object> image file for PIL
    '''
    image = Image.open(file_path)
    return image


def ImageRegionInterest(image,
                        height,
                        width):
    '''
    Trim PIL image to specified region of interest.
    Args:
        image: <object> image file for PIL
        height: <int> number of pixels in vertical axis
        width: <int> number of pixels in horizontal axis
    Returns:
        pixels: <array> pixel array of image
        regionofinterest: <array> trimmed pixel array to region of interest
    '''
    pixels = np.array(image)
    regionofinterest = pixels[0: height, 0: width]
    return pixels, regionofinterest


def DistPix(marker,
            bar):
    '''
    Calaculate the distance each pixel represents in SEM image. Distance is
    set to micrometer scale, i.e. if image file returns um as unit, the scalar
    returns 1, mm is a 1000x more and nm is 1000x less. Pulls data from params
    dictionary and calculates from array. Ensure arguments are individual array
    elements.
    Args:
        marker: <string> SM_MICRON_MARKER string from parameter dictionary
        bar: <string> SM_MICRON_BAR string from parameter dictionary
    Returns:
        distanceperpixel: <float> distance in um per pixel
    '''
    distancedict = {
        'mm': 1E3,
        'um': 1,
        'nm': 1E-3}
    value = int(marker[: -2])
    unit = marker.translate({
        ord('0'): None,
        ord('1'): None,
        ord('2'): None,
        ord('3'): None, 
        ord('4'): None, 
        ord('5'): None,
        ord('6'): None,
        ord('7'): None,
        ord('8'): None,
        ord('9'): None})
    scalar = distancedict[unit]
    distanceperpixel = (value * scalar) / int(bar)
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


def AddDictKeys(primary_dict,
                secondary_dict):
    '''
    Add one dictionary key and values to another dictionary.
    Args:
        primary_dict: <dict> intial dictionary to add keys to
        secondary_dict: <dict> dictionary of keys to add to primary
    Returns:
        primary_dict: <dict> initial dictionary with added keys and values
    '''
    for key, values in secondary_dict.items():
        primary_dict.update({f'{key}': values})
    return primary_dict


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
            lines = readSemLog(file_path=txtpath)
            semParameters = SEMDict(lines=lines)

            imagepath = os.path.join(
                dirpath,
                f'{file[0: -4]}.bmp')
            image = OpenImgFile(file_path=imagepath)

            pixels, roi = ImageRegionInterest(
                image=image,
                height=int(semParameters['CM_FULL_SIZE'][1]),
                width=int(semParameters['CM_FULL_SIZE'][0]))
            distanceperpixel = DistPix(
                marker=semParameters['SM_MICRON_MARKER'][0],
                bar=semParameters['SM_MICRON_BAR'][0])

            periods = []
            frequencies = []
            for i in range(len(roi)):
                fourierfrequencies, fourierperiods = FourierTransformRow(
                    row=roi[i],
                    num_peaks=3,
                    distance_pixel=distanceperpixel)
                periods.append(fourierperiods)
                frequencies.append(fourierfrequencies)

            calculatedGratingProperties = AddDictKeys(
                primary_dict=semParameters,
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

            org.saveJson(
                out_path=os.path.join(
                    dirpath,
                    f'{file[0: -4]}_Results.csv'),
                dictionary=calculatedGratingProperties)

        else:
            pass
