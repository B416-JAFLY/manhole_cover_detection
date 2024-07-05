'''
对Yolo验证集进行数据增殖，包括旋转+高斯噪声,其中90°的缩放由于涉及到标签的缩放，计算有点复杂，偷懒没做
'''
import os
import cv2
import numpy as np
import shutil

# 创建新文件夹
os.makedirs('images/val_augmentation', exist_ok=True)
os.makedirs('labels/val_augmentation', exist_ok=True)

def augment_image(image, angle):
    if angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    else:
        return image

def add_gaussian_noise(image, mean=0, var=2500):
    sigma = var**0.5
    gauss = np.random.normal(mean, sigma, image.shape).astype('float32')
    noisy_image = cv2.add(image.astype('float32'), gauss)
    return np.clip(noisy_image, 0, 255).astype('uint8')

def adjust_labels(labels, angle, img_shape):
    adjusted_labels = []
    height, width = img_shape
    for label in labels:
        cls, x, y, w, h = label
        if angle == 90:
            new_x = y
            new_y = 1 - x
            new_w = h
            new_h = w
        elif angle == 180:
            new_x = 1 - x
            new_y = 1 - y
            new_w = w
            new_h = h
        adjusted_labels.append((cls, new_x, new_y, new_w, new_h))
    return adjusted_labels

def load_labels(label_path):
    with open(label_path, 'r') as f:
        labels = [tuple(map(float, line.strip().split())) for line in f.readlines()]
    return labels

def save_labels(label_path, labels):
    with open(label_path, 'w') as f:
        for label in labels:
            f.write(' '.join(map(str, label)) + '\n')

# 获取所有图片和标签文件
image_files = [f for f in os.listdir('images/val') if f.endswith('.jpg')]
label_files = [f.replace('.jpg', '.txt') for f in image_files]

# 数据增殖
for img_file, lbl_file in zip(image_files, label_files):
    img_path = os.path.join('images/val', img_file)
    lbl_path = os.path.join('labels/val', lbl_file)
    
    # 读取图片和标签
    image = cv2.imread(img_path)
    labels = load_labels(lbl_path)
    
    # 原始图片和标签
    cv2.imwrite(os.path.join('images/val_augmentation', img_file), image)
    save_labels(os.path.join('labels/val_augmentation', lbl_file), labels)
    
    # 90°翻转
    # image_90 = augment_image(image, 90)
    # # image_90 = add_gaussian_noise(image_90)
    # labels_90 = adjust_labels(labels, 90, image.shape[:2])
    # cv2.imwrite(os.path.join('images/val_augmentation', '90_noisy_' + img_file), image_90)
    # save_labels(os.path.join('labels/val_augmentation', '90_noisy_' + lbl_file), labels_90)
    
    # 180°翻转
    image_180 = augment_image(image, 180)
    image_180 = add_gaussian_noise(image_180)
    labels_180 = adjust_labels(labels, 180, image.shape[:2])
    cv2.imwrite(os.path.join('images/val_augmentation', '180_noisy_' + img_file), image_180)
    save_labels(os.path.join('labels/val_augmentation', '180_noisy_' + lbl_file), labels_180)
    
    # # 添加高斯噪声
    noisy_image = add_gaussian_noise(image)
    cv2.imwrite(os.path.join('images/val_augmentation', 'noisy_' + img_file), noisy_image)
    save_labels(os.path.join('labels/val_augmentation', 'noisy_' + lbl_file), labels)

print("数据增殖完成。")
