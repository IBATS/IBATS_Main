# -*- coding: utf-8 -*-
"""
Created on 2017/6/9
@author: MG
"""
import logging
from ibats_common.config import ConfigBase as ConfigBaseCommon, update_config as update_config_common
from ibats_bitmex_trader.config import ConfigBase as CB_BitMex_Trader, update_config as update_config_bitmex_trader
from ibats_bitmex_feeder.config import ConfigBase as CB_BitMex_Feeder, update_config as update_config_bitmex_feeder
from ibats_huobi_trader.config import ConfigBase as CB_Huobi_Trader, update_config as update_config_huobi_trader
from ibats_huobi_feeder.config import ConfigBase as CB_Huobi_Feeder, update_config as update_config_huobi_feeder

logger = logging.getLogger(__name__)
_DB_URL_BASE = 'mysql://m*:***@localhost/'  # 仅为配置方便而设置变量，请勿外部引用


# 更新 Common 配置
class ConfigBase(ConfigBaseCommon):
    # mysql db info
    DB_URL_DIC = {
        ConfigBaseCommon.DB_SCHEMA_IBATS: _DB_URL_BASE + ConfigBaseCommon.DB_SCHEMA_IBATS,
    }


# 更新 BitMex Feeder 配置
class ConfigFeederBitMex(CB_BitMex_Feeder):
    # api configuration
    # https://testnet.bitmex.com/app/apiKeys
    TEST_NET = True
    EXCHANGE_PUBLIC_KEY = "***"
    EXCHANGE_SECRET_KEY = "***"

    # mysql db info
    DB_HANDLER_ENABLE = True
    DB_URL_DIC = {
        CB_BitMex_Feeder.DB_SCHEMA_MD: _DB_URL_BASE + CB_BitMex_Feeder.DB_SCHEMA_MD
    }

    # redis info
    REDIS_PUBLISHER_HANDLER_ENABLE = False
    REDIS_INFO_DIC = {'REDIS_HOST': 'localhost',  # '192.168.239.131'
                      'REDIS_PORT': '6379',
                      }


# 更新 BitMex Trader 配置
class ConfigTraderBitMex(CB_BitMex_Trader):
    # api configuration
    # https://testnet.bitmex.com/app/apiKeys
    TEST_NET = True
    EXCHANGE_PUBLIC_KEY = "***"
    EXCHANGE_SECRET_KEY = "***"

    # mysql db info
    DB_URL_DIC = {
        CB_BitMex_Trader.DB_SCHEMA_MD: _DB_URL_BASE + CB_BitMex_Trader.DB_SCHEMA_MD,
        CB_BitMex_Trader.DB_SCHEMA_IBATS: _DB_URL_BASE + CB_BitMex_Trader.DB_SCHEMA_IBATS,
    }


# 更新 Huobi Feeder 配置
class ConfigFeederHuobi(CB_Huobi_Feeder):
    # api configuration
    # https://testnet.bitmex.com/app/apiKeys
    EXCHANGE_ACCESS_KEY = '***'
    EXCHANGE_SECRET_KEY = '***'

    # mysql db info
    DB_HANDLER_ENABLE = True
    DB_SCHEMA_MD = 'md_huobi'
    DB_URL_DIC = {
        DB_SCHEMA_MD: _DB_URL_BASE + DB_SCHEMA_MD,
    }

    # redis info
    REDIS_PUBLISHER_HANDLER_ENABLE = False
    REDIS_INFO_DIC = {'REDIS_HOST': 'localhost',  # '192.168.239.131'
                      'REDIS_PORT': '6379',
                      }


# 更新 Huobi Trader 配置
class ConfigTraderHuobi(CB_Huobi_Trader):
    # api configuration
    # https://testnet.bitmex.com/app/apiKeys
    EXCHANGE_ACCESS_KEY = '***'
    EXCHANGE_SECRET_KEY = '***'

    # mysql db info
    DB_SCHEMA_MD = 'md_huobi'
    DB_URL_DIC = {
        DB_SCHEMA_MD: _DB_URL_BASE + DB_SCHEMA_MD,
        CB_Huobi_Trader.DB_SCHEMA_IBATS: _DB_URL_BASE + CB_Huobi_Trader.DB_SCHEMA_IBATS,
    }


def update_config(config_update: ConfigBase):
    global config
    config = config_update
    logger.info('更新默认配置信息 %s < %s', ConfigBase, config_update)


logging.getLogger('ibats_common.strategy').setLevel(logging.INFO)
# 实例化配置对象
config = ConfigBase()
update_config_common(config)
update_config_bitmex_feeder(ConfigFeederBitMex())
update_config_bitmex_trader(ConfigTraderBitMex())
update_config_huobi_feeder(ConfigFeederHuobi())
update_config_huobi_trader(ConfigTraderHuobi())
