import abc
import six


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
