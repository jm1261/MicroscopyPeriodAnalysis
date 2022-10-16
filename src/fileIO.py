from PIL import Image
import json
import numpy as np


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


def OpenImgFile(file_path):
    '''
    Loads image file.
    Args:
        file_path: <string> path to file
    Returns:
        image: <np.array> array of pixels
    '''
    image = Image.open(file_path)
    return np.array(image)

def saveJson(out_path,
            dictionary):
    '''
    Save dictionary to json file.
    Args:
        out_path: <string> path to file, including file name and extension
        dictionary: <dict> python dictionary to save out
    Returns:
        None
    '''
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')


def convert(o):
    '''
    Check type of data string
    '''
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError