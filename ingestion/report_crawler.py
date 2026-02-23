from vnstock import financial_ratio, financial_flow

# 1. Get Financial Indicators (P/E, P/B, ROE, ROA, Profit Margins) for FPT
df_ratio = financial_ratio(symbol="FPT", report_range='yearly', is_all=True)
print("--- FPT Financial Ratios ---")
print(df_ratio.head())

# 2. Get Income Statement / Balance Sheet details
# report_type can be: 'incomestatement', 'balancesheet', 'cashflow'
df_income = financial_flow(symbol="FPT", report_type='incomestatement', report_range='yearly')
print("\n--- FPT Income Statement ---")
print(df_income.head())