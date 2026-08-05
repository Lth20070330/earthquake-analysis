# 全球地震数据分析与风险评价系统

基于 USGS 地震目录数据，对全球地震活动进行数据清洗、统计分析、空间聚类与风险评估，并提供一个 tkinter 图形界面进行交互式分析。

## 项目概述

本项目从原始地震数据出发，完成从数据预处理到风险评估的完整流程：

- **数据预处理**：去重、缺失值处理、类型转换、时间特征提取、异常值过滤
- **统计分析**：时间分布（月度/日尺度）、震级分布、空间分布、热点区域、深度-震级关系
- **空间聚类**：使用 K-means 对地震经纬度进行聚类，识别地震带
- **风险评估**：基于 AHP（层次分析法）构建震级-深度-活动性三指标风险评价模型，含一致性检验
- **可视化**：10 类图表，含全球底图叠加
- **GUI 界面**：tkinter 实现，菜单驱动各分析模块，支持单次地震风险评估

## 数据来源

`data.csv` 来自 [USGS Earthquake Catalog](https://earthquake.usgs.gov/earthquakes/search/)，约 16000 条记录，字段包括时间、经纬度、深度、震级、地点等。

## 目录结构

```
代码/
├── data.csv              # 原始地震数据
├── data_process.py       # 数据加载与预处理
├── analysis.py           # 统计分析（时间/震级/空间/热点/深度）
├── clustering.py         # K-means 空间聚类
├── ahp_risk.py           # AHP 风险评价模型
├── visualization.py      # 可视化（10 类图表）
├── gui.py                # tkinter GUI 主程序
├── results/              # 生成的图表输出
│   ├── monthly_count.png
│   ├── daily_trend.png
│   ├── magnitude_distribution.png
│   ├── magnitude_pie.png
│   ├── world_distribution.png
│   ├── hotspot.png
│   ├── depth_magnitude.png
│   ├── kmeans_cluster.png
│   ├── risk_level_distribution.png
│   └── ahp_weights.png
└── .gitignore
```

## 环境依赖

- Python 3.11+
- pandas, numpy
- scikit-learn
- matplotlib
- geopandas, geodatasets
- Pillow

安装依赖：

```bash
pip install pandas numpy scikit-learn matplotlib geopandas geodatasets Pillow
```

## 使用方法

### 启动 GUI

```bash
python gui.py
```

GUI 左侧菜单提供以下功能：

1. 数据概况
2. 时间变化分析
3. 震级特征分析
4. 全球空间分布
5. 地震热点分析
6. 深度-震级关系
7. K-means 空间聚类
8. AHP 风险评价
9. 单次风险评估（输入震级/深度/经纬度，输出风险等级）

### 单独运行模块

各分析模块可独立运行：

```bash
python data_process.py    # 数据预处理与概况
python analysis.py        # 统计分析
```

## AHP 风险评价说明

判断矩阵（震级 > 深度 > 活动性）：

| 指标 | 震级 | 深度 | 活动性 |
|------|------|------|--------|
| 震级 | 1 | 3 | 5 |
| 深度 | 1/3 | 1 | 2 |
| 活动性 | 1/5 | 1/2 | 1 |

- 震级分数：按能量 `10^(1.5*mag)` 归一化
- 深度分数：<70km → 1.0，<300km → 0.6，否则 0.3
- 活动性分数：5°网格内历史地震频次归一化

综合得分按 0.6/0.3 阈值划分为 High / Medium / Low 三级。
