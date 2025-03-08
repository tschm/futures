from futures.bloomberg.ticker import ticker_continuous


def test_ticker():
    x = ticker_continuous(ticker="RX1 Comdty")
    assert x == "RX1 N:00_0_N EXCH Comdty"

    x = ticker_continuous(ticker="AAA Index", roll_type="R", number_of_days=5)
    assert x == "AAA R:05_0_N EXCH Index"

    x = ticker_continuous(ticker="AAA Curncy", roll_type="N", number_of_months=1)
    assert x == "AAA N:00_1_N EXCH Curncy"
