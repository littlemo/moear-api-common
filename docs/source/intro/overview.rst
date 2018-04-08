.. _intro-overview:

====
概览
====

该项目的目的为给 `MoEar`_ 服务提供接口的定义及常用工具方法的实现。

故该项目本身结构极其简单，下面分别从 :ref:`sec-interface-define` 和 :ref:`sec-utils` 两方面进行说明。


安装方法
========

您可以通过 ``pip`` 进行安装，本包仅在 ``Python 3.X`` 下测试通过::

    pip install moear-api-common


.. _sec-interface-define:

接口定义
========

为了增强 `MoEar`_ 的可扩展性，在实现时，基于 OpenStack 项目中的 `stevedore`_ 包，
实现了扩展两个扩展插件机制，分别用于实现 **爬虫** 与 **打包** 功能的扩展。

`MoEar`_ 在运行时会根据相应逻辑，加载相应的爬虫、打包实现，从而实现松耦合、可扩展。
同时我也分别实现了一个爬虫与一个打包工具，用以使 `MoEar`_ 可以正常完成整个业务流程，
亦可作为一个例子，给有能力的小伙伴儿提供一个 DIY 的参考例程。

接口定义在 ``base.py`` 文件中，共提供两种接口，分别为

1. 爬虫接口： :class:`.SpiderBase` ，用于定义一个扩展文章爬虫需要实现的所有方法
2. 打包接口： :class:`.PackageBase` ，用于定义一个扩展打包工具需要实现的所有方法

爬虫接口
--------

爬虫插件的业务流程为，当 `MoEar`_ 服务启动时，会遍历所有 *setup.py* 中
``entry_points`` 含有 ``moear.spider`` 入口的 Python 包，并调用其
:meth:`.SpiderBase.register` 方法，将返回字典持久化到 DB 中。

`MoEar`_ 服务会根据具体 Spider 注册时配置中提供的爬取策略（爬取时间、随机延迟范围等）
创建计划任务，待任务触发时，调用相应 Spider 插件的 :meth:`.SpiderBase.crawl` 方法，
执行爬取操作，并等待结果返回后，将其持久化到 DB 中。

.. attention::

    此处 `MoEar`_ 会开启基于 `Celery`_ 的分布式消息队列，并在独立进程中调用相关接口

获取到爬取结果数据后， `MoEar`_ 会在执行打包任务前，
将从 DB 中获取相应文章数据 & 元数据，生成同 :meth:`.SpiderBase.crawl`
返回的相同格式的数据结构作为入参，调用 :meth:`.SpiderBase.format` 方法，

.. note::

    具体数据结构，内容，格式，配置项信息，将在稍后参考例程中作详细阐述。

打包接口
--------

打包插件的业务流程很简单，目前只提供了一个业务方法定义 :meth:`.PackageBase.generate` 。
该方法将完成对传入数据结构的处理，如将文章内容中的 ``img`` 下载到本地，文章内容保存到文件，
并最终打包成相应设备支持的电子书格式，如：``mobi`` ， ``epub`` 等。稍后我将实现 **Kindle**
上最常用的 ``mobi`` 格式打包插件，用以作为参考例程。

`MoEar`_ 对打包插件的获取流程为，会遍历所有 *setup.py* 中
``entry_points`` 含有 ``moear.package`` 入口的 Python 包。

.. attention::

    此接口的调用环境与上述 :meth:`.SpiderBase.crawl` :meth:`.SpiderBase.format`
    相同，会在基于 `Celery`_ 的分布式消息队列的独立进程中调用被调用

.. note::

    具体数据结构，内容，格式，配置项信息，将在稍后参考例程中作详细阐述。

配置说明
--------

当前支持的配置参数主要用于控制打包行为，具体参见 :ref:`topics-configure`


.. _sec-utils:

常用工具
========

目前提供的工具主要分三块：

#. 系统操作
#. kindlegen支持
#. 图片处理

具体接口说明参见 :ref:`topics-utils`


.. _MoEar: https://github.com/littlemo/moear
.. _stevedore: https://docs.openstack.org/stevedore/latest/
.. _Celery: https://github.com/celery/celery
