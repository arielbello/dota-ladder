import os


def create_folder_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)
