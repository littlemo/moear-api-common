import os
import sys
import logging
import unittest

from moear_api_common import utils
from moear_api_common.utils import img
from moear_api_common import config


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(message)s")  # output format
sh = logging.StreamHandler(stream=sys.stdout)  # output to standard output
sh.setFormatter(format)
log.addHandler(sh)

_base_dir = os.path.dirname(os.path.abspath(__file__))
_assets_dir = os.path.join(_base_dir, 'assets')
_build_dir = os.path.join(_base_dir, 'build')


class TestUtilsImgMethods(unittest.TestCase):
    """
    测试工具包中img的工具方法
    """
    def test_000_rescale_image(self):
        """测试调整图片工具方法"""
        raw_path = os.path.join(_assets_dir, 'raw.jpg')
        with open(raw_path, 'rb') as fh:
            raw_img_buf = fh.read()
        data = img.rescale_image(
            raw_img_buf,
            dimen=config.img_max_thumb_dimen,
            maxsizeb=config.img_max_thumb_size)
        output_path = os.path.join(_build_dir, 'rescale.jpg')
        utils.mkdirp(_build_dir)
        with open(output_path, 'wb') as fh:
            fh.write(data)

    def test_100_gray_image(self):
        '''测试灰度图片处理的工具方法'''
        raw_path = os.path.join(_assets_dir, 'raw.jpg')
        with open(raw_path, 'rb') as fh:
            raw_img_buf = fh.read()
        data = img.gray_image(raw_img_buf)
        output_path = os.path.join(_build_dir, 'gray.jpg')
        utils.mkdirp(_build_dir)
        with open(output_path, 'wb') as fh:
            fh.write(data)
