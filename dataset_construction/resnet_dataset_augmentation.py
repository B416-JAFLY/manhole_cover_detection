import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import random

def rotate_images_in_directory(images_path):
    # 需要旋转的角度
    angles = [45, 90, 135, 180, 225, 270, 315]
    
    # 获取目录中的所有文件
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法读取图像: {image_path}")
            continue
        
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        
        for angle in angles:
            # 计算旋转矩阵
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # 计算新的边界尺寸
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])
            new_w = int((h * sin) + (w * cos))
            new_h = int((h * cos) + (w * sin))
            
            # 调整旋转矩阵以考虑新尺寸
            M[0, 2] += (new_w / 2) - center[0]
            M[1, 2] += (new_h / 2) - center[1]
            
            # 执行仿射变换（旋转）
            rotated_image = cv2.warpAffine(image, M, (new_w, new_h))
            
            # 保存旋转后的图像
            new_image_path = f"{images_path}/{os.path.splitext(image_file)[0]}_rotate_{angle}.jpg"
            cv2.imwrite(new_image_path, rotated_image)
    
    print(f"一共处理了{len(image_files)}张图像")

def translate_image(images_path, shift_x, shift_y):
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        image = cv2.imread(image_path)
        rows, cols = image.shape[:2]
        M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        translated_image = cv2.warpAffine(image, M, (cols, rows))
        cv2.imwrite(f"{images_path}/{os.path.splitext(image_file)[0]}_translate_{shift_x}_{shift_y}.jpg", translated_image)
    print(f"一共处理了{len(image_files)}张图像")

def scale_image(images_path, scale_factor):
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        image = Image.open(image_path)
        new_size = (int(image.size[0] * scale_factor), int(image.size[1] * scale_factor))
        scaled_image = image.resize(new_size)
        scaled_image.save(f"{images_path}/{os.path.splitext(image_file)[0]}_scale_{scale_factor}.jpg")
    print(f"一共处理了{len(image_files)}张图像")

def flip_image(images_path, direction):
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        image = Image.open(image_path)
        if direction == 'horizontal':
            flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        flipped_image.save(f"{images_path}/{os.path.splitext(image_file)[0]}_flip_{direction}.jpg")
    print(f"一共处理了{len(image_files)}张图像")

def crop_image(images_path, crop_area):
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        image = Image.open(image_path)
        cropped_image = image.crop(crop_area)
        cropped_image.save(f"{images_path}/{os.path.splitext(image_file)[0]}_crop.jpg")
    print(f"一共处理了{len(image_files)}张图像")

def color_jitter_image(images_path, brightness, contrast, saturation):
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        image = Image.open(image_path)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
        enhancer = ImageEnhance.Color(image)
        jittered_image = enhancer.enhance(saturation)
        jittered_image.save(f"{images_path}/{os.path.splitext(image_file)[0]}_color_jitter.jpg")
    print(f"一共处理了{len(image_files)}张图像")

def add_noise_image(images_path, variance):
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        image = cv2.imread(image_path)
        row, col, ch = image.shape
        mean = 0
        sigma = variance ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        noisy_image = image + gauss.reshape(row, col, ch)
        cv2.imwrite(f"{images_path}/{os.path.splitext(image_file)[0]}_noise.jpg", noisy_image)
    print(f"一共处理了{len(image_files)}张图像")

def affine_transform_image(images_path, pts1, pts2):
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        image = cv2.imread(image_path)
        rows, cols, ch = image.shape
        M = cv2.getAffineTransform(np.float32(pts1), np.float32(pts2))
        transformed_image = cv2.warpAffine(image, M, (cols, rows))
        cv2.imwrite(f"{images_path}/{os.path.splitext(image_file)[0]}_affine.jpg", transformed_image)
    print(f"一共处理了{len(image_files)}张图像")

def gamma_correction_image(images_path, gamma):
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法读取图像: {image_path}")
            continue
        
        for g in [gamma, 1.0/gamma]:  # 使用 gamma 和 1.0/gamma
            inv_gamma = 1.0 / g
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            gamma_image = cv2.LUT(image, table)
            gamma_sign = 'positive' if g > 1 else 'negative'
            cv2.imwrite(f"{images_path}/{os.path.splitext(image_file)[0]}_gamma_{gamma_sign}_{abs(g)}.jpg", gamma_image)

    
    print(f"一共处理了{len(image_files)}张图像")

def gaussian_blur_image(images_path, kernel_size):
    image_files = os.listdir(images_path)
    for image_file in image_files:
        image_path = os.path.join(images_path, image_file)
        image = cv2.imread(image_path)
        blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
        cv2.imwrite(f"{images_path}/{os.path.splitext(image_file)[0]}_blur_{kernel_size}.jpg", blurred_image)
    print(f"一共处理了{len(image_files)}张图像")


def process_directory(base_path):

    exclude_folders = [
    "0-北京电信",
]
    folders = os.listdir(base_path)
    
    for folder in folders:
        if folder not in exclude_folders:
            images_path = os.path.join(base_path, folder)
            if os.path.isdir(images_path):
                print(f"正在处理{folder}文件夹")
                
                # 旋转示例
                # rotate_images_in_directory(images_path)
                
                # 颜色抖动示例
                color_jitter_image(images_path, 1.2, 1.5, 1.3)
                
                # 添加噪声示例
                add_noise_image(images_path, 1600)
                
                # 伽马校正示例
                gamma_correction_image(images_path, 2.0)






if __name__ == "__main__":

    base_path = "../../images_dataset_resnet/00"
    process_directory(base_path)




    # images_path = "../../images_dataset_resnet/0/0-北京电信"
    
    # # 旋转示例
    # rotate_images_in_directory(images_path)  
        
    # # 颜色抖动示例
    # color_jitter_image(images_path, 1.2, 1.5, 1.3)
    
    # # 添加噪声示例
    # add_noise_image(images_path, 1600)
    
    # # 伽马校正示例
    # gamma_correction_image(images_path, 2.0)
    
    # # 高斯模糊示例
    # gaussian_blur_image(images_path, 5)







    # # 平移示例
    # translate_image(images_path, 10, 20)
    
    # # 缩放示例
    # scale_image(images_path, 1.5)
    
    # # 翻转示例
    # flip_image(images_path, 'horizontal')
    
    # # 裁剪示例
    # crop_area = (50, 50, 200, 200)
    # crop_image(images_path, crop_area)

        
    # # 仿射变换示例
    # pts1 = [(50, 50), (200, 50), (50, 200)]
    # pts2 = [(10, 100), (200, 50), (100, 250)]
    # affine_transform_image(images_path, pts1, pts2)