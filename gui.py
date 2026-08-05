import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
from data_process import (load_data,clean_data)
from analysis import (
    time_analysis,
    magnitude_analysis,
    spatial_analysis,
    hotspot_analysis,
    depth_magnitude_analysis
)
from visualization import (
    plot_monthly_count,
    plot_daily_trend,
    plot_magnitude_distribution,
    plot_magnitude_pie,
    plot_world_distribution,
    plot_hotspot,
    plot_depth_magnitude,
    plot_kmeans_cluster,
    plot_risk_distribution,
    plot_ahp_weights
)
from clustering import (kmeans_clustering)
from ahp_risk import (
    calculate_risk_index,
    classify_risk,
    single_risk_assessment,
    calculate_ahp_weights
)

#初始化
data = load_data()
data = clean_data(data)
FONT_TITLE = ("SimHei",18,"bold")
FONT_BUTTON = ("Microsoft YaHei",11)
FONT_TEXT = ("Microsoft YaHei",10)
FONT_NORMAL = ("Microsoft YaHei",11)

# 主窗口
window = tk.Tk()
window.title("全球地震数据分析与风险评价系统")
window.geometry("1200x800")
left_frame = tk.Frame(window,width=220)
left_frame.pack(side="left",fill="y",padx=10,pady=10)
right_frame = tk.Frame(window)
right_frame.pack(side="right",expand=True,fill="both",padx=10,pady=10)
title = tk.Label(left_frame,text="功能菜单",font=FONT_TITLE)
title.pack(pady=20)
image_frame = tk.Frame(right_frame)
image_frame.pack(pady=10)
result_box = scrolledtext.ScrolledText(right_frame,width=80,height=8,font=FONT_TEXT)
result_box.pack(pady=5)
log_box = scrolledtext.ScrolledText(right_frame,width=80,height=8, font=FONT_TEXT)
log_box.pack(pady=5)
current_images = []
def show_result(text):
    result_box.delete("1.0",tk.END)
    result_box.insert(tk.END,text)
def write_log(text):
    log_box.insert(tk.END,text + "\n")
    log_box.see(tk.END)


def show_images(paths):
    global current_images

    for widget in image_frame.winfo_children():
        widget.destroy()
    current_images = []
    if len(paths) == 1:
        size = (850, 500)
    else:
        size = (400, 300)

    for path in paths:
        try:
            img = Image.open(path)
            img.thumbnail(size)
            photo = ImageTk.PhotoImage(img)
            current_images.append(photo)
            label = tk.Label(image_frame, image=photo)
            label.pack(side="left", padx=10)
            write_log(f"加载图片:{path}")
        except Exception:
            write_log(f"图片加载失败:{path}")

# 功能页面
def summary():
    show_result(
f"""
数据概况
数据量:
{len(data)} 条

时间范围:
{data['time'].min()}
至
{data['time'].max()}
平均震级:
{data['mag'].mean():.2f}
最大震级:
{data['mag'].max():.2f}
平均深度:
{data['depth'].mean():.2f} km
"""
    )
    write_log("完成数据概况统计")





def time_page():
    result = time_analysis(data)
    plot_monthly_count(result["monthly"])
    plot_daily_trend(result["daily"])
    show_images(["results/monthly_count.png", "results/daily_trend.png"])
    show_result(
"""
时间变化分析
包含：
1. 月度地震数量变化
2. 日尺度地震活动趋势
用于分析地震活动时间规律。
"""
    )
    write_log("时间分析完成")





def magnitude_page():
    result = magnitude_analysis(data)
    plot_magnitude_distribution(data)
    plot_magnitude_pie(result["distribution"])
    show_images(["results/magnitude_distribution.png", "results/magnitude_pie.png"])
    show_result(
f"""
震级特征分析
平均震级:
{result['mean']:.2f}
最大震级:
{result['max']:.2f}
包括：
震级连续分布
震级等级比例
"""
    )
    write_log("震级分析完成")





def spatial_page():
    result = spatial_analysis(data)
    plot_world_distribution(result)
    show_images(["results/world_distribution.png"])
    show_result(
"""
全球空间分布分析
根据经纬度坐标展示全球地震事件空间分布。
"""
    )
    write_log("空间分布分析完成")





def hotspot_page():
    result = hotspot_analysis(data)
    plot_hotspot(result)
    show_images(["results/hotspot.png"])
    show_result(
"""
地震热点分析
采用空间网格统计方法。
用于发现全球地震活动高频区域。
"""
    )
    write_log("热点分析完成")





def depth_page():
    result = depth_magnitude_analysis(data)
    plot_depth_magnitude(result["data"])
    show_images(["results/depth_magnitude.png"])
    show_result(
f"""
震源深度-震级关系
相关系数:
{result['correlation']:.3f}
"""
    )
    write_log("深度关系分析完成")





def cluster_page():
    result = kmeans_clustering(data, 5)
    plot_kmeans_cluster(result)
    show_images(["results/kmeans_cluster.png"])
    show_result(
f"""
K-means空间聚类
聚类数量:
5
轮廓系数:
{result['score']:.3f}
"""
    )
    write_log("K-means聚类完成")



# AHP风险评价
def risk_page():
    risk_data = calculate_risk_index(data)
    result = classify_risk(risk_data)
    plot_risk_distribution(result)
    weights, CR = calculate_ahp_weights()
    plot_ahp_weights(weights)
    show_images(["results/risk_level_distribution.png", "results/ahp_weights.png"])
    count = result["risk_level"].value_counts()
    show_result(
f"""
AHP风险等级评价
评价方法:
层次分析法(AHP)
指标权重:
Magnitude:
{weights['Magnitude']:.3f}
Depth:
{weights['Depth']:.3f}
Activity:
{weights['Activity']:.3f}
一致性比例 CR:
{CR:.4f}
风险等级统计:
High:
{count.get('High',0)}
Medium:
{count.get('Medium',0)}
Low:
{count.get('Low',0)}
"""
    )
    write_log("AHP风险评价完成")

# 单次风险评估窗口

def risk_predict_window():
    win = tk.Toplevel(window)
    win.title("单次地震风险评估")
    win.geometry("400x400")
    names = ["震级", "深度", "纬度", "经度"]
    entries = []
    for name in names:
        tk.Label(win, text=name, font=FONT_NORMAL).pack(pady=5)
        entry = tk.Entry(win)
        entry.pack()
        entries.append(entry)
    def evaluate():
        try:
            result = single_risk_assessment(float(entries[0].get()), float(entries[1].get()), float(entries[2].get()), float(entries[3].get()), data)

            messagebox.showinfo("风险评估结果",
f"""
风险评分:
{result['score']:.3f}
风险等级:
{result['level']}
"""
            )

            write_log("完成一次AHP风险评估")

        except Exception as e:
            messagebox.showerror("错误", "请输入正确数字")

    tk.Button(win, text="开始评估", font=FONT_BUTTON, command=evaluate).pack(pady=20)

# 按钮
# ==========================


buttons = [
    ("数据概况", summary),
    ("时间变化分析", time_page),
    ("震级特征分析", magnitude_page),
    ("全球空间分布", spatial_page),
    ("地震热点分析", hotspot_page),
    ("深度-震级关系", depth_page),
    ("K-means空间聚类", cluster_page),
    ("AHP风险评价", risk_page),
    ("单次风险评估", risk_predict_window)
]

for text, command in buttons:
    tk.Button(left_frame, text=text, width=22, height=2, font=FONT_BUTTON, command=command).pack(pady=5)
tk.Button(left_frame, text="退出", width=22, height=2, font=FONT_BUTTON, command=window.destroy).pack(pady=20)
window.mainloop()