import pandas as pd
import numpy as np
import os

def calculate_etf_performance(df1, df2):
    df1 = df1.copy()
    df2 = df2.copy()

    # YearMonth를 datetime으로 변환
    df1['YearMonth'] = pd.to_datetime(df1['YearMonth'])
    df2['YearMonth'] = pd.to_datetime(df2['YearMonth'])

    # YearMonth를 인덱스로 설정
    df1.set_index('YearMonth', inplace=True)
    df2.set_index('YearMonth', inplace=True)

    result = {}

    for i in range(1, 16):
        for period in ['front', 'back']:
            col_key = f"{period}_{i}"
            returns = {}

            for ym in df2.index:
                next_month = ym + pd.DateOffset(months=1)
                if next_month not in df1.index:
                    continue

                etf = df2.loc[ym, f"{col_key}_select"]
                price_col = f"{etf}_{col_key}"

                try:
                    price_current = df1.loc[ym, price_col]
                    price_next = df1.loc[next_month, price_col]
                    ret = (price_next - price_current) / price_current
                    returns[ym] = ret
                except KeyError:
                    continue
                except Exception:
                    continue

            result[col_key] = pd.Series(returns)

    # 결과 DataFrame 생성
    result_df = pd.DataFrame(result)
    result_df.index.name = 'YearMonth'
    # 1. 월별 수익률 저장
    output_file = 'etf_result.csv'
    if os.path.exists(output_file):
        os.remove(output_file)
    result_df.to_csv(output_file, index=False)

    # 2. 누적 수익률 계산 및 저장 (추가된 부분)
    cumulative_returns = (1 + result_df).cumprod() - 1
    cumulative_file = 'etf_cumulative.csv'
    if os.path.exists(cumulative_file):
        os.remove(cumulative_file)
    cumulative_returns.to_csv(cumulative_file, index=False)

    # 통계 계산
    stats = []
    for col in result_df.columns:
        data = result_df[col].dropna()
        if len(data) == 0:
            continue
        
        # 누적 수익률 기반 계산
        cumulative = (1 + data).cumprod()
        total_return = cumulative.iloc[-1] - 1  # 최종 누적 수익률
        monthly_return = data.mean()
        annual_return = (1 + monthly_return)**12 - 1
        mdd = ((cumulative.cummax() - cumulative)/cumulative.cummax()).max()
        volatility = data.std()

        stats.append({
            'column': col,
            'total_return': total_return,
            'monthly_return': monthly_return,
            'annual_return': annual_return,
            'mdd': mdd,
            'volatility': volatility
        })

    stats_df = pd.DataFrame(stats)

    # 출력
    pd.set_option('display.float_format', '{:.4%}'.format)
    # print("\n🔍 전략별 성과 비교:")
    # print(stats_df.sort_values(by='total_return', ascending=False))

    # 최고 수익률 출력
    best_row = stats_df.loc[stats_df['total_return'].idxmax()]
    # print("\n📈 최고 수익률 전략:")
    # print(f"전략명: {best_row['column']}")
    # print(f"총 누적 수익률: {best_row['total_return']:.2%}")
    # print(f"연평균 수익률: {best_row['annual_return']:.2%}")
    return best_row['column'], best_row['total_return'], best_row['annual_return']
    # 파일 저장 정보 출력
    # print(f"\n✅ 저장된 파일:")
    # print(f"- 월별 수익률: {output_file}")
    # print(f"- 누적 수익률: {cumulative_file}")
