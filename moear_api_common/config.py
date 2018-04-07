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

#: 打包输出文件的扩展名
filename_extension = 'mobi'

#: icon路径
icons_path = os.path.join(_assets_dir, 'icons')

#: 封面图片，留空则不会为书籍增加封面，size: ``600*800``。
#: 默认为随 ``moear-api-common`` 包附带的 **cv_default.jpg** 文件
img_cover = os.path.join(_images_path, 'cv_default.jpg')

#: 报头图片，size: 600*60。
#: 默认为随 ``moear-api-common`` 包附带的 **mh_default.jpg** 文件
img_masthead = os.path.join(_images_path, 'mh_default.gif')

#: 合并图书的封面图片，留空则将所有书籍封面贴在一起
# img_cover_bv = img_cover

#: 缩略图处理约束条件，小于等于 ``16KB``
img_max_thumb_size = 16 * 1024
#: 缩略图处理约束条件，尺寸小于等于 ``180*240``
img_max_thumb_dimen = (180, 240)
#: 缩小图片尺寸到 ``(Width, Height)``
img_reduce_to = (600, 800)

#: 是否将图片转换为灰度图，这将有利于显著减小输出文件的大小，建议在电纸书上阅读时开启
img_convert_to_gray = True

#: 基础样式文件。默认为随 ``moear-api-common`` 包附带的 **base.css** 文件
css_base = os.path.join(_css_path, 'base.css')

# feeds_title = 'MoEar'
# feeds_desc = 'RSS delivering from MoEar'

# 是否将中文文件名转换为拼音
# pinyin_filename = False

#: 是否为TOC条目生成简述
toc_desc_generate = True
#: TOC条目简述的字数限制
toc_desc_word_limit = 500

# TOC标题
# toc_title = 'Table Of Contents'

#: TOC描述是否包含图片，此功能暂未实现
toc_thumbnail_generate = False

# 切分长图为多个小图（图片高大于指定值）
# 当值为 None 或 0 时，此功能被关闭
# threshold_split_long_image = 750

# 截断超过字数限制的邮件主题字串
# subject_wordcnt_for_apmail = 16
