import os


def mkdirp(path):
    """
    创建传入的路径

    该方法为一个串联调用方法，仅对 :func:`os.makedirs` 做了简单封装。

    推荐用法::

        path_created = mkdirp(path)  # 赋值路径的同时确保其已被创建

    用例:

    >>> from moear_api_common.utils import mkdirp
    >>> mkdirp('build/doctest/test_path')
    'build/doctest/test_path'

    :param str path: 待创建路径
    :return: 创建完成的路径
    :rtype: str
    :raises OSError: 调用 :func:`os.makedirs` 时发生的异常，若路径已存在则不抛出异常
    """
    os.makedirs(path, exist_ok=True)
    return path


def get_config_dict(config):
    '''
    获取配置数据字典

    对传入的配置包进行格式化处理，生成一个字典对象

    :param object config: 配置模块
    :return: 配置数据字典
    :rtype: dict
    '''
    dst = {}
    tmp = config.__dict__
    key_list = dir(config)
    key_list.remove('os')
    for k, v in tmp.items():
        if k in key_list and not k.startswith('_'):
            dst[k] = v
    return dst
