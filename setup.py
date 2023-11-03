# -*- coding: utf-8 -*-

from distutils.core import setup
setup(
    name = 'retryCommand',
    version = '0.0.1',
    keywords = [],
    description = 'It is a Python library that allows you to retry executing a command multiple times until it succeeds or reaches the maximum number of retries. It provides options to customize the behavior of retries, such as setting a timeout for each execution and specifying the return codes that indicate success.',
    long_description = open("README.md","r",encoding="utf-8").read(),
    author = 'kuankuan',
    author_email = '2163826131@qq.com',
    url="https://gitee.com/kuankuan2007/retry-command",
    install_requires = ['rich'],
    long_description_content_type="text/markdown",
    packages = ['retryCommand'],
    
    license = 'Mulan PSL v2',
    platforms=[
        "windows",
        "linux",
        "macos"
    ] ,
    classifiers = [
        "Natural Language :: English",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)'
    ],
    entry_points = {
        'console_scripts': [
            'do-retry = retryCommand:retryCommand',
        ],
    }
)
