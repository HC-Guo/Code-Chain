import json

# JSON文件路径
file_path = '/data/hongcheng_guo/JJ/Codechain/dataset/instructions/instruction_task3.json'

# 打开JSON文件并加载数据
with open(file_path, 'r') as f:
    data = json.load(f)

# 现在，变量data包含了JSON文件中的数据，它通常是一个字典或列表
# 可以对data进行进一步的操作

# 示例：访问JSON数据中的特定信息
for item in data:
    print(item["instruction"]) 
    print(item["output"])
 