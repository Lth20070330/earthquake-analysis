from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

import pandas as pd
def kmeans_clustering(data, n_clusters=5):

    X = data[["latitude","longitude"]]
    # 创建模型
    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )
    labels = model.fit_predict(X)
    # 添加类别
    cluster_data = data.copy()
    cluster_data["cluster"] = labels
    # 聚类中心
    centers = pd.DataFrame(
        model.cluster_centers_,
        columns=[
            "latitude",
            "longitude"
        ]
    )
    print("聚类中心:")
    print(centers)

    # 轮廓系数
    score = silhouette_score(X,labels )
    print(f"\nSilhouette Score: {score:.3f}")
    return {
        "data": cluster_data,
        "centers": centers,
        "score": score
    }

def cluster_summary(cluster_result):
    data = cluster_result["data"]
    summary = (
        data
        .groupby("cluster")
        .agg(
            count=("id","count"),
            avg_mag=("mag","mean"),
            avg_depth=("depth","mean"),
            center_lat=("latitude","mean"),
            center_lon=("longitude","mean")
        )
        .reset_index()
    )
    print( summary)
    return summary
