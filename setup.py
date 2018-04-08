from setuptools import setup, find_packages


setup(
    name='moear-api-common',
    url='https://github.com/littlemo/moear-api-common',
    author='moear developers',
    author_email='moore@moorehy.com',
    maintainer='littlemo',
    maintainer_email='moore@moorehy.com',
    version='1.0.2.post1',
    description='为MoEar扩展插件提供接口定义以及通用组件',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='moear api',
    packages=find_packages(exclude=('docs', 'tests*')),
    include_package_data=True,
    zip_safe=False,
    license='GPLv3',
    python_requires='>=3',
    project_urls={
        'Documentation': 'http://moear-api-common.rtfd.io/',
        'Source': 'https://github.com/littlemo/moear-api-common',
        'Tracker': 'https://github.com/littlemo/moear-api-common/issues',
    },
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
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Email',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Internet',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
