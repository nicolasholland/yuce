import pandas as pd
import datetime
from pvlib.forecast import GFS
import seaborn as sns;sns.set()
import matplotlib.pyplot as plt
from io import BytesIO
import imageio

def ghi():
    latitude = 34.3416
    longitude = 108.9398
    start = pd.Timestamp(datetime.date.today())
    end = start + pd.Timedelta(days=1)

    gfs = GFS()
    data = gfs.get_processed_data(latitude, longitude, start, end)
    clouds = data['total_clouds'].resample("5min").interpolate()
    df = gfs.cloud_cover_to_irradiance(clouds, how='clearsky_scaling')

    ghi = df.ghi

    ax = ghi.plot()
    plt.ylabel("GHI FORECAST [W/m²]")
    plt.title("北京")

    ax.axvline(pd.Timestamp.utcnow().floor("10min"), color="orange",
               linestyle="--")
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches=None, pad_inches=0.1)
    plt.close()
    buf.seek(0)

    return imageio.imread(buf)


def main():
    ghi()


if __name__ == '__main__':
    main()
