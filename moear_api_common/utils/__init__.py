import os


def mkdirp(path):
    """
    创建传入的路径

    该方法为一个串联调用方法，仅对 :func:`os.makedirs` 做了简单封装。

    推荐用法::

        path_created = mkdirp(path)  # 赋值路径的同时确保其已被创建

    用例:

    >>> from moear_api_common.utils import mkdirp
    >>> mkdirp('test_file')
    'test_file'

    :param str path: 待创建路径
    :return: 创建完成的路径
    :rtype: str
    :raises OSError: 调用 :func:`os.makedirs` 时发生的异常，若路径已存在则不抛出异常
    """
    os.makedirs(path, exist_ok=True)
    return path


def get_config_dict(config):
    dst = {}
    tmp = config.__dict__
    key_list = dir(config)
    key_list.remove('os')
    for k, v in tmp.items():
        if k in key_list and not k.startswith('_'):
            dst[k] = v
    return dst
