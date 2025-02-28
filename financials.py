import yfinance as yf


def get_financials(ticker_list):
    ticker_metrics = {}
    for ticker in ticker_list:
        ticker_metrics.update(get_financials_helper(ticker))
    return ticker_metrics



def get_financials_helper(ticker):

    ticker_metrics = {}

    stock = yf.Ticker(ticker)
    enterprise_value = stock.info.get('enterpriseValue')

    income_stmt = stock.income_stmt

    try:
        normalized_ebitda = income_stmt.loc['Normalized EBITDA'].iloc[0]
    except Exception as e:
        normalized_ebitda = None
        print(f"{ticker}: Could not retrieve Normalized EBITDA - {e}")

    try:
        total_revenue = income_stmt.loc['Total Revenue'].iloc[0]
    except Exception as e:
        total_revenue = None
        print(f"{ticker}: Could not retrieve Total Revenue - {e}")

    ticker_metrics[ticker] = {
        'enterprise_value': enterprise_value,
        'normalized_ebitda': normalized_ebitda,
        'total_revenue': total_revenue
    }
    return ticker_metrics


