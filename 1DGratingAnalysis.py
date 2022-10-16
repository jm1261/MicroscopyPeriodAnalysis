import os
import numpy as np
import Functions.Organisation as org

import src.fileIO as fileIO
import src.analysis as anal



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
            for i in range(len(grating_region)):
                fourierfrequencies, fourierperiods = anal.FourierTransformRow(
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
                        anal.StandardErrorMean(x=p)
                        for p in np.array(periods).T],
                    'Average_Frequencies': [
                        np.sum(f) / len(f)
                        for f in np.array(frequencies).T],
                    'Frequencies_Errors': [
                        anal.StandardErrorMean(x=f)
                        for f in np.array(frequencies).T]})

            fileIO.save_json(
                out_path=os.path.join(
                    dirpath,
                    f'{file[0: -4]}_Results.json'),
                dictionary=calculated_grating_properties)

        else:
            pass
