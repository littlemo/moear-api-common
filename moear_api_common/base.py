import abc
import six
import re

from . import config


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
        dst = {}
        tmp = config.__dict__
        key_list = dir(config)
        key_list.remove('os')
        for k, v in tmp.items():
            if k in key_list and not k.startswith('__'):
                dst[k] = v
        self.settings = dst

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

    def insert_toc(
            self, oeb, sections, toc_thumbnails,
            insertHtmlToc=True, insertThumbnail=True):
        """
        插入OEB目录

        此处移植的 KindleEar 中相关工具方法，再次感谢原作者。

        此工具方法用于创建 OEB 的两级目录。

        :params oeb: 待操作的 OEB 对象
        :params sections dict: 待操作的书籍数据结构有序字典，
            值为元组 (title, brief, humbnail, content)
        :params toc_thumbnails dict: key为图片原始URL，value为其在 OEB 内的 href
        :params insertHtmlToc bool: 是否插入 HTML 目录
        :params insertThumbnail bool: 是否插入缩略图
        """
        toc_title = self.settings.get('toc_title')
        css_pat = r'<style type="text/css">(.*?)</style>'
        css_ex = re.compile(css_pat, re.M | re.S)
        body_pat = r'(?<=<body>).*?(?=</body>)'
        body_ex = re.compile(body_pat, re.M | re.S)

        num_articles = 1
        num_sections = 0

        ncx_toc = []
        # html_toc_2 secondary toc
        html_toc_2 = []
        name_section_list = []
        for sec in sections.keys():
            css = [
                '.pagebreak{page-break-before:always;}h1{font-size:2.0em;}h2{'
                'font-size:1.5em;}h3{font-size:1.4em;}h4{font-size:1.2em;}h5{'
                'font-size:1.1em;}h6{font-size:1.0em;}']
            html_content = []
            secondary_toc_list = []
            first_flag = False
            sec_toc_thumbnail = None
            for title, brief, thumbnail, content in sections[sec]:
                # 获取自定义的CSS
                for css_obj in css_ex.finditer(content):
                    if css_obj and css_obj.group(1):
                        if css_obj.group(1) not in css:
                            css.append(css_obj.group(1))

                if first_flag:
                    # insert anchor && pagebreak
                    html_content.append(
                        '<div id="%d" class="pagebreak">' % (num_articles))
                else:
                    # insert anchor && pagebreak
                    html_content.append('<div id="%d">' % (num_articles))
                    first_flag = True
                    if thumbnail:
                        sec_toc_thumbnail = thumbnail  # url

                # 将body抽取出来
                body_obj = re.search(body_ex, content)
                if body_obj:
                    # insect article
                    html_content.append(body_obj.group() + '</div>')
                    secondary_toc_list.append(
                        (title, num_articles, brief, thumbnail))
                    num_articles += 1
                else:
                    html_content.pop()
            html_content.append('</body></html>')

            html_content.insert(
                0, '<html><head><title>%s</title><style type="text/css">%s</st'
                'yle></head><body>' % (sec, ''.join(css)))

            # add section.html to maninfest and spine
            # We'd better not use id as variable.
            # It's a python builtin function.
            id_, href = oeb.manifest.generate(
                id='feed', href='feed%d.html' % num_sections)
            item = oeb.manifest.add(
                id_, href, 'application/xhtml+xml', data=''.join(html_content))
            oeb.spine.add(item, True)

            # 在目录分类中添加每个目录下的文章篇数
            sec_with_num = '%s (%d)' % (sec, len(sections[sec]))
            # Sections name && href && no brief
            ncx_toc.append(
                ('section', sec_with_num, href, '', sec_toc_thumbnail))

            # generate the secondary toc
            if insertHtmlToc:
                html_toc_ = [
                    '<html><head><title>toc</title></head>'
                    '<body><h2>%s</h2><ol>' % (sec_with_num)]
            for title, anchor, brief, thumbnail in secondary_toc_list:
                if insertHtmlToc:
                    html_toc_.append(
                        '&nbsp;&nbsp;&nbsp;&nbsp;<li><a href="%s#%d">%s</a>'
                        '</li><br />' % (href, anchor, title))
                # article name & article href && article brief
                ncx_toc.append((
                    'article', title, '%s#%d' % (href, anchor),
                    brief, thumbnail))
            if insertHtmlToc:
                html_toc_.append('</ol></body></html>')
                html_toc_2.append(html_toc_)
                name_section_list.append(sec_with_num)

            num_sections += 1

        if insertHtmlToc:
            # Generate HTML TOC for Calibre mostly
            # html_toc_1 top level toc
            html_toc_1 = [
                u'<html><head><title>Table Of Contents</title></head><body>'
                '<h2>%s</h2><ul>' % (toc_title)]
            html_toc_1_ = []
            # We need index but not reversed()
            for a in range(len(html_toc_2) - 1, -1, -1):
                # Generate Secondary HTML TOC
                id_, href = oeb.manifest.generate(
                    id='section', href='toc_%d.html' % (a))
                item = oeb.manifest.add(
                    id_, href, 'application/xhtml+xml',
                    data=" ".join(html_toc_2[a]))
                oeb.spine.insert(0, item, True)
                html_toc_1_.append(
                    '&nbsp;&nbsp;&nbsp;&nbsp;<li><a href="%s">%s</a>'
                    '</li><br />' % (href, name_section_list[a]))
            html_toc_2 = []
            for a in reversed(html_toc_1_):
                html_toc_1.append(a)
            html_toc_1_ = []
            html_toc_1.append('</ul></body></html>')
            # Generate Top HTML TOC
            id_, href = oeb.manifest.generate(id='toc', href='toc.html')
            item = oeb.manifest.add(
                id_, href, 'application/xhtml+xml', data=''.join(html_toc_1))
            oeb.guide.add('toc', 'Table of Contents', href)
            oeb.spine.insert(0, item, True)

        # Generate NCX TOC for Kindle
        po = 1
        toc = oeb.toc.add(str(
            oeb.metadata.title[0]), oeb.spine[0].href,
            id='periodical', klass='periodical', play_order=po)
        po += 1
        for ncx in ncx_toc:
            insertThumbnail = False
            if insertThumbnail and ncx[4]:
                toc_thumbnail = toc_thumbnails[ncx[4]]
            else:
                toc_thumbnail = None

            if ncx[0] == 'section':
                sectoc = toc.add(str(
                    ncx[1]), ncx[2], klass='section',
                    play_order=po, id='Main-section-%d' % po,
                    toc_thumbnail=toc_thumbnail)
            elif sectoc:
                sectoc.add(str(
                    ncx[1]), ncx[2], description=ncx[3] if ncx[3] else None,
                    klass='article', play_order=po,
                    id='article-%d' % po, toc_thumbnail=toc_thumbnail)
            po += 1

    @abc.abstractmethod
    def generate(self, data, spider, usermeta, *args, **kwargs):
        """
        生成
        ----

        根据传入的数据结构生成最终用于推送的文件字节字符串对象(byteStringIO)，
        MoEar会将其持久化并用于之后的推送任务

        :params data dict: 待打包的数据结构
        :params spider dict: 指定爬虫的信息数据(包括 'meta' 字段的元数据字典，
            其中需包含书籍名称用的时间戳)
        :params usermeta dict: 指定用户的package相关配置元数据
        :returns: byteStringIO, 返回生成的书籍打包输出对象
        """
