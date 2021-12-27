import ccxt
import datetime
import time

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    },
})

# s = "2021/01/01"
# since = time.mktime(datetime.datetime.strptime(s, "%Y/%d/%m").timetuple())
# since = str(int(since)*1000)
# res = exchange.fetch_ohlcv('BNB/BUSD',since=1609459200)
res = exchange.fetch_ohlcv('BNB/BUSD','1d')
res = res[-2:]

res2 = exchange.fetch_ohlcv('BNB/BUSD','1d')
res2= res2[-2:]
markets = exchange.load_markets()
ret = []
for key in markets:
    if 'BNB' in key:
        el = markets[key]
        ret.append(el['info'])
        print(el['info']['symbol'],el['info']['contractType'],key)
markets2 = exchange.load_markets()
m1 = markets['BTC/USDT']
m2 = markets2['BTC/USDT']
for key in markets:
    if 'PERP' in key:
        print(key)
print()
