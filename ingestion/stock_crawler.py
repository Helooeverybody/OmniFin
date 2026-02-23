import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time
from tqdm import tqdm

class MarketCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*'
        })

    def fetch_vietnam_stock(self, symbol, start_date, end_date):
        try:
            api_symbol = symbol
            if symbol == 'HNXIndex': 
                api_symbol = 'HNX'
            elif symbol == 'UPCOMIndex': 
                api_symbol = 'UPCOM'

            start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
            end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
            
            url = f"https://services.entrade.com.vn/chart-api/v2/ohlcs/stock?from={start_ts}&to={end_ts}&symbol={api_symbol}&resolution=1D"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return pd.DataFrame()
            data = response.json()
            if 't' not in data or not data['t']:
                return pd.DataFrame() 
            df = pd.DataFrame({
                'Date': data['t'],
                'Open': data['o'],
                'High': data['h'],
                'Low': data['l'],
                'Close': data['c'],
                'Volume': data['v']
            })
            df['Date'] = pd.to_datetime(df['Date'], unit='s').dt.strftime('%Y-%m-%d')
            df['Ticker'] = symbol
            df['Market'] = 'Vietnam'
            return df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market']]
        except Exception as e:
            print(f"Error fetching Vietnam stock {symbol}: {e}") 
            return pd.DataFrame()

    def fetch_international_stock(self, symbol, start_date, end_date):
        try:
            stock = yf.Ticker(symbol)
            end_date_yf = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime('%Y-%m-%d')
            df = stock.history(start=start_date, end=end_date_yf, interval="1d")
            
            if df.empty:
                return pd.DataFrame()

            df.reset_index(inplace=True)
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            df['Ticker'] = symbol
            df['Market'] = 'International'
            
            return df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market']]
        except Exception:
            return pd.DataFrame()

    def fetch_crypto_binance(self, symbol, start_date, end_date):
        try:
            start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp() * 1000)
            end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp() * 1000)
            
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&startTime={start_ts}&endTime={end_ts}"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            if not data or isinstance(data, dict): 
                return pd.DataFrame()

            df = pd.DataFrame(data, columns=['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume', 
                                             'CloseTime', 'QuoteAssetVol', 'Trades', 'Tbbav', 'Tbqav', 'Ignore'])
            
            df['Date'] = pd.to_datetime(df['OpenTime'], unit='ms').dt.strftime('%Y-%m-%d')
            df['Ticker'] = symbol
            df['Market'] = 'Crypto'
            
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = df[col].astype(float)
                
            return df[['Date', 'Ticker', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market']]
        except Exception:
            return pd.DataFrame()
    def crawl_all_markets(self, vn_symbols, int_symbols, crypto_symbols, start_date, end_date):
        all_data = []
        if vn_symbols:
            for symbol in tqdm(vn_symbols, desc="[1/3] Downloading VN Market", unit="symbol"):
                df = self.fetch_vietnam_stock(symbol, start_date, end_date)
                if not df.empty: all_data.append(df)
                time.sleep(0.2)
        if int_symbols:
            for symbol in tqdm(int_symbols, desc="[2/3] Downloading International Market", unit="symbol"):
                df = self.fetch_international_stock(symbol, start_date, end_date)
                if not df.empty: all_data.append(df)
                time.sleep(0.1)
        if crypto_symbols:
            for symbol in tqdm(crypto_symbols, desc="[3/3] Downloading Crypto", unit="symbol"):
                df = self.fetch_crypto_binance(symbol, start_date, end_date)
                if not df.empty: all_data.append(df)
                time.sleep(0.5) 
        if all_data:
            master_df = pd.concat(all_data, ignore_index=True)
            master_df.sort_values(by=['Market', 'Ticker', 'Date'], inplace=True)
            return master_df
        return pd.DataFrame()

if __name__ == "__main__":
    crawler = MarketCrawler()
    
    START_DATE = "2020-01-01" 
    END_DATE = datetime.now().strftime("%Y-%m-%d")

    vietnam_symbols = [
        "VCB", "BID", "CTG", "TCB", "VPB", "MBB", "ACB", "STB", "HDB", "SHB", "VIB", "TPB", "EIB", "MSB", "LPB", "OCB", "SSB",
        "VHM", "VIC", "VRE", "NVL", "KDH", "NLG", "DXG", "PDR", "DIG", "CEO", "HDG", "CRE", "SCR",
        "SSI", "VND", "VCI", "HCM", "SHS", "MBS", "FTS", "BSI", "CTS", "VIX", "AGR",
        "HPG", "HSG", "NKG", "HT1", "BCC", "POM",
        "FPT", "MWG", "PNJ", "DGW", "FRT", "PET",
        "VNM", "MSN", "SAB", "DBC", "HAG", "PAN", "TAR", "MCH", "QNS",
        "GAS", "PLX", "PVD", "PVS", "BSR", "POW", "NT2", "GEG", "PC1",
        "DGC", "DCM", "DPM", "GVR", "PHR", "DPR", "CSV",
        "GMD", "HAH", "VSC", "PVT", "MVN",
        "IDC", "KBC", "SZC", "VGC", "ITA", "BCM",
        "VCG", "HHV", "CTD", "HBC", "LCG", "CII", "FCN",
        "VJC", "HVN", "SKG",
        "VNINDEX", "VN30", "HNXIndex", "UPCOMIndex"
    ]
    
    international_symbols = [
        "AAPL", "TSLA", "MSFT", "NVDA", "GOOGL", "AMZN", # Tech 
        "GC=F", "CL=F", "SI=F",                          # Gold, Oil, Silver
        "^GSPC", "^DJI", "^IXIC"                         # S&P500, Dow Jones, Nasdaq
    ]
    
    # --- Crypto ---
    crypto_symbols = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT" # Top 5 coins on Binance
    ]

    print(f"CRAWL FROM: {START_DATE} to {END_DATE}")
    print(f"THE TOTAL NUMBER OF SYMBOLS: {len(vietnam_symbols) + len(international_symbols) + len(crypto_symbols)}")
    print("-" * 50)
    
    final_data = crawler.crawl_all_markets(
        vn_symbols=vietnam_symbols, 
        int_symbols=international_symbols, 
        crypto_symbols=crypto_symbols, 
        start_date=START_DATE, 
        end_date=END_DATE
    )
    
    if not final_data.empty:
        final_data[['Open', 'High', 'Low', 'Close']] = final_data[['Open', 'High', 'Low', 'Close']].round(3)
        filename = f"universal_market_data_{END_DATE}.csv"
        final_data.to_csv(filename, index=False)
        print("\n" + "="*50)
        print(f"\n[*]{len(final_data)} rows of data collected successfully! ")
        print(f"File saved to: {filename}")
        

        stats = final_data.groupby('Market')['Ticker'].nunique()
        print("\n[+] Statistics of unique tickers collected by market:")
        print(stats.to_string())
    else:
        print("\n[-]Crawl completed but no data was collected.")