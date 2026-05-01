import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置字体路径
font_path = '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'
font = FontProperties(fname=font_path, size=35)

# 读取文本文件并加载到列表
def load_int_data(path):
    with open(path, 'r') as f:
        line = f.readline().strip()
        int_list = [int(item) for item in line.split(',') if item.isdigit()]
    return int_list

def load_float_data(path):
    with open(path, 'r') as f:
        line = f.readline().strip()
        float_list = [float(item) for item in line.split(',') if item.strip()]
    return float_list

# 创建图形和轴
def plot_lg(x, y, xlabel, ylabel, img_path):
    fig, ax = plt.subplots()

    # 绘制折线图
    ax.plot(x, y, marker='^', markersize=4, linewidth=1, color='#104680')

    # 添加标题和标签
    ax.set_xlabel(xlabel, fontproperties=font)
    ax.set_ylabel(ylabel, fontproperties=font)

    # 设置刻度字体
    ax.set_xticklabels(ax.get_xticks(), fontproperties=font)
    ax.set_yticklabels(ax.get_yticks(), fontproperties=font)

    # 显示网格
    ax.grid(True)

    # 显示图像
    plt.savefig(img_path, dpi=256)


def plot_dlg(x, y1, y2, xlabel, y1label, y2label, img_path, anchor=(1.0, 1.0)):
    fig, ax1 = plt.subplots(figsize=(12, 6.5))

    ax1.plot(x, y1, marker='^', markersize=2, linewidth=3, label=y1label, color='blue')
    ax1.set_xlabel(xlabel, fontproperties=font)
    ax1.set_ylabel(y1label, fontproperties=font)
    ax1.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])  
    ax1.set_xticklabels([0.0, 0.5, 1.0, 1.5, 2.0, 2.5], font=font)
    ax1.set_yticks([0, 2000, 4000, 6000, 8000, 10000])
    ax1.set_yticklabels(['0', '2k', '4k', '6k', '8k', '10k'], font=font)

    # 显示网格
    ax1.grid(True, linestyle='--', color='gray', linewidth=1.5)

    ax2 = ax1.twinx()  # 共存的右侧Y轴
    ax2.plot(x, y2, marker='^', markersize=2, linewidth=3, label=y2label, color='red')
    ax2.set_ylabel(y2label, fontproperties=font)

    ax2.set_yticks([2.00, 2.40, 2.80, 3.20, 3.60, 4.00])
    ax2.set_yticklabels([2.00, 2.40, 2.80, 3.20, 3.60, 4.00], font=font)

    # 获取两个图的图例项
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    # 合并图例项
    lines = lines1 + lines2
    labels = labels1 + labels2

    # 绘制合并的图例
    font.set_size(25)
    ax1.legend(lines, labels, prop=font, bbox_to_anchor=anchor)
    plt.subplots_adjust(left=0.17, right=0.84, top=0.95, bottom=0.2)

    plt.savefig(img_path, dpi=256)


if __name__ == '__main__':
    alpha_list = load_float_data('txt/alpha_or/output_alpha.txt')
    or_list = load_float_data('txt/alpha_or/output_or.txt')
    outlier_list = load_int_data('txt/alpha_or/output_outliers.txt')
    plot_dlg(alpha_list, outlier_list, or_list, r'$\alpha$', r'$Outliers(\alpha)$', r'$OR(\alpha)$', 'jpg/2017_LOCAL_ALPHA_OR_OOD.jpg')
