from get_data import *
from rebuild_date import *
from calculate_etf_returns import *
from score import *
from select_etf import *
from result import *
import itertools
import multiprocessing as mp
import csv
from tqdm import tqdm
#
def process_combination(params):
    try:
        score = calc_etf_momentum_score(calculate_close, params)
        ticker = select_etf_ticker(score)
        result = calculate_etf_performance(rebuild_close, ticker)

        name, value1, value2 = result
        return [params, name, round(value1, 2), round(value2, 2)]
    except Exception as e:
        print(f"Error with params {params}: {e}")
        return None

# 데이터 준비
df_close = fetch_etf_data('adj')
rebuild_close = rebuild_etf_data(df_close)
calculate_close = calculate_returns(rebuild_close)

def main():
    # 0 ~ 100까지 10단위 조합
    param_range = range(0, 101, 10)
    all_combinations = list(itertools.product(param_range, repeat=4))

    print(f"총 조합 수: {len(all_combinations)}")

    # 병렬 처리 (7개 코어)
    with mp.Pool(processes=7) as pool:
        results = list(tqdm(pool.imap_unordered(process_combination, all_combinations), total=len(all_combinations)))

    # 결과 필터링 및 저장
    valid_results = [r for r in results if r is not None]

    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Params', 'Name', 'Value1', 'Value2'])
        writer.writerows(valid_results)

    print("저장 완료: output.csv")

if __name__ == "__main__":
    main()