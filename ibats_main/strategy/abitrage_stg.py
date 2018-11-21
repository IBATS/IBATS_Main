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
from ibats_common.common import PeriodType, RunMode, BacktestTradeMode, ExchangeName, ContextKey, Direction
from ibats_common.strategy import StgBase
from ibats_common.strategy_handler import strategy_handler_factory_multi_exchange

logger = logging.getLogger(__name__)


class MACrossStg(StgBase):

    def __init__(self):
        super().__init__()
        self.ma5 = []
        self.ma10 = []

    def on_prepare_min1(self, md_df, context):
        if md_df:
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
                self.open_long(instrument_id, close, 1)
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
                self.open_short(instrument_id, close, 1)


def _test_use():
    # 参数设置
    run_mode = RunMode.Backtest
    strategy_params = {}
    md_agent_params_list = [
        {
            'md_period': PeriodType.Min1,
            'exchange_name': ExchangeName.BitMex,
            'instrument_id_set': {'ETHUSD'},  # ['jm1711', 'rb1712', 'pb1801', 'IF1710'],
            'init_md_date_to': '2017-9-1',
        },
        {
            'md_period': PeriodType.Min1,
            'exchange_name': ExchangeName.HuoBi,
            'instrument_id_set': {'ETHUSD'},  # ['jm1711', 'rb1712', 'pb1801', 'IF1710'],
            'init_md_date_to': '2017-9-1',
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
                'exchange_name': ExchangeName.BitMex,
                'trade_mode': BacktestTradeMode.Order_2_Deal,
                'init_cash': 1000000,
            },
            {
                'exchange_name': ExchangeName.BitMex,
                'trade_mode': BacktestTradeMode.Order_2_Deal,
                'init_cash': 1000000,
            }
        ]
        strategy_handler_param = {
            'date_from': '2018-7-19',  # 策略回测历史数据，回测指定时间段的历史行情
            'date_to': '2018-7-20',
        }

    # 初始化策略处理器
    stghandler = strategy_handler_factory_multi_exchange(
        stg_class=MACrossStg,
        strategy_params=strategy_params,
        md_agent_params_list=md_agent_params_list,
        run_mode=RunMode.Backtest,
        trade_agent_params_list=trade_agent_params_list,
        strategy_handler_param=strategy_handler_param,
    )
    stghandler.start()
    time.sleep(10)
    stghandler.keep_running = False
    stghandler.join()
    logging.info("执行结束")


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG, format=config.LOG_FORMAT)
    _test_use()
