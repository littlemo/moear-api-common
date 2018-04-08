from io import BytesIO
from PIL import Image


def rescale_image(
        data, maxsizeb=4000000, dimen=None,
        png2jpg=False, graying=True, reduceto=(600, 800)):
    '''
    若 ``png2jpg`` 为 ``True`` 则将图片转换为 ``JPEG`` 格式，所有透明像素被设置为
    *白色* 。确保结果图片尺寸小于 ``maxsizeb`` 的约束限制。

    如果 ``dimen`` 不为空，则生成一个相应约束的缩略图。依据 ``dimen`` 的类型，设置约束为
    ``width=dimen, height=dimen`` 或者 ``width, height = dimen``

    :param data: 原始图片字节数据
    :type data: bytes or io.BytesIO
    :param int maxsizeb: 文件大小约束，单位：字节
    :param dimen: 缩略图尺寸约束，宽&高
    :type dimen: int or (int, int)
    :param bool png2jpg: 是否将图片转换为 JPG 格式
    :param bool graying: 是否将图片进行灰度处理
    :param reduceto: 若图片大于此约束则进行相应缩小处理，宽&高
    :type reduceto: (int, int)
    :return: 处理后的图片字节数据，可直接以 ``wb`` 模式输出到文件中
    :rtype: bytes
    '''
    if not isinstance(data, BytesIO):
        data = BytesIO(data)
    img = Image.open(data)
    width, height = img.size
    fmt = img.format
    if graying and img.mode != "L":
        img = img.convert("L")

    reducewidth, reduceheight = reduceto

    if dimen is not None:
        if hasattr(dimen, '__len__'):
            width, height = dimen
        else:
            width = height = dimen
        img.thumbnail((width, height))
        if png2jpg and fmt == 'PNG':
            fmt = 'JPEG'
        data = BytesIO()
        img.save(data, fmt)
    elif width > reducewidth or height > reduceheight:
        ratio = min(
            float(reducewidth) / float(width),
            float(reduceheight) / float(height))
        img = img.resize((
            int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
        if png2jpg and fmt == 'PNG':
            fmt = 'JPEG'
        data = BytesIO()
        img.save(data, fmt)
    elif png2jpg and fmt == 'PNG':
        data = BytesIO()
        img.save(data, 'JPEG')
    else:
        data = BytesIO()
        img.save(data, fmt)

    return data.getvalue()


def gray_image(data):
    '''
    灰度化图片

    将传入的图片数据转换为灰度图后返回

    :param data bytes: 图片字节数据，可通过以 ``rb`` 模式读取图片文件获得
    :return: 处理后的图片字节数据，可直接以 ``wb`` 模式输出到文件中
    :rtype: bytes
    '''
    if not isinstance(data, BytesIO):
        data = BytesIO(data)
    img = Image.open(data)
    fmt = img.format
    if img.mode != "L":
        img = img.convert("L")
    data = BytesIO()
    img.save(data, fmt)
    return data.getvalue()
