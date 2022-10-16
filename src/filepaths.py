import os


def get_working_directory(subdirectory='TestImages'):
    current_directory = os.getcwd()
    working_directory = os.path.join(
        current_directory, subdirectory)
    return working_directory
