import abc
import six

import config


@six.add_metaclass(abc.ABCMeta)
class SpiderBase(object):
    """
    爬虫基类
    ========

    用以作为抽象类定义爬虫扩展所需提供的服务接口

    包括：

    1. 爬虫注册
    2. 爬虫调用
    3. 打包格式化
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def register(self, *args, **kwargs):
        """
        注册
        ----

        调用方可根据主键字段进行爬虫的创建或更新操作

        :returns: dict, 返回符合接口定义的字典数据
        """

    @abc.abstractmethod
    def crawl(self, *args, **kwargs):
        """
        爬取
        ----

        执行爬取操作，并阻塞直到爬取完成，返回结果数据

        :returns: dict, 返回符合接口定义的字典数据
        """

    @abc.abstractmethod
    def format(self, data, *args, **kwargs):
        """
        格式化
        ------

        将传入的Post列表数据进行格式化处理

        :param data: 待处理的文章列表
        :type data: list

        :returns: dict, 返回符合mobi打包需求的定制化数据结构
        """


@six.add_metaclass(abc.ABCMeta)
class PackageBase(object):
    """
    打包基类
    ========

    用以作为抽象类定义打包驱动所需提供的服务接口
    """
    def __init__(self, *args, **kwargs):
        """
        初始化默认配置参数，可在子类中进行覆盖
        """
        self.settings = dict(config)

    def configure(self, settings):
        """
        更新自定义配置
        --------------

        该方法用于更新配置信息，Package开发者可在实现具体类时在 `__init__` 中进行调用，
        从而覆盖全局配置。

        另外，该方法会由MoEar服务在使用时主动调用，并传入具体Spider中注册的元数据配置，
        用于覆盖已有配置参数。

        即优先级为：Spider自定义 > 具体Package配置 > Package全局默认配置
        """
        self.settings.update(settings)

    @abc.abstractmethod
    def generate(self, data, *args, **kwargs):
        """
        生成
        ----

        根据传入的数据结构生成最终用于推送的文件字节字符串对象(byteStringIO)，
        MoEar会将其持久化并用于之后的推送任务

        :params data dict: 待打包的数据结构
        :returns: byteStringIO, 返回生成的书籍打包输出对象
        """
