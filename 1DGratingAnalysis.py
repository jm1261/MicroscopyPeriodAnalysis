import os
import numpy as np
import Functions.Organisation as org

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

    txtfiles, imagefiles = org.FindDirFile(
        dir_path=working_directory,
        file_string='.txt',
        image_string='.bmp')

    for file in txtfiles:

        if f'{file[0: -4]}.bmp' in imagefiles:
            print(file)
            txtpath = os.path.join(
                working_directory,
                file)

            sem_parameters = fileIO.read_sem_log(file_path=txtpath)

            imagepath = os.path.join(
                working_directory,
                f'{file[0: -4]}.bmp')

            image = fileIO.read_image(file_path=imagepath)

            grating_region = anal.trim_to_region_of_interest(
                image=image,
                height=sem_parameters['image_height'],
                width=sem_parameters['image_width'])

            distanceperpixel = anal.calculate_distanceperpixel(
                distance_value=sem_parameters['calibration_distance_value'],
                distance_unit=sem_parameters['calibration_distance_unit'],
                number_of_pixels=sem_parameters['calibration_number_of_pixels'])

            periods = []
            frequencies = []
            for row in grating_region:
                fourierfrequencies, fourierperiods = anal.FourierTransformRow(
                    row=row,
                    num_peaks=3,
                    distance_pixel=distanceperpixel)
                periods.append(fourierperiods)
                frequencies.append(fourierfrequencies)

            calculated_grating_properties = dict(
                sem_parameters,
                **{
                    'Average_Periods_nm': [
                        np.sum(p) / len(p)
                        for p in np.array(periods).T],
                    'Period_Errors_nm': [
                        anal.StandardErrorMean(x=p)
                        for p in np.array(periods).T],
                    'Average_Frequencies': [
                        np.sum(f) / len(f)
                        for f in np.array(frequencies).T],
                    'Frequencies_Errors': [
                        anal.StandardErrorMean(x=f)
                        for f in np.array(frequencies).T]}
            )

            fileIO.save_json(
                out_path=os.path.join(
                    working_directory,
                    f'{file[0: -4]}_Results.json'),
                dictionary=calculated_grating_properties)

        else:
            pass
