import os


def find_kindlegen_prog(path=None):
    '''
    获取kindlegen程序路径

    该方法会检索系统 ``PATH`` 路径，查找包含 ``kindlegen`` 文件的路径，
    并返回该文件的绝对路径。若不存在则返回 ``None``

    .. attention::

        检索 ``PATH`` 路径前，会优先寻找指定路径，并在检索到第一个符合文件后立刻返回

    :param str path: 关键字参数，若传入，则优先检测该路径下是否存在 kindlegen 程序
    :return: kindlegen的绝对路径
    :rtype: str
    '''
    try:
        kindlegen_prog = 'kindlegen'

        # search in current directory and PATH to find kinglegen
        path_list = [path]
        path_list.extend(os.getenv('PATH').split(':'))
        for p in path_list:
            if p:
                fname = os.path.join(p, kindlegen_prog)
                if os.path.exists(fname):
                    return fname
        return None
    except Exception:
        return None
