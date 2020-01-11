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

def ghi(latitude, longitude, title):
    """
    Found Wall time: 9.07 s
    """
    start = pd.Timestamp(datetime.date.today())
    end = start + pd.Timedelta(days=2)

    gfs = GFS()
    data = gfs.get_processed_data(latitude, longitude, start, end)
    clouds = data['total_clouds'].resample("5min").interpolate()
    df = gfs.cloud_cover_to_irradiance(clouds, how='clearsky_scaling')

    ghi = df.ghi

    ax = ghi.plot()
    plt.ylabel("GHI FORECAST [W/m²]")
    plt.title(title)

    ax.axvline(pd.Timestamp.utcnow().floor("10min"), color="orange",
               linestyle="--")
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches=None, pad_inches=0.1)
    plt.close()
    buf.seek(0)

    return imageio.imread(buf)

