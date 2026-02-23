import pandas as pd
import time
from tqdm import tqdm

from vnstock import Finance
import os
os.environ['VNSTOCK_API_KEY'] = 'vnstock_6bde9c03b7291cf177a19cdc14174677'
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
invalid_symbols = ["VNINDEX", "VN30", "HNXIndex", "UPCOMIndex"]
valid_symbols = [sym for sym in vietnam_symbols if sym not in invalid_symbols]

print(f"[*] Total valid symbols to download financial reports: {len(valid_symbols)}\n")

def crawl_financial_reports(symbols, report_type='income_statement', period='year'):
    all_data = []
    
    for symbol in tqdm(symbols, desc=f"Downloading {report_type} ({period})"):
        try:
            finance = Finance(symbol=symbol, source='VCI') 
        
            if report_type == 'income_statement':
                df = finance.income_statement(period=period)
            elif report_type == 'balance_sheet':
                df = finance.balance_sheet(period=period)
            elif report_type == 'cash_flow':
                df = finance.cash_flow(period=period)
            else:
                print("Invalid report type!")
                return pd.DataFrame()
            if df is not None and not df.empty:
                if 'ticker' not in df.columns and 'Ticker' not in df.columns:
                    df['Ticker'] = symbol
                elif 'ticker' in df.columns:
                    df.rename(columns={'ticker': 'Ticker'}, inplace=True)
                    
                all_data.append(df)
                
            time.sleep(0.3)
            
        except Exception as e:
            tqdm.write(f"[-] Cannot download data for {symbol}: {e}")
    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        return master_df
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    
    REPORT_TYPE = 'income_statement' 
    PERIOD = 'month' 
    
    final_reports_df = crawl_financial_reports(valid_symbols, report_type=REPORT_TYPE, period=PERIOD)
    
    if not final_reports_df.empty:
        cols = final_reports_df.columns.tolist()
        if 'Ticker' in cols:
            cols.insert(0, cols.pop(cols.index('Ticker')))
            final_reports_df = final_reports_df[cols]
        
        filename = f"vn_companies_{REPORT_TYPE}_{PERIOD}.csv"
        final_reports_df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print("\n" + "="*50)
        print(f"[+] SUCCESS! Collected {len(final_reports_df)} rows of financial data.")
        print(f"[+] Data saved to: {filename}")
        
        success_count = final_reports_df['Ticker'].nunique()
        print(f"[+] Number of companies with data retrieved: {success_count} / {len(valid_symbols)}")
    else:
        print("\n[-] No data collected.")