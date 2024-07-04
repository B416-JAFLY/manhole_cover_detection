'''
构建resnet分类任务数据集，把原始yolo数据集中的图像裁剪成包含单个元素的图像，并保存到新的目录中。
'''
import os
import cv2

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def crop_and_save_image(image_path, label_path, output_dir):
    # 读取图像
    image = cv2.imread(image_path)
    h, w, _ = image.shape
    
    # 读取标签
    with open(label_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        # 解析标签内容
        parts = line.strip().split()
        class_info = parts[0]
        class_id, class_name = class_info.split('-')
        x_center, y_center, width, height = map(float, parts[1:])
        
        # 计算边界框坐标
        x1 = int((x_center - width / 2) * w)
        y1 = int((y_center - height / 2) * h)
        x2 = int((x_center + width / 2) * w)
        y2 = int((y_center + height / 2) * h)
        
        # 裁剪图像
        cropped_image = image[y1:y2, x1:x2]
        
        # 保存裁剪后的图像
        output_folder = os.path.join(output_dir, class_id)
        ensure_dir(output_folder)
        base_name = os.path.basename(image_path)
        new_name = f"{class_info}_{base_name}"
        output_path = os.path.join(output_folder, new_name)
        cv2.imwrite(output_path, cropped_image)

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            image_path = os.path.join(directory, filename)
            label_path = os.path.splitext(image_path)[0] + '.txt'
            if os.path.exists(label_path):
                crop_and_save_image(image_path, label_path, directory)

if __name__ == '__main__':
    current_directory = '.'  # 当前目录
    process_directory(current_directory)
