from io import BytesIO
from PIL import Image


def rescale_image(
        data, maxsizeb=4000000, dimen=None,
        png2jpg=False, graying=True, reduceto=(600, 800)):
    '''
    Convert image setting all transparent pixels to white and changing format
    to JPEG. Ensure the resultant image has a byte size less than
    maxsizeb.

    If dimen is not None, generate a thumbnail of
    width=dimen, height=dimen or width, height = dimen (depending on the type
    of dimen)

    Returns the image as a bytestring.
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
