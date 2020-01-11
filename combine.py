import numpy as np
import gfs
import himawari
import imageio
import io


def image():
    plot = gfs.gfs()
    sat = himawari.getimage()

    img = np.concatenate((sat, plot), axis=1)

    retval = io.BytesIO()
    imageio.imwrite(retval, img, format="png")
    return retval