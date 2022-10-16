from PIL import Image
import json
import numpy as np


def read_sem_log(file_path):
    '''
    Load JEOL-SEM txt file as a dictionary of key parameters

    Args:
        file_path: <string> path to file
    Returns:
        parameterdict: <dict> parameter dictionary
    '''
    with open(file_path) as infile:
        raw_lines = infile.readlines()
    sanitized_lines = remove_unwanted_characters(raw_lines)
    JEOL_parameters = lines_to_parameters(sanitized_lines)
    sanitized_parameters = sanitize_JEOL_parameters(JEOL_parameters)
    return sanitized_parameters


def remove_unwanted_characters(raw_lines):
    '''
    Remove $ and \n characters from lines
    '''
    lines = [
        (line.translate({ord('$'): None}))[0: -1]
        for line in raw_lines]
    return lines


def lines_to_parameters(lines):
    '''
    Pull important parameters into dictionary. 
    To further add parameters, simply add names and keys to the sample dictionary in this function. 
    Remember FULL_SIZE parameter is [width, height].

    Args:
        lines: <array> array of lines from txt file, stripped of '$' and '\n'
    Returns:
        parameterdict: <dict> parameter dictionary
    '''
    parameters = dict()
    for line in lines:
        parameter_label, *parameter_values = line.split(' ')
        parameters[parameter_label] = parameter_values
    return parameters


def sanitize_JEOL_parameters(raw_parameters):

    parameter_map = {
        'CM_ACCEL_VOLT': 'acceleration_voltage',
        'CM_BRIGHTNESS': 'brightness',
        'CM_CONTRAST': 'contrast',
        'CM_MAG': 'magnification',
        'SM_EMI_CURRENT': 'emission_current',
        'SM_MICRON_BAR': 'calibration_number_of_pixels',
        'SM_MICRON_MARKER': 'calibration_distance',
        'SM_WD': 'working_distance',
    }
    sanitized_parameters = dict()
    for key, value in parameter_map.items():
        sanitized_parameters[value] = raw_parameters[key]

    # CM_FULL_SIZE is [width, height].
    sanitized_parameters['width'], sanitized_parameters['height'] = raw_parameters['CM_FULL_SIZE']
    return sanitized_parameters


def read_image(file_path):
    '''
    Loads image file.
    Args:
        file_path: <string> path to file
    Returns:
        image: <np.array> array of pixels
    '''
    image = Image.open(file_path)
    return np.array(image)


def save_json(out_path,
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
