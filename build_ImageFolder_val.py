import os
import shutil
from sklearn.model_selection import train_test_split

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def split_dataset(input_folder, output_folder, train_ratio=0.9):
    class_directories = [d for d in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, d))]
    insufficient_classes = []

    for class_dir in class_directories:
        class_path = os.path.join(input_folder, class_dir)
        images = [f for f in os.listdir(class_path) if f.endswith('.jpg')]
        
        if len(images) < 2:
            insufficient_classes.append(class_dir)
            continue

        train_images, val_images = train_test_split(images, train_size=train_ratio)

        # 创建训练和验证集的目录
        train_class_dir = os.path.join(output_folder, 'train', class_dir)
        val_class_dir = os.path.join(output_folder, 'val', class_dir)
        ensure_dir(train_class_dir)
        ensure_dir(val_class_dir)

        # 移动训练集图片
        for img in train_images:
            src_path = os.path.join(class_path, img)
            dst_path = os.path.join(train_class_dir, img)
            shutil.copy(src_path, dst_path)
        
        # 移动验证集图片
        for img in val_images:
            src_path = os.path.join(class_path, img)
            dst_path = os.path.join(val_class_dir, img)
            shutil.copy(src_path, dst_path)

    # 输出提示信息
    if insufficient_classes:
        for class_name in insufficient_classes:
            print(f"由于图片不足，{class_name}类没有划分验证集")

if __name__ == '__main__':
    input_directory = './images_element_recognized/1'  # 要处理的文件夹
    output_directory = './dataset_element_recognized/1'  # 输出文件夹
    split_dataset(input_directory, output_directory)
