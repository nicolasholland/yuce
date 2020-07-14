import os
from os.path import dirname, join
import pandas as pd
import datetime
from pvlib.forecast import GFS
import seaborn as sns;sns.set()
import matplotlib.pyplot as plt
from io import BytesIO
import imageio

import matplotlib
matplotlib.rc('font', family='Source Han Sans CN')

LOCATIONS = {"北京" : (34.3416, 108.9398),
             "上海" : (31.2304, 121.4737),
             "台北" : (25.0330, 121.5654),
             "新加坡" : (1.3521, 103.8198)}

TITLE = imageio.imread(join(dirname(__file__), "images/title.png"))
LEGEND = imageio.imread(join(dirname(__file__), "images/legend.png"))

def get_data():
    filename = pd.Timestamp.utcnow().strftime("%Y%m%d.hdf")

    if not os.path.exists("data"):
        os.mkdir("data")

    files = os.listdir("data")
    retval = {}
    if filename not in files:
        clearcache(files)
        for loc in LOCATIONS.keys():
            df = download_data(*LOCATIONS[loc])
            df.to_hdf(os.path.join("data", filename), loc)

            retval[loc] = df

    else:
        for loc in LOCATIONS.keys():
            df = pd.read_hdf(os.path.join("data", filename), loc)
            retval[loc] = df

    return retval

def clearcache(files):
    for filename in files:
        try:
            os.remove(os.path.join("data", filename))
        except Exception as err:
            print(err)

def download_data(latitude, longitude):
    start = pd.Timestamp(datetime.date.today(), tz="UTC")
    end = start + pd.Timedelta(days=2)
    gfs = GFS()

    data = gfs.get_processed_data(latitude, longitude, start, end)
    clouds = data['total_clouds'].resample("5min").interpolate()
    df = gfs.cloud_cover_to_irradiance(clouds, how='clearsky_scaling')
    return df

def plot(data):
    start = pd.Timestamp(datetime.date.today())
    end = start + pd.Timedelta(hours=40)

    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_axes()

    for loc in data.keys():
        ghi = data[loc].loc[:end].ghi
        ax = ghi.plot(ax=ax, label=loc)


    plt.ylabel("GHI FORECAST [W/m²]")
    plt.legend()
    plt.title("GFS 预测")

    ax.axvline(pd.Timestamp.utcnow().floor("10min"), color="orange",
               linestyle="--")
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches=None, pad_inches=0.1, dpi=100)
    plt.close()
    buf.seek(0)

    return imageio.imread(buf)

def gfs():
    data = get_data()
    img = plot(data)

    img[46:46+23, 413:413+39, :] = TITLE[:, :, :]
    img[82:82+93, 658:658+52, :] = LEGEND[:, :, :]

    return img[:,:,:3]
