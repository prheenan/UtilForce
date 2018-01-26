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

from scipy.interpolate import splprep, splev, interp1d,UnivariateSpline

from scipy.stats import binned_statistic
        
from skimage.morphology import skeletonize,medial_axis,dilation
from skimage import measure
from scipy.interpolate import LSQUnivariateSpline
from skimage.segmentation import active_contour
from skimage.filters import gaussian


class spline_info(object):
    # holds low-level information on the actual fitting used. Everything
    # is in units of pixels
    def __init__(self, u, tck, spline, deriv,x0_px,y0_px):
        self.u = u
        self.tck = tck
        self.spline = spline
        self.deriv = deriv
        self.x0_px = x0_px
        self.y0_px = y0_px

class angle_info(object):
    def __init__(self,theta,L_px):
        self.theta = theta
        self.L_px = L_px
    @property
    def cos_theta(self):
        return np.cos(self.theta)


class polymer_info(object):
    # holds low-level information about the polymer itself
    def __init__(self,theta,cos_theta,
                 L_m,Lp_m,L0_m,L_binned,cos_angle_binned,coeffs):
        self.L_m = L_m
        self.theta = theta
        self.cos_angle = cos_theta
        self.Lp_m = Lp_m
        self.L0_m = L0_m
        self.L_binned = L_binned
        self.cos_angle_binned = cos_angle_binned
        self.coeffs = coeffs

class WormObject(object):
    def __init__(self,x,y,header,text_file):
        """
        object for keeping track of an x,y trace
        
        Args:
            x,y: the coordinates
            text_file: where this trace came from
            header: the header information to store from the file
        """
        self.x = x
        self.y = y
        self.file_name = text_file
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
