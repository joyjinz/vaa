import pandas as pd
import os

def rebuild_etf_data(df_close: pd.DataFrame, filename='etf_rebuild.csv') -> pd.DataFrame:
    # Date를 datetime으로 변환 및 정렬
    df_close['Date'] = pd.to_datetime(df_close['Date'])
    df_close = df_close.sort_values('Date').reset_index(drop=True)
    
    # 연-월 추가
    df_close['YearMonth'] = df_close['Date'].dt.to_period('M')
    unique_months = df_close['YearMonth'].unique()
    
    # 처음, 마지막 월 제외
    months_to_use = unique_months[1:-1]

    result_rows = []
    month_labels = []

    for ym in months_to_use:
        df_month = df_close[df_close['YearMonth'] == ym]
        if len(df_month) < 15:
            continue  # 데이터 부족 시 건너뛰기

        front = df_month.head(15).reset_index(drop=True)
        back = df_month.tail(15).iloc[::-1].reset_index(drop=True)

        row = []
        for etf in df_close.columns:
            if etf in ['Date', 'YearMonth']:
                continue

            # 앞쪽 15개
            row += [front.at[i, etf] for i in range(15)]
            # 뒤쪽 15개
            row += [back.at[i, etf] for i in range(15)]

        result_rows.append(row)
        month_labels.append(str(ym))

    # 컬럼 이름 만들기
    etfs = [col for col in df_close.columns if col not in ['Date', 'YearMonth']]
    columns = []
    for etf in etfs:
        columns += [f"{etf}_front_{i+1}" for i in range(15)]
        columns += [f"{etf}_back_{i+1}" for i in range(15)]

    result_df = pd.DataFrame(result_rows, columns=columns)

    # 첫 행에 월 정보를 삽입
    result_df.insert(0, 'YearMonth', month_labels)

    # 파일 있으면 삭제
    if os.path.exists(filename):
        os.remove(filename)

    result_df.to_csv(filename, index=False)

    return result_df
