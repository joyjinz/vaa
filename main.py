from get_data import *
from rebuild_date import *
from calculate_etf_returns import *
from score import *
from select_etf import *
from result import *

if __name__ == "__main__":
    # df_close = fetch_etf_data()
    df_close = fetch_etf_data('adj')
    print(df_close)
    rebuild_close=rebuild_etf_data(df_close)
    print(rebuild_close)

    calculate_close=calculate_returns(rebuild_close)
    print(calculate_close)
    score = calc_etf_momentum_score(calculate_close, [82, 3, 10, 7])
    print(score)
    ticker = select_etf_ticker(score)
    print(ticker)
    result = calculate_etf_performance(rebuild_close, ticker)