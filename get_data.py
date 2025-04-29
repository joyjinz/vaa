import os
import pandas as pd
import yfinance as yf

def fetch_etf_data(mode='close'):
    etfs = ['SPY', 'EFA', 'EEM', 'AGG', 'LQD', 'IEF', 'SHY']
    filename = 'etf_adjclose.csv' if mode == 'adj' else 'etf_close.csv'
    price_type = 'Adj Close' if mode == 'adj' else 'Close'

    # 파일이 존재하면 기존 데이터 로드
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename, parse_dates=['Date'])
        last_date = df_existing['Date'].max()
    else:
        df_existing = None
        last_date = None

    # 야후에서 데이터 다운로드
    data = yf.download(etfs, start='2000-01-01', auto_adjust=False)

    # 원하는 컬럼만 추출 (Close or Adj Close)
    df = data[price_type]
    df = df.dropna()

    # 모든 ETF에 데이터가 존재하는 가장 최근 시작일 찾기
    df = df.dropna()
    min_date = df.index.min()

    # 만약 기존 데이터가 있으면, 이어서만 다운로드
    if last_date is not None:
        df = df[df.index > last_date]

    # 저장 형식 맞추기
    df = df[etfs]  # 컬럼 순서 고정
    df = df.reset_index()
    df.columns = ['Date'] + etfs

    # 기존 파일과 이어붙이기
    if df_existing is not None and not df.empty:
        df_final = pd.concat([df_existing, df], ignore_index=True)
    elif df_existing is not None:
        df_final = df_existing
    else:
        df_final = df

    # 저장
    df_final.to_csv(filename, index=False, float_format='%.15g')

    return df_final
