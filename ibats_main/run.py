#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/9/28 8:42
@File    : run.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import click
import logging
import time
import os
import sys

if os.path.abspath(os.curdir) not in sys.path:
    sys.path.append(os.path.abspath(os.curdir))
    print("add to path:\n", os.path.abspath(os.curdir))

from ibats_main.config import config
from ibats_common.common import PeriodType, RunMode, BacktestTradeMode, ExchangeName
from ibats_common.strategy_handler import strategy_handler_factory
from ibats_main.strategy.simple_strategy import MACroseStg

logger = logging.getLogger()

strategy_list = [MACroseStg]  #
promt_str = '输入对应数字选择执行策略：\n' + \
            '\n'.join(['%d) %s' % (num, foo.__name__) for num, foo in enumerate(strategy_list, start=1)]) + '\n'


@click.command()
@click.option('--do', type=click.IntRange(1, 2), prompt="Choose command to run: 1) init 2) run strategy")
def main(do):
    if do == 1:
        from ibats_common.backend.orm import init
        init()
    elif do == 2:
        run_strategy()


@click.command()
@click.option('--num', type=click.IntRange(1, len(strategy_list)), prompt=promt_str)
def run_strategy(num):
    choice = num - 1
    stg_func = strategy_list[choice]

    DEBUG = False
    # 参数设置
    run_mode = RunMode.Backtest
    strategy_params = {'unit': 100}
    md_agent_params_list = [{
        'md_period': PeriodType.Min1,
        'instrument_id_set': {'ETHUSD'},
        'init_md_date_from': '2018-7-19',  # 行情初始化加载历史数据，供策略分析预加载使用
        'init_md_date_to': '2018-10-21',
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
            'date_from': '2018-7-19',  # 策略回测历史数据，回测指定时间段的历史行情
            'date_to': '2018-7-20',
        }
    # 初始化策略处理器
    stghandler = strategy_handler_factory(
        stg_class=stg_func,
        strategy_params=strategy_params,
        md_agent_params_list=md_agent_params_list,
        exchange_name=ExchangeName.BitMex,
        run_mode=RunMode.Backtest,
        trade_agent_params=trade_agent_params,
        strategy_handler_param=strategy_handler_param,
    )

    if DEBUG:
        stghandler.run()
    else:
        # 开始执行策略
        stghandler.start()
        try:
            while not stghandler.is_done:
                time.sleep(2)
        except KeyboardInterrupt:
            logger.warning('程序中断中...')
        except RuntimeError:
            logger.exception('策略执行异常')

        stghandler.is_working = False
        stghandler.join(timeout=2)

    logger.info("执行结束")


if __name__ == "__main__":
    main(standalone_mode=False)
