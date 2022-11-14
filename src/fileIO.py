import json
import numpy as np
from PIL import Image


def load_json(file_path):
    '''
    Extract user variables from json dictionary.
    Args:
        file_path: <string> path to file
    Returns:
        dictionary: <dict> use variables dictionary
    '''
    with open(file_path, 'r') as file:
        return json.load(file)


def remove_unwanted(all_lines,
                    unwanted_character):
    '''
    Remove unwanted characters from lines, removes hidden newline characters.
    Args:
        all_lines: <array> read lines
        unwanted_character: <string> characters to remove
    Return:
        lines: <array> lines with characters and newline characters removed
    '''
    lines = [
        (line.translate({ord(unwanted_character): None}))[0: -1]
        for line in all_lines]
    return lines


def lines_to_parameters(lines):
    '''
    Pull important parameters into dictionary.
    Args:
        lines: <array> array of lines from txt file, stripped of '$' and \n
    Returns:
        parameters: <dict> parameter dictionary
    '''
    parameters = dict()
    for line in lines:
        parameter_label, *parameter_values = line.strip().split(' ')
        parameters[parameter_label] = parameter_values
    return parameters


def desired_JEOL_parameters(all_parameters):
    '''
    Pull important parameters into dictionary. Add more parameters by adding
    names and keys to the dictionary in this function.
    Args:
        all_parameters: <dict> dictionary of all parameters from txt file
    Returns:
        desired_parameters: <dict> dictionary of all desired parameters from
                            txt file
    '''
    desired_parameters = {
        'acceleration_voltage': float(all_parameters['CM_ACCEL_VOLT'][0]),
        'emission_current': float(all_parameters['SM_EMI_CURRENT'][0]),
        'brightness': int(all_parameters['CM_BRIGHTNESS'][0]),
        'contrast': int(all_parameters['CM_CONTRAST'][0]),
        'magnification': int(all_parameters['CM_MAG'][0]),
        'working_distance': float(all_parameters['SM_WD'][0]),
        'calibration_pixels': int(all_parameters['SM_MICRON_BAR'][0])}

    ''' Units given to 2 characters (um, nm, etc.) '''
    units_suffix = 2
    calibration_distance = all_parameters['SM_MICRON_MARKER'][0]
    desired_parameters['calibration_distance'] = int(
        calibration_distance[: -units_suffix])
    desired_parameters['distance_unit'] = calibration_distance[-units_suffix:]

    ''' CM_FULL_SIZE is [width, height] '''
    width, height = (0, 1)
    desired_parameters['image_width'] = int(
        all_parameters['CM_FULL_SIZE'][width])
    desired_parameters['image_height'] = int(
        all_parameters['CM_FULL_SIZE'][height])
    return desired_parameters


def read_SEM_log(file_path):
    '''
    Load JEOL-SEM txt file as a dictionary of key parameters.
    Args:
        file_path: <string> path to file
    Returns:
        parameters: <dict> desired parameter dictionary
    '''
    with open(file_path) as infile:
        all_lines = infile.readlines()
    stripped_lines = remove_unwanted(
        all_lines=all_lines,
        unwanted_character='$')
    JEOL_parameters = lines_to_parameters(lines=stripped_lines)
    parameters = desired_JEOL_parameters(all_parameters=JEOL_parameters)
    return parameters


def read_image(file_path):
    '''
    Load image file.
    Args:
        file_path: <string> path to file
    Returns:
        image: <array> numpy array of pixels
    '''
    image = Image.open(file_path)
    return np.array(image)


def convert(o):
    '''
    Check type of data string
    '''
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError


def save_json_dicts(out_path,
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
