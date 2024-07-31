import re
import os

# 定义 songlist 文件路径
songlist_path = './songs/songlist'

# 读取 songlist 文件
with open(songlist_path, "r", encoding="utf-8") as file:
    json_data = file.read()


# 使用正则表达式匹配每个 "id" 之前的位置并插入索引
def add_index(json_string):
    pattern = r'(\s*{)(?=\s*"id":)'  # 匹配 `{` 后面的 `"id":`，不包含后者
    matches = list(re.finditer(pattern, json_string))
    offset = 0

    for i, match in enumerate(matches, start=1):
        index_str = f'\n      "idx": {i},'
        position = match.end() + offset  # 插入到 `{` 的下一行
        json_string = json_string[:position] + index_str + json_string[position:]
        offset += len(index_str)

    return json_string


# 更新后的 JSON 数据
updated_json = add_index(json_data)

# 创建原文件的备份
backup_path = songlist_path + '.bak'
os.rename(songlist_path, backup_path)

# 将结果写入到原文件中
with open(songlist_path, "w", encoding="utf-8") as output_file:
    output_file.write(updated_json)

print(f"索引已成功添加，备份已创建为 {backup_path}，并将更新后的数据写入到 {songlist_path} 文件中。")
