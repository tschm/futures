import pandas as pd

from .reference import reference


def chain(
    future_name,
    include_expired_contracts=True,
    after=None,
    before=None,
    connection=None,
):
    """
    :param future_name: A name of a futures, e.g. "CC1 Comdty"
    :param include_expired_contracts: either True or False
    :param before: if specified, ignore contracts with notice before this date
    :param after: if specified, ignore contracts with notice after this data
    :return: DataFrame with row FIGI code: {FUT_NOTICE_FIRST: date, TICKER: Bloomberg contract name}.
    Note that we avoid actual Bloomberg contract names such as CLM2 Comdty as this name is immutable!
    """
    include = "Y" if include_expired_contracts else "N"
    contracts = reference(
        tickers=future_name,
        fields="FUT_CHAIN",
        connection=connection,
        ovrds=("INCLUDE_EXPIRED_CONTRACTS", include),
    )

    # or [('INCLUDE_EXPIRED_CONTRACTS', include)]

    ref = reference(
        tickers=contracts,
        fields=["ID_BB_GLOBAL", "FUT_NOTICE_FIRST", "FUT_MONTH_YR"],
        connection=connection,
    )

    ref["FUT_NOTICE_FIRST"] = ref["FUT_NOTICE_FIRST"].apply(lambda stamp: pd.Timestamp(int(stamp) * 1e6).date())

    if before:
        ref = ref.loc[ref["FUT_NOTICE_FIRST"] >= before]

    if after:
        ref = ref.loc[ref["FUT_NOTICE_FIRST"] <= after]

    ref["TICKER"] = ref.index
    return ref.set_index("ID_BB_GLOBAL").sort_values(by="FUT_NOTICE_FIRST")


def ticker_continuous(
    ticker,
    pricing_source="EXCH",
    roll_type="N",
    number_of_days=0,
    number_of_months=0,
    roll_adjustment="N",
):
    """
    Function to create the Bloomberg ticker names for continuous futures
    :param ticker: A name for a future, such as CC1 Comdty
    :param pricing_source: usually "EXCH"
    :param roll_type:
                * N - Roll at first notice,
                * R - relative at expiration
    :param number_of_days: number of days prior to notice or expiration
    :param number_of_months: number of months prior to notice or expiration
    :param roll_adjustment:
                * N - no roll adjustment
                * D - roll adjustment by difference
                * W - roll adjustment by weighted average
                * R - roll adjustment by ratio
    :return:
    """

    if ticker.endswith("Index"):
        ticker = ticker[:-6]
        typ = "Index"

    if ticker.endswith("Comdty"):
        ticker = ticker[:-7]
        typ = "Comdty"

    if ticker.endswith("Curncy"):
        ticker = ticker[:-7]
        typ = "Curncy"

    return "{ticker} {roll_type}:{days:02d}_{months}_{roll_adj} {source} {typ}".format(
        ticker=ticker,
        roll_type=roll_type,
        days=number_of_days,
        months=number_of_months,
        roll_adj=roll_adjustment,
        source=pricing_source,
        typ=typ,
    )
