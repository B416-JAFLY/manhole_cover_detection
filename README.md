# 井盖检测
使用yolo和resnet50实现的井盖检测与分类，通过yolo检测出图片中井盖，然后通过resnet50对井盖功能区与单位进行分类
## 数据集
单位区命名为{0-单位名}，功能区命名为{1-功能名}
## 数据集构建
./dataset_construction
## 模型训练与推理
./model_training_inference