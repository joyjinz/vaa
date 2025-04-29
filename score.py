import os
import pandas as pd

def calc_etf_momentum_score(df,weights):
    """
    df: 데이터프레임
    w_1M, w_3M, w_6M, w_12M: 각 기간별 가중치(정수 0~100)
    """
    etfs = ['SPY', 'EFA', 'EEM', 'AGG', 'LQD', 'IEF', 'SHY']
    fronts = [f'front_{i}' for i in range(1, 16)]
    backs = [f'back_{i}' for i in range(1, 16)]
    bases = fronts + backs  # 기준일 30개

    score_dict = {'YearMonth': df['YearMonth']}
    for etf in etfs:
        for base in bases:
            # 각 기간별 수익률 컬럼명
            col_1M = f'{etf}_{base}_1M_ret'
            col_3M = f'{etf}_{base}_3M_ret'
            col_6M = f'{etf}_{base}_6M_ret'
            col_12M = f'{etf}_{base}_12M_ret'
            # 모멘텀 점수 계산
            score = (
                df[col_1M] * weights[0] +
                df[col_3M] * weights[1] +
                df[col_6M] * weights[2] +
                df[col_12M] * weights[3]
            )
            score_dict[f'{etf}_{base}_score'] = score

    score_df = pd.DataFrame(score_dict)

    # 파일 저장(기존 파일 있으면 삭제)
    out_file = 'etf_score.csv'
    if os.path.exists(out_file):
        os.remove(out_file)
    score_df.to_csv(out_file, index=False)

    return score_df
