from os.path import join, dirname
import pandas as pd
import requests
import imageio

def saturl():
    time = (pd.Timestamp.utcnow() - pd.Timedelta("15min")).floor("10min")
    base = "https://www.data.jma.go.jp/mscweb/data/himawari/img/fd_/"
    retval = base + time.strftime("fd__b03_%H%M.jpg")
    return retval

def getimage():
    """
    Wall time: 165 ms
    """
    try:
        c = requests.get(saturl()).content
        img = imageio.imread(c)
        img = img[1:, 1:]
        imageio.imwrite(join(dirname(__file__), "data/sat.png"), img)

    except Exception as err:
        img = imageio.imread(join(dirname(__file__), "data/sat.png"))
        print(err)

    return img


