#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/7 10:42
@File    : ma_cross_stg.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import time
import logging
from collections import defaultdict
from ibats_main.config import config  # 单策略执行时，该语句需写在加载 ibats_common 模块前面，以便首先更新数据库配置信息
from ibats_common.common import PeriodType, RunMode, BacktestTradeMode, ExchangeName, ContextKey, Direction
from ibats_common.strategy import StgBase
from ibats_common.strategy_handler import strategy_handler_factory_multi_exchange
# 下面代码是必要的引用
# md_agent md_agent 并没有“显式”的被使用，但是在被引用期间，已经将相应的 agent 类注册到了相应的列表中
import ibats_bitmex_trader.agent.md_agent
import ibats_bitmex_trader.agent.td_agent
import ibats_huobi_trader.agent.md_agent
import ibats_huobi_trader.agent.td_agent

logger = logging.getLogger(__name__)


class InterExchangeSpread(StgBase):

    def __init__(self):
        super().__init__()
        self.ma5 = defaultdict(list)

    def on_prepare_min1(self, md_df, context):
        md_agent_key = context[ContextKey.md_agent_key]
        if md_df is not None and md_df.shape[0] >= 5:
            self.ma5[md_agent_key] = list(md_df['close'].rolling(5, 5).mean())[10:]
        else:
            self.logger.warning('%s md_df 数据无效 %s', md_agent_key, md_df)

    def on_min1(self, md_df, context):
        md_agent_key = context[ContextKey.md_agent_key]
        close = md_df['close'].iloc[-1]
        self.ma5[md_agent_key].append(md_df['close'].iloc[-5:].mean())
        # 提取另一个 key
        another_key_set = self.ma5.keys() - {md_agent_key}
        if len(another_key_set) == 0:
            self.logger.warning('%s 缺少与之对应的key，无法进行计算', md_agent_key)
            return
        another_key = another_key_set.pop()
        # 数据长度校验
        if len(self.ma5[another_key]) < 2:
            self.logger.warning('%s 数据长度不足，无法进行计算', another_key)
            return
        if len(self.ma5[md_agent_key]) < 2:
            self.logger.warning('%s 数据长度不足，无法进行计算', md_agent_key)
            return
        # 获取 symbol
        instrument_id = context[ContextKey.instrument_id_list][0]
        if self.ma5[another_key][-2] < self.ma5[md_agent_key][-2] \
                and self.ma5[another_key][-1] > self.ma5[md_agent_key][-1]:
            position_date_pos_info_dic = self.get_position(instrument_id, md_agent_key=md_agent_key)
            no_target_position = True
            if position_date_pos_info_dic is not None:
                for position_date, pos_info in position_date_pos_info_dic.items():
                    direction = pos_info.direction
                    if direction == Direction.Short:
                        self.close_short(instrument_id, close, pos_info.position, md_agent_key=md_agent_key)
                    elif direction == Direction.Long:
                        no_target_position = False
            if no_target_position:
                self.open_long(instrument_id, close, 1, md_agent_key=md_agent_key)
        elif self.ma5[another_key][-2] > self.ma5[md_agent_key][-2] \
                and self.ma5[another_key][-1] < self.ma5[md_agent_key][-1]:
            position_date_pos_info_dic = self.get_position(instrument_id, md_agent_key=md_agent_key)
            no_target_position = True
            if position_date_pos_info_dic is not None:
                for position_date, pos_info in position_date_pos_info_dic.items():
                    direction = pos_info.direction
                    if direction == Direction.Long:
                        self.close_long(instrument_id, close, pos_info.position, md_agent_key=md_agent_key)
                    elif direction == Direction.Short:
                        no_target_position = False
            if no_target_position:
                self.open_short(instrument_id, close, 1, md_agent_key=md_agent_key)


def _test_use():
    # 参数设置
    run_mode = RunMode.Backtest
    strategy_params = {}
    md_agent_params_list = [
        {
            'agent_name': 'Huobi.Min1',
            'md_period': PeriodType.Min1,
            'exchange_name': ExchangeName.HuoBi,
            'instrument_id_list': ['ethusdt'],
            'init_md_date_to': '2018-8-15',
        },
        {
            'agent_name': 'BitMex.Min1',
            'md_period': PeriodType.Min1,
            'exchange_name': ExchangeName.BitMex,
            'instrument_id_list': ['ETHUSD'],
            'init_md_date_to': '2018-8-15',
        }
    ]
    if run_mode == RunMode.Realtime:
        trade_agent_params_list = [{
        }]
        strategy_handler_param = {
        }
    else:
        trade_agent_params_list = [
            {
                'agent_name': 'HuoBiAg',
                'exchange_name': ExchangeName.HuoBi,
                'trade_mode': BacktestTradeMode.Order_2_Deal,
                'init_cash': 1000000,
            },
            {
                'agent_name': 'BitMexAg',
                'exchange_name': ExchangeName.BitMex,
                'trade_mode': BacktestTradeMode.Order_2_Deal,
                'init_cash': 1000000,
            }
        ]
        strategy_handler_param = {
            'date_from': '2018-8-15',  # 策略回测历史数据，回测指定时间段的历史行情
            'date_to': '2018-8-19',
            'md_td_agent_key_list_map': {
                'Huobi.Min1': ['HuoBiAg'],
                'BitMex.Min1': ['BitMexAg']
            },  # md_td_agent_map 是可选输入参数，默认情况下，将根据交易所名称进行一一对应，这里也可以根据实际需要进行手动 mapping
        }

    # 初始化策略处理器
    stghandler = strategy_handler_factory_multi_exchange(
        stg_class=InterExchangeSpread,
        strategy_params=strategy_params,
        md_agent_params_list=md_agent_params_list,
        run_mode=RunMode.Backtest,
        trade_agent_params_list=trade_agent_params_list,
        strategy_handler_param=strategy_handler_param,
    )
    stghandler.start()
    time.sleep(30)
    stghandler.keep_running = False
    stghandler.join()
    logging.info("执行结束")


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, format=config.LOG_FORMAT)
    _test_use()
