import abc
import six

from . import config
from .utils import get_config_dict


@six.add_metaclass(abc.ABCMeta)
class SpiderBase(object):
    """
    爬虫基类

    用以作为抽象类定义爬虫扩展所需提供的服务接口

    包括：

    1. 爬虫注册
    2. 爬虫调用
    3. 打包格式化
    """

    def __init__(self, *args, **kwargs):
        """
        初始化默认配置参数，可在子类中进行覆盖

        配置优先级为：``用户元数据`` > ``具体Package配置`` > ``Common全局默认配置``

        :param dict usermeta: （*可选*，关键字参数）指定用户的package相关配置元数据，
            如：定制书籍名(book_title)等
        """
        # 设置全局默认配置
        self.options = get_config_dict(config)

        # 依照优先级，逐级更新 options 数据，具体Spider配置，用户元数据
        custom_opts = self.hook_custom_options()
        if not isinstance(custom_opts, dict):
            raise TypeError('hook_custom_options 返回值类型错误：{}'.format(
                type(custom_opts)))
        self.__configure(custom_opts)
        self.__configure(kwargs.pop('usermeta', {}))

    def __configure(self, options):
        """
        更新自定义配置

        该方法用于更新配置信息，Package开发者可在实现具体类时在 ``__init__`` 中进行调用，
        从而覆盖全局配置。

        另外，该方法会由MoEar服务在使用时主动调用，并传入具体Spider中的定制数据以及用户元数据，
        用于覆盖已有配置参数。
        """
        self.options.update(options)

    @abc.abstractmethod
    def hook_custom_options(self):
        """
        配置定制配置项钩子

        该方法返回当前类的自定义配置项，由基类在 ``__init__`` 方法中调用，
        调用点位于，Common默认全局配置完成后，用户元数据配置前

        :return: 返回当前类的自定义配置项
        :rtype: dict
        """

    @abc.abstractmethod
    def register(self, *args, **kwargs):
        """
        注册

        调用方可根据主键字段进行爬虫的创建或更新操作

        :return: 返回符合接口定义的字典数据
        :rtype: dict
        """

    @abc.abstractmethod
    def crawl(self, *args, **kwargs):
        """
        爬取

        执行爬取操作，并阻塞直到爬取完成，返回结果数据

        :return: 返回符合接口定义的字典数据
        :rtype: dict
        """

    @abc.abstractmethod
    def format(self, data, *args, **kwargs):
        """
        格式化

        将传入的Post列表数据进行格式化处理

        :param data: 待处理的文章列表
        :type data: list

        :return: 返回符合mobi打包需求的定制化数据结构
        :rtype: dict
        """


@six.add_metaclass(abc.ABCMeta)
class PackageBase(object):
    """
    打包基类

    用以作为抽象类定义打包驱动所需提供的服务接口
    """
    def __init__(self, spider, *args, **kwargs):
        """
        初始化默认配置参数，可在子类中进行覆盖

        配置优先级为：``用户元数据`` > ``Spider元数据`` >
        ``具体Package配置`` > ``Common全局默认配置``

        :param dict spider: 指定爬虫的信息数据(包括 'meta' 字段的元数据字典，
            其中需包含书籍名称用的时间戳)
        :param dict usermeta: （*可选*，关键字参数）指定用户的package相关配置元数据，
            如：定制书籍名(book_title)等
        """
        # 设置全局默认配置
        self.options = get_config_dict(config)

        # 依照优先级，逐级更新 options 数据，具体Package配置，Spider元数据，用户元数据
        custom_opts = self.hook_custom_options()
        if not isinstance(custom_opts, dict):
            raise TypeError('hook_custom_options 返回值类型错误：{}'.format(
                type(custom_opts)))
        self.__configure(custom_opts)
        self.__configure(spider.pop('meta', {}))
        self.__configure(kwargs.pop('usermeta', {}))

        # 赋值spider实例变量
        self.spider = spider

    def __configure(self, options):
        """
        更新自定义配置

        该方法用于更新配置信息，Package开发者可在实现具体类时在 ``__init__`` 中进行调用，
        从而覆盖全局配置。

        另外，该方法会由MoEar服务在使用时主动调用，并传入具体Spider中注册的元数据配置，
        用于覆盖已有配置参数。
        """
        self.options.update(options)

    @property
    def ext(self):
        '''
        输出文件的扩展名

        .. tip::

            可在 ``hook_custom_options`` 方法中，通过 **filename_extension** 键名
            来设置

        :return: 扩展名
        :rtype: str
        '''
        return self.options.get('filename_extension')

    @abc.abstractmethod
    def hook_custom_options(self):
        """
        配置定制配置项钩子

        该方法返回当前类的自定义配置项，由基类在 ``__init__`` 方法中调用，
        调用点位于，Common默认全局配置完成后，Spider元数据、用户元数据配置前

        :return: 返回当前类的自定义配置项
        :rtype: dict
        """

    @abc.abstractmethod
    def generate(self, data, *args, **kwargs):
        """
        生成

        根据传入的数据结构生成最终用于推送的文件字节字符串(bytes)，
        MoEar会将其持久化并用于之后的推送任务

        :param dict data: 待打包的数据结构
        :return: 返回生成的书籍打包输出字节
        :rtype: bytes
        """
