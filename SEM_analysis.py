import time
import numpy as np
import src.fileIO as io
import src.filepaths as fp
import src.analysis as anal
import matplotlib.pyplot as plt

from pathlib import Path


def remove_outliers(arr, threshold):
    mean_value = np.mean(arr)
    std_dev = np.std(arr)

    # Identify elements significantly smaller or larger than the mean
    outliers = [val for val in arr if val < mean_value - threshold * std_dev or val > mean_value + threshold * std_dev]

    # Create a new array without outliers
    filtered_arr = [val for val in arr if val not in outliers]

    return filtered_arr


if __name__ == '__main__':
    root = Path().absolute()
    storage_path = Path('//storage.its.york.ac.uk/physics/krauss/Josh/Post_Doc')
    SEM_path = Path(f'{storage_path}/SEM/Analysis')
    file_list = fp.extractfile(
        directory_path=SEM_path,
        file_string='.bmp')
    for file in file_list[1:2]:
        file_path = Path(f'{SEM_path}/{file}')
        file_name = fp.get_filename(file_path=file_path)
        text_path = Path(f'{SEM_path}/{file_name}.txt')
        image = io.read_image(file_path=file_path)
        image_parameters = io.read_SEM_log(file_path=text_path)
        grating_region = anal.trim_img_to_roi(
            image=image,
            height=image_parameters['image_height'],
            width=image_parameters['image_width'])
        distance_per_pixel = anal.calc_distance_per_pixel(
            distance_value=image_parameters['calibration_distance'],
            distance_unit=image_parameters['distance_unit'],
            number_of_pixels=image_parameters['calibration_pixels'])
        print(f'\n{file}')
        period = 0.500
        for row in grating_region:
            mean_value = np.mean(row)
            std = np.std(row)

            # Initialize variables
            below_mean_lengths = []
            above_mean_lengths = []

            # Iterate through the array to find individual sections
            current_section_length = 0
            for value in row:
                print(f'Value = {value}, Mean = {mean_value}, StdDev = {std}')
                if value < mean_value:
                    current_section_length += 1
                else:
                    if current_section_length > 0:
                        below_mean_lengths.append(current_section_length)
                        current_section_length = 0
            # Check if the last section is below mean
            if current_section_length > 0:
                below_mean_lengths.append(current_section_length)

            current_section_length = 0
            for value in row:
                print(f'Value = {value}, Mean = {mean_value}, StdDev = {std}')
                if value > mean_value:
                    current_section_length += 1
                else:
                    if current_section_length > 0:
                        above_mean_lengths.append(current_section_length)
                        current_section_length = 0
            # Check if the last section is above mean
            if current_section_length > 0:
                above_mean_lengths.append(current_section_length)

            # Calculate above mean lengths based on below mean lengths
            #above_mean_lengths = [length for length in below_mean_lengths if length > 0]

            # Print the results
            print(f"Lengths of sections below the mean: {below_mean_lengths}")
            print(f"Lengths of sections above the mean: {above_mean_lengths}")

            # Remove outliers
            aboves = remove_outliers(arr=above_mean_lengths, threshold=2)
            belows = remove_outliers(arr=below_mean_lengths, threshold=2)

            # Print the results
            print(f"Lengths of sections below the mean: {belows}")
            print(f"Lengths of sections above the mean: {aboves}")

            # Calculate the distances
            above_lengths = [length * distance_per_pixel for length in above_mean_lengths]
            below_lengths = [length * distance_per_pixel for length in below_mean_lengths]

            # Print the results
            print(f"Lengths of sections below the mean: {below_lengths}")
            print(f"Lengths of sections above the mean: {above_lengths}")

            # Average them
            above_avg = np.mean(above_lengths)
            below_avg = np.mean(below_lengths)

            # Print the results
            print(f"Lengths of sections below the mean: {below_avg}")
            print(f"Lengths of sections above the mean: {above_avg}")

            # Fill factor
            ff = above_avg / period
            print(f'Fill Factor = {ff}')
