import os
import json
from openpyxl import Workbook
from openpyxl.drawing.image import Image as OpenpyxlImage
from PIL import Image as PilImage

# 设置文件夹路径
image_folder = 'images/images_cut'

# 获取文件夹中的所有.json文件
json_files = [f for f in os.listdir(image_folder) if f.endswith('.json')]

# 字典存储每个类别及其对应的图像文件和裁剪信息
categories = {}

# 读取每个json文件并统计类别
for json_file in json_files:
    json_path = os.path.join(image_folder, json_file)
    with open(json_path, 'r') as f:
        data = json.load(f)
        image_name = data['imagePath']
        for shape in data['shapes']:
            label = shape['label']
            points = shape['points']
            if label not in categories:
                categories[label] = {'image': image_name, 'points': points}

# 创建一个新的Excel工作簿
wb = Workbook()
ws = wb.active

# 添加列标题
ws.append(['类别名', '图片'])

# 设置列宽
ws.column_dimensions['A'].width = 30
ws.column_dimensions['B'].width = 30

# 遍历每个类别并裁剪图像，插入到Excel中
for i, (label, info) in enumerate(categories.items(), start=1):
    image_path = os.path.join(image_folder, info['image'])
    points = info['points']
    x1, y1 = points[0]
    x2, y2 = points[1]

    # 裁剪图像
    with PilImage.open(image_path) as img:
        cropped_img = img.crop((x1, y1, x2, y2))
        cropped_img_path = os.path.join(image_folder, f"cropped_{label.replace('/', '_')}.jpg")
        cropped_img.save(cropped_img_path)

        # 插入类别名和裁剪后的图像到Excel中
        img = OpenpyxlImage(cropped_img_path)
        cell = f'B{i+1}'
        ws.add_image(img, cell)
        ws[f'A{i+1}'] = label

# 保存Excel文件
output_file = 'categories_with_images.xlsx'
wb.save(output_file)

print(f"Excel文件已生成并保存为{output_file}")
