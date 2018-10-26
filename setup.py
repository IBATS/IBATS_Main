#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/14 16:07
@File    : setup.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as rm:
    long_description = rm.read()

setup(name='IBATS_BitMex_Trader',
      version='0.1.3',
      description='作为IBATS架构的 Trader 端，用于连接BitMex进行相应的交易及账户信息获取等动作',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='MG',
      author_email='mmmaaaggg@163.com',
      url='https://github.com/mmmaaaggg/IBATS_Trader',
      packages=find_packages(),
      python_requires='>=3.6',
      classifiers=(
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: Unix",
          "Operating System :: POSIX",
          "License :: OSI Approved :: MIT License",
          "Development Status :: 5 - Production/Stable",
          "Environment :: No Input/Output (Daemon)",
          "Intended Audience :: Developers",
          "Natural Language :: Chinese (Simplified)",
          "Topic :: Software Development",
      ),
      install_requires=[
          'websocket',
          'msgpack>=0.5.6',
          'bitmex',
          'bitmex-ws',
          'IBATSTrader',
          'IBATS_BitMex_Feeder',
          'mysqlclient>=1.3.8',
          'numpy==1.14.4',
          'pandas==0.23.0',
          'SQLAlchemy==1.2.8',
      ])
