import yfinance as yf
import pandas as pd
import numpy as np


'''
def fetch_dividend_info(tickers):
    results = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        # Current price
        print(stock.info)
        current_price = stock.info.get('regularMarketPrice')
        if current_price is None:
            hist = stock.history(period="1d")
            current_price = hist['Close'][0] if not hist.empty else np.nan
        # Recent 6 dividends average
        dividends = stock.dividends
        avg_dividend = dividends[-6:].mean() if not dividends.empty else 0.0
        # Income = avg dividend / current price
        income = avg_dividend / current_price if current_price else 0.0
        # Expense ratio (if present, usually for ETFs)
        expense_ratio = stock.info.get('netExpenseRatio', np.nan)
        yyield= stock.info.get('dividendYield',np.nan)
        print(f"{ticker} {expense_ratio}")
        if expense_ratio is not None and expense_ratio == expense_ratio:  # checks not nan
            expense_ratio = expense_ratio * 100  # convert to percentage
        results.append({
            'Ticker': ticker,
            'Current Price': current_price,
            'Average Dividend (6 recent)': avg_dividend,
            'Income (Dividend Yield)': income,
            'Expense Ratio (%)': expense_ratio,
            'd yield':yyield
        })
    return pd.DataFrame(results)
'''
def fetch_dividend_info(tickers):
    results = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            
            # Try to get basic info first to check if ticker is valid
            try:
                info = stock.info
                print(f"Successfully fetched info for {ticker}")
            except Exception as e:
                print(f"Error fetching info for {ticker}: {e}")
                # Add a row with NaN values for failed tickers
                results.append({
                    'Ticker': ticker,
                    'Current Price': np.nan,
                    'Average Dividend (6 recent)': np.nan,
                    'Income (Dividend Yield)': np.nan,
                    'Expense Ratio (%)': np.nan,
                    'd yield': np.nan
                })
                continue
            
            # Current price
            current_price = info.get('regularMarketPrice')
            if current_price is None:
                try:
                    hist = stock.history(period="1d")
                    current_price = hist['Close'][-1] if not hist.empty else np.nan
                except:
                    current_price = np.nan
            
            # Recent 6 dividends average
            try:
                dividends = stock.dividends
                avg_dividend = dividends[-6:].mean() if not dividends.empty else 0.0
            except:
                avg_dividend = np.nan
            
            # Income = avg dividend / current price
            income = avg_dividend / current_price if (current_price and not np.isnan(current_price)) else 0.0
            
            # Expense ratio (if present, usually for ETFs)
            expense_ratio = info.get('netExpenseRatio', np.nan)
            yyield = info.get('dividendYield', np.nan)
            
            print(f"{ticker} expense_ratio: {expense_ratio}")
            
            if expense_ratio is not None and not np.isnan(expense_ratio):
                expense_ratio = expense_ratio * 100  # convert to percentage
            
            results.append({
                'Ticker': ticker,
                'Current Price': current_price,
                'Average Dividend (6 recent)': avg_dividend,
                'Income (Dividend Yield)': income,
                'Expense Ratio (%)': expense_ratio,
                'd yield': yyield
            })
            
        except Exception as e:
            print(f"Unexpected error processing {ticker}: {e}")
            # Add a row with NaN values for failed tickers
            results.append({
                'Ticker': ticker,
                'Current Price': np.nan,
                'Average Dividend (6 recent)': np.nan,
                'Income (Dividend Yield)': np.nan,
                'Expense Ratio (%)': np.nan,
                'd yield': np.nan
            })
    
    return pd.DataFrame(results)


if __name__ == "__main__":
    # Example list of tickers
    #tickers = ['JNK','HYG','LQD','SJNK','PHB','HYLB','MBB','FXC','FXE','FXB']

    tickers = ["ZAG", "ZMBS", "ZDB", "ZEF", "ZEB", "ZRE", "ZUT", "ZHY", "ZJK", "ZJK.U", "ZPR", "ZPR.U", "ZLC", "ZFL", "ZPL", "ZCM", "ZFM", "ZMP", "ZMU", "ZIC", "ZIC.U", "ZRR", "ZCS", "ZFS", "ZPS", "ZSU", "ZUAG", "ZUAG.F", "ZUAG.U", "ZHP", "ZUP", "ZUP.U", "ZBAL.T", "ZDV", "ZWC", "ZWB", "ZWB.U", "ZWA", "ZWEN", "ZWHC", "ZWT", "ZWK", "ZWU", "ZWP", "ZWE", "ZFH", "ZWG", "ZGRO.T", "ZDI", "ZDH", "ZMI", "ZMI.U", "ZPAY", "ZPAY.F", "ZPAY.U", "ZST", "ZUS.U", "ZUCM", "ZUCM.U", "ZDY", "ZDY.U", "ZUD", "ZWH", "ZWH.U", "ZWS", "ZPW", "ZPW.U", "ZPH", "ZWQT", "BGDV", "BGRT", "ZMMK", "BGIF"]

    tickers_with_to = [ticker + ".TO" for ticker in tickers]

    df = fetch_dividend_info(tickers_with_to)
    print(df.to_string())
