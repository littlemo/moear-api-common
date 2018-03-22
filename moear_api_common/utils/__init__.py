import os
import errno


def mkdirp(path):
    """
    创建传入的路径树

    Args:
        path (str):
            Path containing directories to create

    Returns:
        str: The passed in path

    Raises:
        OSError:
            If some underlying error occurs when calling :func:`os.makedirs`,
            that is not errno.EEXIST.
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

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
