from scipy import interpolate
import numpy as np


def interp(z_var):
    # cubic interpolation on the image
    # at a resolution of (pix_mult*8 x pix_mult*8)
    xx, yy = (np.linspace(0, 8, 8),
              np.linspace(0, 8, 8))
    grid_x, grid_y = (np.linspace(0, 8, 64),
                      np.linspace(0, 8, 64))
    f = interpolate.interp2d(xx, yy, z_var, kind='cubic')
    return f(grid_x, grid_y)