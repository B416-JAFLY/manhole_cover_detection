'''
统计imagefolder中每个子文件夹中的图片数量，绘制直方图
'''
import os
# import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties

# 设置中文字体以避免中文字符显示问题
# font_path = 'SimHei.ttf'  # 确保字体文件路径正确
# font_prop = FontProperties(fname=font_path)
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
# plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 假设你的根目录路径是 'path_to_root_directory'
root_dir = '../../images_dataset_resnet/0'

# 获取子目录
subdirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

# 统计每个子目录下的文件数量
folder_counts = {}
for subdir in subdirs:
    subdir_path = os.path.join(root_dir, subdir)
    folder_counts[subdir] = len([d for d in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, d))])

# 输出统计结果
for folder, count in folder_counts.items():
    print(f"{folder} 文件夹共有 {count} 个文件")

# 绘制直方图
# plt.bar(folder_counts.keys(), folder_counts.values())
# plt.xlabel('文件夹')
# plt.ylabel('文件数量')
# plt.title('0/ 目录下各文件夹中的文件数量')
# plt.xticks(rotation=90)
# plt.tight_layout()
# plt.show()
