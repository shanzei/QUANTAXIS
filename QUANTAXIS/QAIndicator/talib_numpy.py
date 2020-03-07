# coding:utf-8
# Author: 阿财（Rgveda@github）（11652964@qq.com）
# Created date: 2020-02-27
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
try:
    import talib
except:
    pass
    #print('PLEASE install TALIB to call these methods')


# 定义MACD函数
def TA_MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    '''
    参数设置:
        fastperiod = 12
        slowperiod = 26
        signalperiod = 9

    返回: macd - dif, signal - dea, hist * 2 - bar, delta
    '''
    macd, signal, hist = talib.MACD(prices, 
                                    fastperiod=fastperiod, 
                                    slowperiod=slowperiod, 
                                    signalperiod=signalperiod)
    delta = np.r_[np.nan, np.diff(hist * 2)]
    return np.c_[macd, signal, hist * 2, delta]


# 定义RSI函数
def TA_RSI(prices, timeperiod=12):
    '''
    参数设置:
        timeperiod = 12

    返回: ma
    '''
    rsi = talib.RSI(prices, timeperiod=timeperiod)
    delta = np.r_[np.nan, np.diff(rsi)]
    return np.c_[rsi, delta]


# 定义RSI函数
def TA_BBANDS(prices, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0):
    '''
    参数设置:
        timeperiod = 5
        nbdevup = 2
        nbdevdn = 2

    返回: up, middle, low
    '''
    up, middle, low = talib.BBANDS(prices, timeperiod, nbdevup, nbdevdn, matype)
    ch = (up - low) / low
    delta = np.r_[np.nan, np.diff(ch)]
    return np.c_[up, middle, low, ch, delta]


def TA_KDJ(hight, low, close, fastk_period=9, slowk_matype=0, slowk_period=3, slowd_period=3):
    '''
    参数设置:
        fastk_period = 9
        lowk_matype = 0, 
        slowk_period = 3, 
        slowd_period = 3

    返回: K, D, J
    '''
    K, D = talib.STOCH(hight, low, close, fastk_period=fastk_period, slowk_matype=slowk_matype, slowk_period=slowk_period, slowd_period=slowd_period)
    J = 3 * K - 2 * D
    delta = np.r_[np.nan, np.diff(J)]
    return np.c_[K, D, J, delta]


def TA_ADX(high, low, close, timeperiod=14):
    """
    ADX - Average Directional Movement Index
    """
    real = talib.ADX(high, low, close, timeperiod=timeperiod)
    return np.c_[real]


def TA_ADXR(high, low, close, timeperiod=14):
    """
    名称：平均趋向指数的趋向指数
    简介：使用ADXR指标，指标判断ADX趋势。
    ADXR - Average Directional Movement Index Rating
    """
    real = talib.ADXR(high, low, close, timeperiod=timeperiod)
    return np.c_[real]


def TA_CCI(high, low, close, timeperiod=14):
    """
    名称：平均趋向指数的趋向指数
    简介：使用CCI指标，指标判断CCI趋势。
    CCI - Commodity Channel Index
    """
    real = talib.CCI(high, low, close, timeperiod=timeperiod)
    delta = np.r_[np.nan, np.diff(real)]
    return np.c_[real, delta]


def TA_KAMA(close, timeperiod=30):
    """
    请直接用 talib.KAMA(close, timeperiod)
    KAMA - Kaufman Adaptive Moving Average
    """
    real = talib.KAMA(close, timeperiod=timeperiod)
    return np.c_[real]


def TA_HMA(close, period):
    """
    赫尔移动平均线(HMA) 
    Hull Moving Average.
    Formula:
    HMA = WMA(2*WMA(n/2) - WMA(n)), sqrt(n)
    """
    hma = talib.WMA(2 * talib.WMA(close, int(period / 2)) - talib.WMA(close, period), int(np.sqrt(period)))
    return hma


def TA_ADXm(data, period=10, smooth=10, limit=18):
    """
    Moving Average ADX
    ADX Smoothing Trend Color Change on Moving Average and ADX Cross. Use on Hourly Charts - Green UpTrend - Red DownTrend - Black Choppy No Trend

    Source: https://www.tradingview.com/script/owwws7dM-Moving-Average-ADX/

    Parameters
    ----------
    data : (N,) array_like
        传入 OHLC Kline 序列。
        The OHLC Kline.
    period : int or None, optional
        DI 统计周期 默认值为 10
        DI Length period. Default value is 10. 
    smooth : int or None, optional
        ADX 平滑周期 默认值为 10
        ADX smoothing length period. Default value is 10.
    limit : int or None, optional
        ADX 限制阈值 默认值为 18
        ADX MA Active limit threshold. Default value is 18.

    Returns
    -------
    adx, ADXm : ndarray
        ADXm 指标和趋势指示方向 (-1, 0, 1) 分别代表 (下跌, 无明显趋势, 上涨)
        ADXm indicator and thread directions sequence. (-1, 0, 1) means for (Negatice, No Trend, Postive)

    """
    lenadx = period
    lensig = smooth
    limadx = limit

    up = data.high.pct_change()
    down = data.low.pct_change() * -1

    trur = TA_HMA(talib.TRANGE(data.high.values, data.low.values, data.close.values) , lenadx)
    plus = 100 * TA_HMA(np.where(((up > down) & (up > 0)), up, 0), lenadx) / trur
    minus = 100 * TA_HMA(np.where(((down > up) & (down > 0)), down, 0), lenadx) / trur
    plus = np.r_[np.zeros(lenadx + 2), plus[(lenadx + 2):]]
    minus = np.r_[np.zeros(lenadx + 2), minus[(lenadx + 2):]]
    sum = plus + minus 
    adx = 100 * TA_HMA(abs(plus - minus) / (np.where((sum == 0), 1, sum)), lensig)
    adx = np.r_[np.zeros(lensig + 2), adx[(lensig + 2):]]
    ADXm = np.where(((adx > limadx) & (plus > minus)), 1, np.where(((adx > limadx) & (plus < minus)), -1, 0))
    return adx, ADXm