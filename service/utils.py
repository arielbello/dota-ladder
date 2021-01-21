import os
import time
import constants as Const


def is_first_run() -> bool:
    return not os.path.exists(Const.Files.APP_LOG)


def log_write(log_text):
    with open(Const.Files.APP_LOG, "a+") as file:
        file.write(f"{time.ctime()}: {log_text}\n")


def create_folder_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)
