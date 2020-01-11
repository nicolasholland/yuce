import pandas as pd
import requests
import imageio

def saturl():
    time = (pd.Timestamp.utcnow() - pd.Timedelta("10min")).floor("10min")
    base = "https://www.data.jma.go.jp/mscweb/data/himawari/img/fd_/"
    retval = base + time.strftime("fd__b03_%H%M.jpg")
    return retval

def getimage():
    """
    Wall time: 165 ms
    """
    c = requests.get(saturl()).content
    img = imageio.imread(c)

    return img


