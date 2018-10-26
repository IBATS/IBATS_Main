# -*- coding: utf-8 -*-
"""
Created on 2017/6/9
@author: MG
"""
import logging
from logging.config import dictConfig
from ibats_common.config import ConfigBase as ConfigBaseCommon, update_config as update_config_common
from ibats_bitmex_trader.config import ConfigBase as ConfigBaseTrader, update_config as update_config_trader
from ibats_bitmex_feeder.config import ConfigBase as ConfigBaseFeeder, update_config as update_config_feeder
logger = logging.getLogger()


class ConfigTrader(ConfigBaseTrader):
    # api configuration
    # https://testnet.bitmex.com/app/apiKeys
    TEST_NET = True
    EXCHANGE_PUBLIC_KEY = "kRGATSGD9QRhSRvY0Ih58t5z"
    EXCHANGE_SECRET_KEY = "tYJwFJeFe5SxzWETFEvoI_HxDaUbtF2fCNwxXd8SZyPNL-1J"

    # mysql db info
    DB_URL_DIC = {
        super().DB_SCHEMA_MD: f'mysql://mg:****@localhost/' + super().DB_SCHEMA_MD,
        super().DB_SCHEMA_IBATS: 'mysql://mg:****@localhost/' + super().DB_SCHEMA_IBATS,
    }


update_config_trader(ConfigTrader())


class ConfigFeeder(ConfigBaseFeeder):
    # api configuration
    # https://testnet.bitmex.com/app/apiKeys
    TEST_NET = True
    EXCHANGE_PUBLIC_KEY = "K5DaKlClbXg_TQn5lEGOswd8"
    EXCHANGE_SECRET_KEY = "QQwPpUpCUcJwtqFIsDXevMqhEPUM3eanZUnzlSpYGqaLIbph"

    # mysql db info
    DB_HANDLER_ENABLE = True
    DB_URL_DIC = {
        super().DB_SCHEMA_MD: 'mysql://mg:****@localhost/' + super().DB_SCHEMA_MD
    }

    # redis info
    REDIS_PUBLISHER_HANDLER_ENABLE = False
    REDIS_INFO_DIC = {'REDIS_HOST': 'localhost',  # '192.168.239.131'
                      'REDIS_PORT': '6379',
                      }


update_config_feeder(ConfigFeeder())


class ConfigBase(ConfigBaseCommon):

    # mysql db info
    DB_URL_DIC = {
        super().DB_SCHEMA_IBATS: 'mysql://mg:****@localhost/' + super().DB_SCHEMA_IBATS,
    }


# 开发配置（SIMNOW MD + Trade）
config = ConfigBase()
update_config_common(config)


def update_config(config_update: ConfigBase):
    global config
    config = config_update
    logger.info('更新默认配置信息 %s < %s', ConfigBase, config_update)
