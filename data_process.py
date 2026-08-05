import pandas as pd
import os
def load_data(file_path="data.csv"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"未找到数据文件: {file_path}")
    data = pd.read_csv(file_path)
    print("数据读取成功")
    print(f"原始数据量: {len(data)} 条")
    print(f"字段数量: {len(data.columns)}")
    return data
def clean_data(data):

    # 1. 删除重复数据
    duplicate_num = data.duplicated(subset=["id"]).sum()
    print(f"发现重复记录: {duplicate_num} 条")
    data = data.drop_duplicates(subset=["id"])

    # 2. 关键字段缺失值处理
    key_columns = [
        "time",
        "latitude",
        "longitude",
        "depth",
        "mag"
    ]
    missing_num = data[key_columns].isnull().sum()
    print("\n关键字段缺失情况:")
    print(missing_num)
    before = len(data)
    data = data.dropna(subset=key_columns)
    after = len(data)
    print(f"删除缺失数据: {before-after} 条")

    # 3. 数据类型转换
    data["time"] = pd.to_datetime(data["time"],errors="coerce")
    numeric_columns = [
        "latitude",
        "longitude",
        "depth",
        "mag"
    ]
    for col in numeric_columns:
        data[col] = pd.to_numeric(data[col],errors="coerce" )
    data = data.dropna(subset=numeric_columns)
    # 4. 时间特征提取
    data["month"] = data["time"].dt.month
    data["day"] = data["time"].dt.date
    # 5. 异常值简单检查
    before = len(data)
    data = data[(data["mag"] > 0)&(data["depth"] >= 0)]
    after = len(data)
    print(f"删除异常记录: {before-after} 条")
    print("\n数据预处理完成")
    print(f"最终数据量: {len(data)} 条")
    return data


#输出一下概况
def data_summary(data):
    print("\n========== 数据概况 ==========")
    print(f"数据数量: {len(data)}")
    print(f"时间范围: "f"{data['time'].min()} "f"至 "f"{data['time'].max()}")
    print(f"平均震级: "f"{data['mag'].mean():.2f}")
    print(f"最大震级: "f"{data['mag'].max():.2f}")
    print(f"平均深度: "f"{data['depth'].mean():.2f} km")
if __name__ == "__main__":
    earthquake_data = load_data()
    earthquake_data = clean_data(earthquake_data)
    data_summary(earthquake_data)
