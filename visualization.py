import matplotlib.pyplot as plt
import os
import geopandas as gpd
import geodatasets
from matplotlib.lines import Line2D

RESULT_DIR = "results"
if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)
# 1. 月份图
def plot_monthly_count(month_data):
    plt.figure(figsize=(8,5))
    plt.bar(month_data["month"],month_data["count"])
    plt.xlabel("Month")
    plt.ylabel("Earthquake Count")
    plt.title("Monthly Earthquake Distribution")
    plt.xticks(range(1,13))
    plt.grid(alpha=0.3)
    plt.savefig(f"{RESULT_DIR}/monthly_count.png",dpi=300,bbox_inches="tight")
    plt.close()
# 2. 每日图
def plot_daily_trend(day_data):
    plt.figure(figsize=(10,5))
    plt.plot(range(len(day_data)),day_data["count"])
    plt.xlabel("Day Index")
    plt.ylabel("Earthquake Count")
    plt.title("Daily Earthquake Trend")
    plt.grid(alpha=0.3)
    plt.savefig(f"{RESULT_DIR}/daily_trend.png",dpi=300,bbox_inches="tight")
    plt.close()

# 3. 震级直方图
def plot_magnitude_distribution(data):
    plt.figure(figsize=(8,5))
    plt.hist(data["mag"], bins=30)
    plt.xlabel("Magnitude")
    plt.ylabel("Count")
    plt.title("Magnitude Distribution")
    plt.grid(alpha=0.3)
    plt.savefig(f"{RESULT_DIR}/magnitude_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()
# 4. 震级饼
def plot_magnitude_pie(mag_distribution):
    plt.figure(figsize=(7,7))
    plt.pie(mag_distribution["count"], labels=mag_distribution["magnitude_level"], autopct="%1.1f%%", startangle=90)
    plt.title("Magnitude Level Proportion")
    plt.savefig(f"{RESULT_DIR}/magnitude_pie.png", dpi=300, bbox_inches="tight")
    plt.close()

# 5. 全球地震空间分布
def plot_world_distribution(data):
    plt.figure(figsize=(12,6))
    ax = plt.gca()
    ax.set_facecolor("#dbeeff")
    world = gpd.read_file(geodatasets.get_path("naturalearth.land"))
    world.plot(ax=ax, color="lightgray", edgecolor="white")
    scatter = ax.scatter(data["longitude"], data["latitude"], c=data["mag"], s=data["mag"]**3, cmap="hot", alpha=0.65)
    plt.colorbar(scatter, ax=ax, label="Magnitude")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Global Earthquake Distribution")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.grid(alpha=0.3)
    plt.savefig(f"{RESULT_DIR}/world_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()
# 6. 全球热点热力图

def plot_hotspot(hotspot):
    plt.figure(figsize=(12,6))
    ax = plt.gca()
    ax.set_facecolor("#dbeeff")
    world = gpd.read_file(geodatasets.get_path("naturalearth.land"))
    world.plot(ax=ax, color="lightgray", edgecolor="white")
    scatter = ax.scatter(hotspot["lon_grid"], hotspot["lat_grid"], c=hotspot["count"], s=hotspot["count"]**0.8, cmap="YlOrRd", alpha=0.55)
    plt.colorbar(scatter, ax=ax, label="Earthquake Count")
    ax.set_title("Global Earthquake Hotspot Map")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.grid(alpha=0.3)
    plt.savefig(f"{RESULT_DIR}/hotspot.png", dpi=300, bbox_inches="tight")
    plt.close()

# 7. 深度-震级关系

def plot_depth_magnitude(relation):
    plt.figure(figsize=(8,5))
    plt.scatter(relation["depth"], relation["mag"], alpha=0.4)
    plt.xlabel("Depth(km)")
    plt.ylabel("Magnitude")
    plt.title("Depth-Magnitude Relationship")
    plt.grid(alpha=0.3)
    plt.savefig(f"{RESULT_DIR}/depth_magnitude.png", dpi=300, bbox_inches="tight")
    plt.close()

# 8. K-means空间聚类
def plot_kmeans_cluster(cluster_result):
    cluster_data = cluster_result["data"]
    centers = cluster_result["centers"]
    plt.figure(figsize=(12,6))
    ax = plt.gca()
    ax.set_facecolor("#dbeeff")
    world = gpd.read_file(geodatasets.get_path("naturalearth.land"))
    world.plot(ax=ax, color="lightgray", edgecolor="white")
    ax.scatter(cluster_data["longitude"], cluster_data["latitude"], c=cluster_data["cluster"], cmap="tab10", s=20, alpha=0.65)
    ax.scatter(centers["longitude"], centers["latitude"], marker="*", s=250, color="black")
    ax.set_title("K-means Earthquake Spatial Clustering")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.grid(alpha=0.3)
    plt.savefig(f"{RESULT_DIR}/kmeans_cluster.png", dpi=300, bbox_inches="tight")
    plt.close()

# 9. 风险等级分布
def plot_risk_distribution(data):
    risk_count = data["risk_level"].value_counts()
    plt.figure(figsize=(7,5))
    plt.bar(risk_count.index, risk_count.values)
    plt.xlabel("Risk Level")
    plt.ylabel("Count")
    plt.title("AHP Earthquake Risk Level Distribution")
    plt.grid(alpha=0.3)
    plt.savefig(f"{RESULT_DIR}/risk_level_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()

# 10. AHP权重分布

def plot_ahp_weights(weights):
    plt.figure(figsize=(7,5))
    plt.bar(list(weights.keys()), list(weights.values()))
    plt.xlabel("Indicator")
    plt.ylabel("Weight")
    plt.title("AHP Indicator Weights")
    plt.ylim(0, 1)
    plt.grid(alpha=0.3)
    plt.savefig(f"{RESULT_DIR}/ahp_weights.png", dpi=300, bbox_inches="tight")
    plt.close()