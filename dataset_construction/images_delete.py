'''
删除没有对应json文件的图片
'''
import os

# 设置文件夹路径
image_folder = './images/images_cut'

# 获取文件夹中的所有文件
files = os.listdir(image_folder)

# 统计图像文件数量
image_files = [f for f in files if f.endswith('.jpg')]
json_files = [f for f in files if f.endswith('.json')]

# 查找没有对应.json文件的.jpg文件
images_without_json = []
for image_file in image_files:
    json_file = image_file.replace('.jpg', '.json')
    if json_file not in json_files:
        images_without_json.append(image_file)

# 删除没有对应.json文件的.jpg文件
for image_file in images_without_json:
    os.remove(os.path.join(image_folder, image_file))

# 输出结果
total_images = len(image_files)
deleted_images = len(images_without_json)

print(f"一共有{total_images}张图片")
if images_without_json:
    print("下列图片没有对应的.json文件：")
    for image_file in images_without_json:
        print(image_file)
print(f"已删除上述{deleted_images}张图片")
