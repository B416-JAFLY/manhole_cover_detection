import os
import re

def process_files(directory):
    # 获取目录下所有的 .txt 文件
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    for file in files:
        filepath = os.path.join(directory, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        processed_lines = []
        for line in lines:
            # 使用正则表达式去除类别后面的中文
            processed_line = re.sub(r'(\d+)-[^\s]+', r'\1', line)
            processed_lines.append(processed_line)
        
        # 将处理后的内容写回文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(processed_lines)

# 设置你要处理的目录路径
directory_path = 'images/images_cut'
process_files(directory_path)
