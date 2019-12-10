"""
This class contains all images who has the same height and width.
"""
import os
from typing import Tuple
from PIL import Image

class ImagePtr:
    """
    This class contains all images who has the same height and width.
    """

    def __init__(self, width, height, file: str):
        self.width: int = width
        self.height: int = height
        # num of image with same width and height
        self.num: int = 1
        # total size(bytes) of all images who share the same width and height
        self.total_size: float = os.path.getsize(file)

    def get_width(self) -> int:
        """ return the width of image : int """
        return self.width

    def get_height(self) -> int:
        """ return the height of image : int """
        return self.height

    def get_num(self) -> int:
        """ return number of images who share the same width and height """
        return self.num

    def get_total_size(self) -> float:
        """ return total size of images who share the same width and height """
        return self.total_size

    def increment(self, img_size: float) -> bool:
        """ increment the number by image by one and total_size by img_size """
        self.num += 1
        self.total_size += img_size
        return True

    def is_same(self, tup: Tuple[int, int]) -> bool:
        """
        recive that tuple that contains 2 value (width: int, height: int)

        return true if it's the same as object, false otherwise
        """
        if tup[0] == self.width and tup[1] == self.height:
            return True

        return False
