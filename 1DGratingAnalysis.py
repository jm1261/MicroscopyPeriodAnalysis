import os

import src.analysis as anal
import src.fileIO as fileIO
import src.filepaths as filepaths
import src.gui as gui

if __name__ == '__main__':

    working_directory = filepaths.get_working_directory()
    working_directory = gui.prompt_for_path(
        default=working_directory,
        title='Select Target Directory',
        dir_path=True)

    all_sem_filepaths = filepaths.FindDirFile(
        working_directory=working_directory,
        log_extension='.txt',
        image_extension='.bmp')

    for sem_filepaths in all_sem_filepaths:
        filename = sem_filepaths['filename']
        logfile_path = sem_filepaths['logfile_path']
        image_path = sem_filepaths['image_path']
        print(filename)

        sem_parameters = fileIO.read_sem_log(file_path=logfile_path)

        image = fileIO.read_image(file_path=image_path)

        grating_region = anal.trim_to_region_of_interest(
            image=image,
            height=sem_parameters['image_height'],
            width=sem_parameters['image_width'])

        distanceperpixel = anal.calculate_distanceperpixel(
            distance_value=sem_parameters['calibration_distance_value'],
            distance_unit=sem_parameters['calibration_distance_unit'],
            number_of_pixels=sem_parameters['calibration_number_of_pixels'])

        grating_parameters = anal.calculate_grating_frequencies(
            grating_region, distanceperpixel)

        calculated_grating_properties = dict(
            sem_parameters,
            **grating_parameters
        )

        fileIO.save_json(
            out_path=os.path.join(
                working_directory,
                f'{filename}_Results.json'),
            dictionary=calculated_grating_properties)
