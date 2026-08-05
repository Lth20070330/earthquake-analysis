import numpy as np
import pandas as pd
#用AHP层次分析法，算一下打分公式权重，然后一致性检验一下
def calculate_ahp_weights():
#判断矩阵，我认为震级>深度>频次
    A = np.array([[1, 3, 5], [1/3, 1, 2], [1/5, 1/2, 1]])
    n = A.shape[0]
    # 特征值分解然后权重归一化
    eigenvalues, eigenvectors = np.linalg.eig(A)
    max_index = np.argmax(eigenvalues.real)
    lambda_max = eigenvalues[max_index].real
    weight = eigenvectors[:, max_index].real
    weight = (weight /weight.sum())

    # 一致性检验
    CI = (lambda_max - n) / (n - 1)
    RI = 0.58
    CR = CI / RI
    weights = {"Magnitude": weight[0],"Depth": weight[1],"Activity": weight[2]}
    return weights, CR

# 风险指标计算
def calculate_risk_index(data):
    result = data.copy()
    energy = 10 ** (1.5 * result["mag"])
    result["Magnitude_score"] = (energy /energy.max()) #震级需要指数归一化，剩下的都是线性的
    def depth_score(depth):
        if depth < 70:
            return 1.0
        elif depth < 300:
            return 0.6
        else:
            return 0.3
    result["Depth_score"] = (result["depth"].apply(depth_score))
    grid_size = 5
    result["lat_grid"] = (np.floor(result["latitude"] /grid_size))
    result["lon_grid"] = (np.floor(result["longitude"] /grid_size))

    frequency = (result.groupby([ "lat_grid","lon_grid"]).size().reset_index(name="frequency")  )
    result = result.merge(frequency,on=["lat_grid","lon_grid"], how="left")
    # 归一化
    if (result["frequency"].max() != result["frequency"].min()):
        result["Activity_score"] = (result["frequency"] - result["frequency"].min()) / (result["frequency"].max() - result["frequency"].min())
    else:
        result["Activity_score"] = 0

    return result

# AHP综合风险评分
def classify_risk(data):
    result = data.copy()
    weights, CR = calculate_ahp_weights()
    result["risk_score"] = (weights["Magnitude"] * result["Magnitude_score"] + weights["Depth"] * result["Depth_score"] + weights["Activity"] * result["Activity_score"])
    def level(score):
        if score >= 0.6:
            return "High"
        elif score >= 0.3:
            return "Medium"
        else:
            return "Low"

    result["risk_level"] = (result["risk_score"].apply(level))
    return result
# 单次风险评估
def single_risk_assessment(magnitude, depth, latitude, longitude, history_data):

    weights, CR = calculate_ahp_weights()
    magnitude_score = (10 ** (1.5 * magnitude) / 10 ** (1.5 * history_data["mag"].max()))
    if depth < 70:
        depth_value = 1.0
    elif depth < 300:
        depth_value = 0.6
    else:
        depth_value = 0.3
    # 活动性指标
    grid_size = 5
    lat_grid = np.floor(latitude / grid_size)
    lon_grid = np.floor(longitude / grid_size)
    temp = history_data.copy()
    temp["lat_grid"] = np.floor(temp["latitude"] / grid_size)
    temp["lon_grid"] = np.floor(temp["longitude"] / grid_size)
    current_count = len(temp[(temp["lat_grid"] == lat_grid) & (temp["lon_grid"] == lon_grid)])
    max_count = (temp.groupby(["lat_grid", "lon_grid"]).size().max())
    activity_score = (current_count / max_count)
    # 综合评分
    score = (weights["Magnitude"] * magnitude_score + weights["Depth"] * depth_value + weights["Activity"] * activity_score)

    if score >= 0.7:
        level = "High"
    elif score >=0.3:
        level = "Medium"
    else:
        level = "Low"
    return {"score": score, "level": level}

