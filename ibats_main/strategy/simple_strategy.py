#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/21 11:26
@File    : simple_strategy.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import logging
import time
import pandas as pd
from ibats_main.config import config  # 单策略执行时，该语句需写在加载 ibats_common 模块前面，以便首先更新数据库配置信息
from ibats_common.common import BacktestTradeMode, PeriodType, RunMode, ContextKey, Direction, ExchangeName
from ibats_common.strategy import StgBase
from ibats_common.strategy_handler import strategy_handler_factory
# 下面代码是必要的引用
# md_agent md_agent 并没有“显式”的被使用，但是在被引用期间，已经将相应的 agent 类注册到了相应的列表中
# import ibats_bitmex_trader.agent.md_agent
# import ibats_bitmex_trader.agent.td_agent
import ibats_huobi_trader.agent.md_agent
import ibats_huobi_trader.agent.td_agent

logger = logging.getLogger(__name__)


class MACroseStg(StgBase):

    def __init__(self, unit=1):
        super().__init__()
        self.ma5 = []
        self.ma10 = []
        self.unit = unit

    def on_prepare_min1(self, md_df: pd.DataFrame, context):
        if md_df is not None and md_df.shape[0] > 0:
            self.ma5 = list(md_df['close'].rolling(5, 5).mean())[10:]
            self.ma10 = list(md_df['close'].rolling(10, 10).mean())[10:]

    def on_min1(self, md_df, context):
        close = md_df['close'].iloc[-1]
        self.ma5.append(md_df['close'].iloc[-5:].mean())
        self.ma10.append(md_df['close'].iloc[-10:].mean())
        instrument_id = context[ContextKey.instrument_id_list][0]
        if self.ma5[-2] < self.ma10[-2] and self.ma5[-1] > self.ma10[-1]:
            position_date_pos_info_dic = self.get_position(instrument_id)
            no_target_position = True
            if position_date_pos_info_dic is not None:
                for position_date, pos_info in position_date_pos_info_dic.items():
                    direction = pos_info.direction
                    if direction == Direction.Short:
                        self.close_short(instrument_id, close, pos_info.position)
                    elif direction == Direction.Long:
                        no_target_position = False
            if no_target_position:
                self.open_long(instrument_id, close, self.unit)
        elif self.ma5[-2] > self.ma10[-2] and self.ma5[-1] < self.ma10[-1]:
            position_date_pos_info_dic = self.get_position(instrument_id)
            no_target_position = True
            if position_date_pos_info_dic is not None:
                for position_date, pos_info in position_date_pos_info_dic.items():
                    direction = pos_info.direction
                    if direction == Direction.Long:
                        self.close_long(instrument_id, close, pos_info.position)
                    elif direction == Direction.Short:
                        no_target_position = False
            if no_target_position:
                self.open_short(instrument_id, close, self.unit)


if __name__ == '__main__':
    # 参数设置
    run_mode = RunMode.Backtest
    strategy_params = {'unit': 100}
    md_agent_params_list = [{
        'md_period': PeriodType.Min1,
        'instrument_id_list': ['ETHUSDT'],
        'init_md_date_from': '2018-7-17',  # 行情初始化加载历史数据，供策略分析预加载使用
        'init_md_date_to': '2018-7-18',
    }]
    if run_mode == RunMode.Realtime:
        trade_agent_params = {
        }
        strategy_handler_param = {
        }
    else:
        trade_agent_params = {
            'trade_mode': BacktestTradeMode.Order_2_Deal,
            'init_cash': 1000000,
        }
        strategy_handler_param = {
            'date_from': '2018-10-29',  # 策略回测历史数据，回测指定时间段的历史行情
            'date_to': '2018-10-30',
        }
    # run_mode = RunMode.BackTest
    # 初始化策略处理器
    stghandler = strategy_handler_factory(stg_class=MACroseStg,
                                          strategy_params=strategy_params,
                                          md_agent_params_list=md_agent_params_list,
                                          exchange_name=ExchangeName.HuoBi,
                                          run_mode=RunMode.Backtest,
                                          trade_agent_params=trade_agent_params,
                                          strategy_handler_param=strategy_handler_param,
                                          )
    stghandler.start()
    time.sleep(10)
    stghandler.keep_running = False
    stghandler.join()
    logging.info("执行结束")
