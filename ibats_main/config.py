# -*- coding: utf-8 -*-
"""
Created on 2017/6/9
@author: MG
"""
import logging
from ibats_common.config import ConfigBase as ConfigBaseCommon, update_config as update_config_common
from ibats_bitmex_trader.config import ConfigBase as ConfigBaseTrader, update_config as update_config_trader
from ibats_bitmex_feeder.config import ConfigBase as ConfigBaseFeeder, update_config as update_config_feeder

logger = logging.getLogger(__name__)
_DB_URL_BASE = 'mysql://mg:****@localhost/'  # 仅为配置方便而设置变量，请勿外部引用


# 更新 Common 配置
class ConfigBase(ConfigBaseCommon):

    # mysql db info
    DB_URL_DIC = {
        ConfigBaseCommon.DB_SCHEMA_IBATS: _DB_URL_BASE + ConfigBaseCommon.DB_SCHEMA_IBATS,
    }


# 实例化配置对象
config = ConfigBase()
update_config_common(config)


# 更新 Feeder 配置
class ConfigFeeder(ConfigBaseFeeder):
    # api configuration
    # https://testnet.bitmex.com/app/apiKeys
    TEST_NET = True
    EXCHANGE_PUBLIC_KEY = "K5DaKlClbXg_TQn5lEGOswd8"
    EXCHANGE_SECRET_KEY = "QQwPpUpCUcJwtqFIsDXevMqhEPUM3eanZUnzlSpYGqaLIbph"

    # mysql db info
    DB_HANDLER_ENABLE = True
    DB_URL_DIC = {
        ConfigBaseFeeder.DB_SCHEMA_MD: _DB_URL_BASE + ConfigBaseFeeder.DB_SCHEMA_MD
    }

    # redis info
    REDIS_PUBLISHER_HANDLER_ENABLE = False
    REDIS_INFO_DIC = {'REDIS_HOST': 'localhost',  # '192.168.239.131'
                      'REDIS_PORT': '6379',
                      }


update_config_feeder(ConfigFeeder())


# 更新 Trader 配置
class ConfigTrader(ConfigBaseTrader):
    # api configuration
    # https://testnet.bitmex.com/app/apiKeys
    TEST_NET = True
    EXCHANGE_PUBLIC_KEY = "kRGATSGD9QRhSRv***"
    EXCHANGE_SECRET_KEY = "tYJwFJeFe5SxzWETFEvoI_HxDaUbtF2fCNwxXd8SZy***"

    # mysql db info
    DB_URL_DIC = {
        ConfigBaseTrader.DB_SCHEMA_MD: _DB_URL_BASE + ConfigBaseTrader.DB_SCHEMA_MD,
        ConfigBaseTrader.DB_SCHEMA_IBATS: _DB_URL_BASE + ConfigBaseTrader.DB_SCHEMA_IBATS,
    }


update_config_trader(ConfigTrader())


def update_config(config_update: ConfigBase):
    global config
    config = config_update
    logger.info('更新默认配置信息 %s < %s', ConfigBase, config_update)


logging.getLogger('ibats_common.strategy').setLevel(logging.INFO)
