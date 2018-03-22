# -*- coding:utf-8 -*-
"""
Post打包系统默认配置项

将在注册加载时填充到系统全局配置中
"""
import os

_base_dir = os.path.dirname(os.path.abspath(__file__))
_assets_dir = os.path.join(_base_dir, 'assets')
_images_path = os.path.join(_assets_dir, 'images')
_css_path = os.path.join(_assets_dir, 'css')

# icon路径
common_icons_path = os.path.join(_assets_dir, 'icons')

# 封面图片，留空则不会为书籍增加封面，size: 600*800
img_cover = os.path.join(_images_path, 'cv_default.jpg')

# 报头图片，size: 600*60
img_masthead = os.path.join(_images_path, 'mh_default.gif')

# 合并图书的封面图片，留空则将所有书籍封面贴在一起
img_cover_bv = img_cover

# 基础样式文件
css_base = os.path.join(_css_path, 'base.css')

feeds_title = 'MoEar'
feeds_desc = 'RSS delivering from MoEar'

# 是否将中文文件名转换为拼音
pinyin_filename = False

# 是否为TOC条目生成简述
toc_desc_generate = True
toc_desc_word_limit = 500

# TOC标题
toc_title = 'Table Of Contents'

# TOC描述是否包含图片
toc_thumbnail_generate = True

# 是否将图片转换为灰度图，这将有利于显著减小输出文件的大小，建议在电纸书上阅读时开启
color_to_gray = True

# 切分长图为多个小图（图片高大于指定值）
# 当值为 None 或 0 时，此功能被关闭
threshold_split_long_image = 750

# 缩小图片尺寸到 (Width, Height)
reduce_image_to = None  # (600, 800)

# 截断超过字数限制的邮件主题字串
subject_wordcnt_for_apmail = 16
