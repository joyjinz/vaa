import os
import pandas as pd

def select_etf_ticker(df):
    aggressive = ['SPY', 'EFA', 'EEM', 'AGG']
    defensive = ['LQD', 'IEF', 'SHY']
    bases = [f'front_{i}' for i in range(1, 16)] + [f'back_{i}' for i in range(1, 16)]

    result = {'YearMonth': df['YearMonth']}
    for base in bases:
        # 각 기준일별 점수 컬럼명
        agg_cols = [f"{etf}_{base}_score" for etf in aggressive]
        def_cols = [f"{etf}_{base}_score" for etf in defensive]

        tickers = []
        for idx, row in df.iterrows():
            agg_scores = row[agg_cols].values
            def_scores = row[def_cols].values

            # 공격형 모두 0 이상이면 공격형 중 최고점 ETF(모두 음수면 0에 가까운 ETF)
            if (agg_scores >= 0).all():
                sel_idx = agg_scores.argmax()
                ticker = aggressive[sel_idx]
            else:
                # 방어형 중 최고점(0이상), 모두 음수면 0에 가까운 ETF
                if (def_scores > 0).any():
                    sel_idx = def_scores.argmax()
                    ticker = defensive[sel_idx]
                else:
                    sel_idx = abs(def_scores).argmin()
                    ticker = defensive[sel_idx]
            tickers.append(ticker)
        result[f"{base}_select"] = tickers

    out_file = 'etf_select_ticker.csv'
    if os.path.exists(out_file):
        os.remove(out_file)
    pd.DataFrame(result).to_csv(out_file, index=False)
    return pd.DataFrame(result)
