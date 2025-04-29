import pandas as pd
import numpy as np
import os

def calculate_returns(df):
    # 수익률 계산 함수
    def calculate_return(column, months):
        return df[column] / df[column].shift(months) - 1

    etf_list = ['SPY', 'EFA', 'EEM', 'AGG', 'LQD', 'IEF', 'SHY']
    periods = [1, 3, 6, 12]  # 1개월, 3개월, 6개월, 12개월

    # 결과를 저장할 리스트 초기화
    return_columns = []

    # 1개월, 3개월, 6개월, 12개월 수익률 계산
    for etf in etf_list:
        for period in periods:
            # front_x 시리즈에 대해서 수익률 계산
            for i in range(1, 16):
                front_column = f"{etf}_front_{i}"
                return_column = f"{front_column}_{period}M_ret"
                return_columns.append((return_column, calculate_return(front_column, period)))

            # back_x 시리즈에 대해서 수익률 계산
            for i in range(1, 16):
                back_column = f"{etf}_back_{i}"
                return_column = f"{back_column}_{period}M_ret"
                return_columns.append((return_column, calculate_return(back_column, period)))

    # 수익률 열을 한 번에 추가
    return_df = pd.DataFrame(dict(return_columns))

    # 기존 DataFrame과 수익률 DataFrame을 결합
    df = pd.concat([df, return_df], axis=1)

    # 결측치가 포함된 행 제거
    df.dropna(inplace=True)

    file_name='etf_calculate.csv'
    if os.path.exists(file_name):
        os.remove(file_name)

    # 계산된 데이터프레임을 CSV로 저장
    df.to_csv(file_name, index=False)


    return df
