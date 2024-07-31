# Arcaea Files Structure Check
# Arcaea文件结构检查
`ArcaeaCheck`

> [!IMPORTANT]  
> 使用前请先使用 `Visual Studio Code` 内的 [vscode-arcaea-file-format](https://github.com/yojohanshinwataikei/vscode-arcaea-file-format) 插件对 songlist 以及 packlist 文件内的**错误**和**警告**进行**修正**并且**格式化**。

# 文件结构定义

```
root/
├── songs/
│   ├── pack/
│   │   ├── select_base.png
│   │   └── ...
│   ├── ignotusafterburn/
│   │   ├── 2.aff
│   │   ├── base.jpg
│   │   ├── base_256.jpg
│   │   ├── base.ogg
│   │   └── ...
│   ├── songlist
│   ├── packlist
│   └── ...
├── img/
│   ├── bg/
│   │   ├── base_conflict.jpg
│   │   ├── base_light.jpg
│   │   └── ...
│   └── ...
├── add_idx.py
├── ArcaeaCheck.py
└── ...
```

# 功能

## `ArcaeaCheck.py`：

- 检查 songlist 中 `"id"` 值是否存在重复。
- 检查 songs 文件夹内是否缺少 songlist 中 `"id"` 值对应的文件夹。
    - 检查文件夹内是否存在 base.jpg、base.ogg、base_256.jpg 三个文件。
- 检查 songlist 中 `"set"` 值是否存在于 packlist 的 `"id"` 值中。（忽略值为 `"single"` 的情况）
- 检查 songlist 中的 `"bg"` 值是否在 bg 文件夹中存在对应的图片文件。
- 检查 packlist 中的 `"id"` 值是否在 pack 文件夹中存在对应的图片文件。
- 检查 songlist 内每首歌的 `"difficulties"` 下是否都存在 `"ratingClass"` 值为 `0`, `1`, `2` 的三个子代码块。
- 若 `"difficulties"` 中存在 `"ratingClass": 3`，检查对应文件夹内是否存在 3.aff 文件。
    - 若不存在 `"ratingClass": 3` ，检查其对应文件夹内是否存在 2.aff 文件。
- 检查 `"title_localized"` 下是否存在 `"en"` 项并且值为空。
- 若存在 `"source_localized"`，检查值是否为空。
- 检查 `"version"` 的值是否为空值。
    > 存在空值会导致在选择全曲时程序出错退出
- 检查 `"date"` 的值是否为十位数字时间戳。

## `add_idx.py`

> [!NOTE]  
> 若需删除`"idx"` 行，请善用[正则表达式](https://regexr-cn.com/)进行替换删除。

- 按照 songlist 内的顺序在每首歌的代码块头部加入 `"idx"` 值。
    > 该值存在与否仅影响 Link Play 功能，不会影响主程序。

