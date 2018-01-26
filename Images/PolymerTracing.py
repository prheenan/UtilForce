# force floating point division. Can still use integer with //
from __future__ import division
# other good compatibility recquirements for python3
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
# This file is used for importing the common utilities classes.
import numpy as np
import matplotlib.pyplot as plt
import sys,scipy,copy


class WormObject(object):
    def __init__(self,x,y,header,file_name):
        """
        object for keeping track of an x,y trace
        
        Args:
            x,y: the coordinates
            file_name: where this trace came from
            header: the header information to store from the file
        """
        self.x = x
        self.y = y
        self.file_name = file_name
        self.header = header
    def assert_fit(self):
        assert self.inf is not None

class TaggedImage:
    def __init__(self,image,worm_objects):
        """
        Grouping of an images and the associated traces on items
        
        Args:
            image_path: the file name of the image
            worm_objects: list of worm_objects associated with this image
        """
        self.image_path = image.Meta.SourceFile
        self.image = image
        self.worm_objects = worm_objects
    @property
    def Meta(self):
        return self.image.Meta
    @property
    def file_name(self):
        return self.image_path.rsplit("/",1)[-1]
    def subset(self,idx):
        return [copy.deepcopy(self.worm_objects[i]) for i in idx]
