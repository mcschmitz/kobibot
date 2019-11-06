import os


def create_dir(directory_path):
    """
    Creates a directory to the given path if it does not exist and returns the path

    Args:
        directory_path: path directory

    Returns:
        the created path
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return directory_path
