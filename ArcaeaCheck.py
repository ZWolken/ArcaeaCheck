import json
import os
import re

# 定义文件路径
songlist_path = './songs/songlist'  # songlist 文件路径
packlist_path = './songs/packlist'  # packlist 文件路径
songs_directory = './songs'         # songs 文件夹路径
img_bg_folder = './img/bg'          # bg 文件夹路径
pack_directory = './songs/pack'     # pack 文件夹路径

# 加载 songlist 文件
with open(songlist_path, 'r', encoding='utf-8') as file:
    songlist_data = json.load(file)

# 加载 packlist 文件
with open(packlist_path, 'r', encoding='utf-8') as file:
    packlist_data = json.load(file)

# 初始化数据容器
song_ids = set()
bg_filenames = []

# 检查背景文件夹存在性
if not os.path.isdir(img_bg_folder):
    print(f"bg 文件夹 {img_bg_folder} 不存在，请检查路径。")

if not os.path.isdir(pack_directory):
    print(f"pack 文件夹 {pack_directory} 不存在，请检查路径。")

# 提取歌曲 id 和背景文件名
for song in songlist_data['songs']:
    song_id = song['id']
    bg_filename = song['bg']

    # 检查 songlist 中的重复 id
    if song_id in song_ids:
        print(f"songlist \"id\"：\"{song_id}\" 存在重复")
    else:
        song_ids.add(song_id)

    # 检查歌曲 ID 是否有对应的文件夹
    song_folder_path = os.path.join(songs_directory, song_id)
    if not os.path.isdir(song_folder_path):
        print(f"songlist \"id\": \"{song_id}\" 未在 songs 文件夹内找到对应文件夹")
    else:
        # 检查歌曲文件夹内是否存在 base.jpg、base.ogg、base_256.jpg 文件
        required_files = ['base.jpg', 'base.ogg', 'base_256.jpg']
        for file in required_files:
            file_path = os.path.join(song_folder_path, file)
            if not os.path.isfile(file_path):
                print(f"在 {song_id} 文件夹内，缺少文件：{file}")

    # 检查 ratingClass 3 并验证 3.aff 文件的存在
    has_rating_class_3 = False
    has_rating_class_0_1_2 = {0: False, 1: False, 2: False}  # 用于检查 ratingClass 0, 1, 2 的存在
    rating_class_set = set()  # 用于检查重复的 ratingClass

    for difficulty in song['difficulties']:
        rating_class = difficulty['ratingClass']

        if rating_class in rating_class_set:
            print(f"歌曲 id {song_id} 的 ratingClass {rating_class} 重复")
        else:
            rating_class_set.add(rating_class)

        if rating_class == 3:
            has_rating_class_3 = True
            aff_file_path = os.path.join(song_folder_path, '3.aff')
            if not os.path.isfile(aff_file_path):
                print(f"songlist \"id\": \"{song_id}\" 存在 \"ratingClass\": 3，但在对应文件夹内缺少 3.aff 文件")

        # 检查 ratingClass 0, 1, 2
        if rating_class in has_rating_class_0_1_2:
            has_rating_class_0_1_2[rating_class] = True

    # 输出缺少 ratingClass 0, 1, 2 的信息
    missing_classes = [str(cls) for cls, exists in has_rating_class_0_1_2.items() if not exists]
    if missing_classes:
        print(f"songlist \"id\": \"{song_id}\" 缺少 \"ratingClass\": {', '.join(missing_classes)}")

    # 在 songlist 中不存在 ratingClass 3 时检查 2.aff 文件
    if not has_rating_class_3:
        aff_file_path = os.path.join(song_folder_path, '2.aff')
        if not os.path.isfile(aff_file_path):
            print(f"songlist \"id\": \"{song_id}\"，无 \"ratingClass\": 3，并在对应文件夹内缺少 2.aff 文件")

    # 检查 title_localized 是否包含非空的 en
    if 'en' not in song['title_localized'] or not song['title_localized']['en']:
        print(f"songlist \"id\": \"{song_id}\"，\"title_localized\" 缺少 \"en\" 或为空")

    # 检查 source_localized 是否存在并包含非空的 en
    if 'source_localized' in song:
        if 'en' not in song['source_localized'] or not song['source_localized']['en']:
            print(f"songlist \"id\": \"{song_id}\"，\"source_localized\" 缺少 \"en\" 或为空")

    # 检查 version 是否为空
    if not song['version'].strip():
        print(f"songlist \"id\": \"{song_id}\"，\"version\" 值为空")

    # 检查 date 是否为十位数字时间戳
    if not re.match(r'^\d{10}$', str(song['date'])):
        print(f"songlist \"id\": \"{song_id}\"，\"date\" 值不是十位数字时间戳")

    # 将背景文件名加入列表用于检查
    bg_filenames.append((bg_filename, song_id))  # 记录背景文件名和对应的 id

# 提取 packlist 中的 pack id 以进行 set 验证
pack_ids = {pack['id'] for pack in packlist_data['packs']}

# 验证 songlist 中的 set 是否在 packlist 中存在，忽略 single 值
for song in songlist_data['songs']:
    song_set = song['set']
    song_id = song['id']

    if song_set != 'single' and song_set not in pack_ids:
        print(f"packlist \"id\": \"{song_set}\" 不存在 (songlist id：\"{song_id}\")")

# 检查 bg 文件的存在性
for bg_filename, song_id in bg_filenames:
    bg_file_exists = any(
        os.path.isfile(os.path.join(img_bg_folder, f"{bg_filename}.{ext}"))
        for ext in ['jpg']
        # for ext in ['jpg', 'jpeg', 'png', 'bmp', 'gif']
    )
    if not bg_file_exists:
        print(f"songlist \"id\": \"{song_id}\",\"bg\": \"{bg_filename}\"，未在 bg 文件夹内找到对应的文件")

# 检查 packlist 中 pack ID 文件的存在性
for pack in packlist_data['packs']:
    pack_id = pack['id']
    pack_file_exists = any(
        os.path.isfile(os.path.join(pack_directory, f"select_{pack_id}.{ext}"))
        for ext in ['png']
        # for ext in ['jpg', 'jpeg', 'png', 'bmp', 'gif']
    )
    if not pack_file_exists:
        print(f"packlist \"id\": \"{pack_id}\"，未在 pack 文件夹中找到对应的图片文件")

# 输出检查完成信息
print("检查完成。")
