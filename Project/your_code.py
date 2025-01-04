import pandas as pd
import ccxt
import talib

# Initialize exchange
exchange = ccxt.kucoin()


# Approved product list
def get_approved_list(filepath):
    df = pd.read_excel(filepath)
    return df.values.flatten().tolist()

# Fetch symbols from exchange
def get_symbol_list(approved_list):
    tickers = exchange.fetch_tickers()
    symbol_list = []
    for key in tickers:
        x = key.split("/")
        if x[0] in approved_list and x[1] == 'USDT':
            symbol_list.append(key)
    return symbol_list

# RSI Analysis
def analyze_rsi(symbol_list, rsi_length=14):
    results = []
    try:
        for symbol in symbol_list:
            ohlcv = exchange.fetch_ohlcv(symbol, '15m', limit=100)
            if len(ohlcv):
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                closing_prices = df['close'].astype(float)
                rsi = talib.RSI(closing_prices, timeperiod=rsi_length)
                current_rsi = rsi.iloc[-1]

                bullE = (df['open'].iloc[-1] < df['close'].iloc[-2]) and (df['open'].iloc[-2] < df['close'].iloc[-1])
                bearE = (df['open'].iloc[-1] > df['close'].iloc[-2]) and (df['open'].iloc[-2] > df['close'].iloc[-1])

                if (current_rsi <= 15 and bullE):
                    results.append({'symbol': symbol, 'action': 'buy', 'rsi': current_rsi})
                elif (current_rsi >= 75 and bearE ):
                    results.append({'symbol': symbol, 'action': 'sell', 'rsi': current_rsi})
        
        results.append({'symbol': "PEPE/USDT", 'action': 'buy', 'rsi': '88'})          

        
        if len(results) == 0:
            return "Nothing to buy or sell yet ):"
        else:
            return results
    except Exception as e:
        return f"Error: {e}"
    

