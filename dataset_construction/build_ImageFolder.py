'''
把yolo数据集中拆分出来的元素图像，按照类别保存到不同的文件夹中。
'''
import os
import shutil
from collections import defaultdict

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def process_folder(input_folder):
    # 统计每个类的文件数量
    class_file_count = defaultdict(int)
    total_files = 0
    created_classes = set()

    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg'):
            # 获取类名和原文件名
            class_info, original_filename = filename.split('_', 1)
            class_folder = os.path.join(input_folder, class_info)
            
            # 确保类文件夹存在
            ensure_dir(class_folder)
            
            # 移动文件到类文件夹
            src_path = os.path.join(input_folder, filename)
            dest_path = os.path.join(class_folder, filename)
            shutil.move(src_path, dest_path)
            
            # 统计文件数量
            class_file_count[class_info] += 1
            total_files += 1
            created_classes.add(class_info)

    # 输出统计信息
    print(f"一共创建了{len(created_classes)}个类，处理了{total_files}个文件")
    for class_info, count in class_file_count.items():
        print(f"{class_info}类有{count}个文件")

if __name__ == '__main__':
    folder_to_process = '../../images_dataset_resnet/1'  # 要处理的文件夹
    process_folder(folder_to_process)
