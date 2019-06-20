# force floating point division. Can still use integer with //
from __future__ import division
# This file is used for importing the common utilities classes.
import numpy as np
import matplotlib.pyplot as plt
import sys
import warnings
from ..FEC import FEC_Util
from ..UtilIgor import PxpLoader,ProcessSingleWave
from ..UtilGeneral import GenUtilities,PlotUtilities
from mpl_toolkits.axes_grid1 import make_axes_locatable

def fit_to_image(image,deg=1,thresh=None,**kw):
    to_ret = np.zeros_like(image)
    shape = to_ret.shape
    coords = np.arange(shape[1])
    n_rows = shape[0]
    mean = np.mean(image)
    image_to_fit = image - mean
    for i in range(n_rows):
        raw_row = image_to_fit[i,:].copy()
        if thresh is not None:
            idx_to_fit = np.where( (raw_row < thresh))[0]
        else:
            idx_to_fit = np.arange(raw_row.size,dtype=np.int64)
        if idx_to_fit.size == 0:
            warnings.warn("Couldn't fit to image")
            corr = np.zeros(np.array(coords).size)
        else:
            coeffs = np.polyfit(x=coords[idx_to_fit],
                                y=raw_row[idx_to_fit],deg=deg,**kw)
            corr = np.polyval(coeffs,x=coords)
        to_ret[i,:] = corr
    # add back in the mean, since we subtracted it
    return to_ret + mean

def line_background(image,deg=1,**kw):
    """
    :param image: original, to correct
    :param deg:  polynomial to subtract from each *row* of image
    :param kw:
    :return: array, polynomial fit to each row of image
    """
    image_cp = image.copy()
    to_ret = fit_to_image(image_cp, deg=deg,**kw)
    return to_ret

def subtract_background(image,**kwargs):
    """
    subtracts a line of <deg> from each row in <images>
    """
    corr = line_background(image,**kwargs)
    return image - corr    
    
def read_images_in_pxp_dir(dir,**kwargs):
    """
    Returns: all SurfaceImage objects from all pxps in dir
    """
    pxps_in_dir = GenUtilities.getAllFiles(dir,ext=".pxp")
    return [image
            for pxp_file in pxps_in_dir 
            for image in PxpLoader.ReadImages(pxp_file,**kwargs)]
            
def read_images_in_ibw_dir(dir,**kwargs):
    """
    Returns: all SurfaceImages objects from all ibws in dir
    """
    ibws_in_dir = GenUtilities.getAllFiles(dir,ext=".ibw")
    return [PxpLoader.read_ibw_as_image(ibw_file)
            for ibw_file in ibws_in_dir]

def cache_images_in_directory(pxp_dir,cache_dir,
                              load_func = read_images_in_pxp_dir,**kwargs):
    """
    conveniewnce wrapper. See FEC_Util.cache_individual_waves_in_directory, 
    except for images 
    """
    to_ret = FEC_Util.cache_individual_waves_in_directory(pxp_dir,cache_dir,
                                                          load_func=load_func,
                                                          **kwargs)
    return to_ret                                                  
    
def smart_colorbar(im,ax=plt.gca(),fig=plt.gcf(),size="5%",
                   colorbar_location='right',
                   label="Height (nm)",add_space_only=False,**kw):
    """
    Makes a color bar on the given axis/figure by moving the axis over a little 
    """    
    # make a separate axis for the colorbar 
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(colorbar_location, size=size, pad=0.1)
    if (not add_space_only):
        to_ret = PlotUtilities.colorbar(label,fig=fig,
                                        bar_kwargs=dict(mappable=im,cax=cax),
                                        **kw)
        return to_ret
    else:
        cax.axis('off')
        return None

    
def make_image_plot(im,imshow_kwargs=dict(cmap=plt.cm.afmhot),pct=50):
    """
    Given an image object, makes a sensible plot 
    
    Args:
        im: PxpLoader.SurfaceImage object
        imshow_kwargs: passed directly to plt.imshow 
        pct: where to put 'zero' default to median (probably the surface
    Returns:
        output of im_show
    """
    # offset the data
    im_height = im.height_nm()
    min_offset = np.percentile(im_height,pct)
    im_height -= min_offset
    range_microns = im.range_meters * 1e6
    to_ret = plt.imshow(im_height.T,extent=[0,range_microns,0,range_microns],
                        interpolation='bicubic',**imshow_kwargs)
    PlotUtilities.tom_ticks()
    micron_str = PlotUtilities.upright_mu("m")
    PlotUtilities.lazyLabel(micron_str,micron_str,"",
                            tick_kwargs=dict(direction='out'))    
    return to_ret                                 
