'''
删除没有对应txt文件的图片
'''
import os

# 设置文件夹路径
image_folder = '../../images_dataset'

# 获取文件夹中的所有文件
files = os.listdir(image_folder)

# 统计图像文件数量
image_files = [f for f in files if f.endswith('.jpg')]
txt_files = [f for f in files if f.endswith('.txt')]

# 查找没有对应.txt文件的.jpg文件
images_without_txt = []
for image_file in image_files:
    txt_file = image_file.replace('.jpg', '.txt')
    if txt_file not in txt_files:
        images_without_txt.append(image_file)

# 删除没有对应.txt文件的.jpg文件
for image_file in images_without_txt:
    os.remove(os.path.join(image_folder, image_file))

# 输出结果
total_images = len(image_files)
deleted_images = len(images_without_txt)

print(f"一共有{total_images}张图片")
if images_without_txt:
    print("下列图片没有对应的.txt文件：")
    for image_file in images_without_txt:
        print(image_file)
print(f"已删除上述{deleted_images}张图片")
