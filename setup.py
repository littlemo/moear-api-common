from setuptools import setup, find_packages


setup(
    name='moear-api-common',
    url='https://github.com/littlemo/moear-api-common',
    author='moear developers',
    author_email='moore@moorehy.com',
    maintainer='littlemo',
    maintainer_email='moore@moorehy.com',
    version='1.0.0',
    description='为MoEar扩展插件提供接口定义以及通用组件',
    long_description=open('docs/source/intro/overview.rst').read(),
    keywords='moear scrapy api',
    packages=find_packages(exclude=('docs', 'tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    license='GPLv3',
    provides=[
        'moear.api',
    ],
    install_requires=[
        'six~=1.11.0',
        'Pillow~=5.0.0',
    ],
    entry_points={},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
