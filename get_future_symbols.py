import ccxt

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    },
})

# noinspection PyUnresolvedReferences
symbols = exchange.dapiPublicGetExchangeInfo()
symbols = exchange.fapiPublicGetExchangeInfo()
symbols = symbols['symbols']
arr = []
for symbol in symbols:
    if 'BNB' in symbol['symbol']:
        arr.append(symbol)
        print(symbol['symbol'],symbol['quoteAsset'])
"""
>>> BNBUSD_PERP
>>> BNBUSD_211231
>>> BNBUSD_220325
"""