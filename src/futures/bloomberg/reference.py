import logging

import pandas as pd
from xbbg import pipeline
from xbbg.core import process

from .conn import connect


def reference(tickers, flds=None, logger=None, connection=None, **kwargs):
    """
    Bloomberg reference data

    Args:
        tickers: list of tickers
        flds: fields to subscribe

    Returns:
        frame: Bloomberg reference Data

    """
    logger = logger or logging.getLogger(__name__)

    if isinstance(tickers, str):
        tickers = [tickers]
    if isinstance(flds, str):
        flds = [flds]

    request = process.create_request(
        service="//blp/refdata",
        request="ReferenceDataRequest",
        **kwargs,
    )
    process.init_request(request=request, tickers=tickers, flds=flds, **kwargs)
    logger.debug(f"Sending request to Bloomberg ...\n{request}")

    with connect(connection=connection) as session:
        session.sendRequest(request=request)

        res = pd.DataFrame(process.rec_events(func=process.process_ref, **kwargs))
        if kwargs.get("raw", False):
            return res

        if res.empty or any(fld not in res for fld in ["ticker", "field"]):
            return pd.DataFrame()

        return (
            res.set_index(["ticker", "field"])
            .unstack(level=1)
            .rename_axis(index=None, columns=[None, None])
            .droplevel(axis=1, level=0)
            .loc[:, res.field.unique()]
            .pipe(pipeline.standard_cols, col_maps=kwargs.get("col_maps", None))
        )
