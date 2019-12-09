"""
This module will only contain functions that manipulates class ImagePtr
in linked list.
"""
import os
import sys
import shutil
from typing import List, Tuple
from pathlib import Path
from PIL import Image
from image_ptr import ImagePtr

def sort_img(files: List[str], destination: str, recursive: bool,
             copy: bool, verbose: bool) -> bool:
    """
    sort all images to the destination directory
    """

    for file in files:
        # get the image width and size
        size: Tuple[int, int] = _is_image(file)
        # sort to destination if it's image
        if size != (0, 0):
            # Create new directory if not exist
            # directory name is all image with the same size
            new_directory: str = os.path.join(destination,
                                              str(size[0]) + 'x' + str(size[1]))
            create_dir(new_directory)
            # Move or copy images to new directory
            # output error if file with same name exists
            try:
                if copy:
                    shutil.copy(file, new_directory)
                    if verbose:
                        print('COPY: "{}"\nTO:   "{}"'.format(file, new_directory))
                else:
                    shutil.move(file, new_directory)
                    if verbose:
                        print('MOVE: "{}"\nTO:   "{}"'.format(file, new_directory))
            except shutil.Error as error:
                print('{0}'.format(error), file=sys.stderr)

        # If file is directory and recursive is True
        elif recursive and os.path.isdir(file):
            # recursively calling its own function with complete file path
            lst_files: List[str] = [os.path.join(file, file_name)
                                    for file_name in os.listdir(file)]
            sort_img(lst_files, destination, recursive, copy, verbose)
        else:
            print('"{0}": is not image'.format(file), file=sys.stderr)


    return True


def dry_run(files:List[str], recursive: bool) -> List[ImagePtr]:
    """
    sort images by height and width

    Return: lst: List[ImagePtr]
    """
    # Contains list of object ImagePtr, with each object contains images
    # who has the same width and height
    lst: List[ImagePtr] = []

    # list all files in directory, get its absolute path
    files: List[str] = [f for f in os.listdir(directory)
                        if os.path.isfile(os.path.join(directory, f))]

    # Cycle through each file
    for file in files:
        file = os.path.join(directory, file) # get the full path
        # Check to see whether it can grab img width and height
        img_size: Tuple = _is_image(file)

        if img_size: # If it can, do the following:
            added: bool = False
            for node in lst: # Cycle through each node in list
                if node.is_same(img_size): # Add img path into node if same size
                    node.add_to_path(file)
                    added = True
            # Create new node if it's not added to the current nodes
            if not added:
                lst.append(ImagePtr(img_size[0], img_size[1], file))

    _print_all(lst)
    return lst

def create_dir(directory: str) -> bool:
    """
        Create from directory:str
        It will create parent directory if it doesn't exist.
        It won't throw Exception if directory already exists.
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
    except FileExistsError as error:
        sys.exit(error)

    return True


# private function
def _is_image(file: str) -> Tuple[int, int]:
    """
    verify whether it's image or not

    Return Tuple (img.width, img.height) if yes
    Return emtpy Tuple if no
    """
    try:
        with Image.open(file) as img:
            return img.size
    except IOError:
        return (0, 0)



def _print_all(lst: List[ImagePtr]) -> bool:
    """
    Private Function
    Print information about sorted images (by width and height)
    Return False if there's ImagePtr._lst is empty
    """
    if not lst:
        print("No image is being sorted into folder.")
        return False

    # print all sorted images and its related information
    for node in lst:
        # print sorted image size and all its related location
        print('Image Size: {}x{}'.format(node.width, node.height))
        # For every object, print all strings in List: node.path
        for location in node.path:
            print('| ', location)
    return True
