"""
'api': {
                    'wapi': 'https://api.binance.com/wapi/v3',
                    'sapi': 'https://api.binance.com/sapi/v1',
                    'dapiPublic': 'https://dapi.binance.com/dapi/v1',
                    'dapiPrivate': 'https://dapi.binance.com/dapi/v1',
                    'dapiPrivateV2': 'https://dapi.binance.com/dapi/v2',
                    'dapiData': 'https://dapi.binance.com/futures/data',
                    'fapiPublic': 'https://fapi.binance.com/fapi/v1',
                    'fapiPrivate': 'https://fapi.binance.com/fapi/v1',
                    'fapiData': 'https://fapi.binance.com/futures/data',
                    'fapiPrivateV2': 'https://fapi.binance.com/fapi/v2',
                    'public': 'https://api.binance.com/api/v3',
                    'private': 'https://api.binance.com/api/v3',
                    'v1': 'https://api.binance.com/api/v1',
                },

[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]
"""
import httpx
import pandas as pd
import typing

url = 'https://dapi.binance.com/dapi/v1'
url = 'https://dapi.binance.com/dapi/v1/api/v3/kline'
url = 'https://dapi.binance.com/dapi/v1'
url = 'https://api.binance.com/api/v3/klines?symbol=BNBUSD_PERP&interval=1m'


def _get_kline(api: str, symbol: str, interval: str = '1m', limit: int = 1000):
    url = f'https://{api}.binance.com/{api}/v1/klines'
    params = dict(symbol=symbol, interval=interval, limit=limit, startTime=1609459200000)
    r = httpx.get(url, params=params)
    res = r.json()
    res = [arr[:6] for arr in res]
    df = pd.DataFrame(res, columns=['index', 'open', 'high', 'low', 'close', 'volume'])
    df['index'] = pd.to_datetime(df['index'], unit='ms')
    df.set_index('index', inplace=True)
    df['open'].astype('float')
    df = df.astype(
        {'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float', 'volume': 'float'}
    )
    return df


def get_dapi_kline(symbol: str, interval: str = '1m', limit: int = 500):
    return _get_kline('dapi', symbol, interval, limit)


def get_fapi_kline(symbol: str, interval: str = '1m', limit: int = 500):
    return _get_kline('fapi', symbol, interval, limit)


def diff(ser, index: int = 1):
    return ser - ser.shift(index)


def df_merges(*args):
    ret = args[0]
    for temp_df in args[1:]:
        ret = pd.merge(ret, temp_df, left_index=True, right_index=True)
    return ret


df_perp = get_dapi_kline('BNBUSD_PERP')
df_perp['BNB 永續'] = df_perp['close']
df_perp['BNB 永續 diff'] = diff(df_perp['BNB 永續'])

df_211231 = get_dapi_kline('BNBUSD_211231')
df_211231['BNB 交割'] = df_211231['close']
df_211231['BNB 交割 diff'] = diff(df_211231['BNB 交割'])

df_link = get_fapi_kline('LINKUSDT')
df_link['LINKUSDT'] = df_link['close']
df_link['LINKUSDT diff'] = diff(df_link['LINKUSDT'])

df_dot = get_fapi_kline('DOTUSDT')
df_dot['DOTUSDT'] = df_dot['close']
df_dot['DOTUSDT diff'] = diff(df_dot['DOTUSDT'])
df = df_merges(df_perp, df_211231, df_link, df_dot)

df = df[['BNB 永續', 'BNB 永續 diff', 'BNB 交割', 'BNB 交割 diff', 'LINKUSDT', 'LINKUSDT diff', 'DOTUSDT', 'DOTUSDT diff']]
df.to_csv('./demo.csv')
print()
