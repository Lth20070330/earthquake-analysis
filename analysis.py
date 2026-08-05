import pandas as pd
import numpy as np
def time_analysis(data):
#月、日
    monthly_count = (data.groupby("month").size().reset_index(name="count"))
    daily_count = (data.groupby("day").size().reset_index(name="count"))
    print("月份统计:")
    print(monthly_count)
    print("\n每日最大地震次数:")
    print(daily_count["count"].max())
    return {"monthly": monthly_count, "daily": daily_count}
def magnitude_analysis(data):
    #震级分布分析
    mean_mag = data["mag"].mean()
    max_mag = data["mag"].max()
    bins = [0, 3, 4, 5, 6, 10]
    labels = ["<3", "3-4", "4-5", "5-6", ">6"]
    level = pd.cut(data["mag"], bins=bins, labels=labels)
    mag_distribution = (level.value_counts().sort_index().reset_index())
    mag_distribution.columns = ["magnitude_level", "count"]
    print(f"平均震级:{mean_mag:.2f}")
    print(f"最大震级:{max_mag:.2f}")
    print("\n震级等级分布:")
    print(mag_distribution)
    return {"mean": mean_mag, "max": max_mag, "distribution": mag_distribution}

def spatial_analysis(data):

    spatial_data = data[["latitude", "longitude", "mag"]].copy()
    print(f"空间点数量:{len(spatial_data)}")
    return spatial_data

def hotspot_analysis(data, grid_size=5):
#地震热点区域分析
    temp = data.copy()
    temp["lat_grid"] = (np.floor(temp["latitude"] / grid_size) * grid_size)
    temp["lon_grid"] = (np.floor(temp["longitude"] / grid_size) * grid_size)
    hotspot = (temp.groupby(["lat_grid", "lon_grid"]).size().reset_index(name="count"))
    hotspot = hotspot.sort_values(by="count", ascending=False)
    print("Top10热点区域:")
    print(hotspot.head(10))
    return hotspot

def depth_magnitude_analysis(data):
#震源深度与震级关系分析

    relation = data[["depth", "mag"]].copy()
    corr = (relation.corr().loc["depth", "mag"])
    print(f"深度与震级相关系数:{corr:.3f}")
    return {"data": relation, "correlation": corr}




if __name__ == "__main__":
    from data_process import (load_data, clean_data)

    data = load_data()
    data = clean_data(data)

    time_analysis(data)
    magnitude_analysis(data)
    spatial_analysis(data)
    hotspot_analysis(data)
    depth_magnitude_analysis(data)