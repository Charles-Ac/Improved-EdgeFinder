from enum import Enum

import pandas
from pycot.reports import CommitmentsOfTraders


class Market(Enum):
    """
    A Market is simply any asset that is reported in the COT reports
    """
    ...


class CurrencyMarket(Market):
    """
    Currencies that are reported in the COT reports
    """
    AUD = dict(
        contract_name="AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        name="AUSTRALIAN DOLLAR",
        abbr="AUD"
    )
    CAD = dict(
        contract_name="CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        name="CANADIAN DOLLAR",
        abbr="CAD"
    )
    CHF = dict(
        contract_name="SWISS FRANC - CHICAGO MERCANTILE EXCHANGE",
        name="SWISS FRANC",
        abbr="CHF"
    )
    EUR = dict(
        contract_name="EURO FX - CHICAGO MERCANTILE EXCHANGE",
        name="EURO",
        abbr="EUR"
    )
    GBP = dict(
        contract_name="BRITISH POUND - CHICAGO MERCANTILE EXCHANGE",
        name="BRITISH POUND",
        abbr="GBP"
    )
    JPY = dict(
        contract_name="JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE",
        name="JAPANESE YEN",
        abbr="JPY"
    )
    NZD = dict(
        contract_name="NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE",
        name="NZ DOLLAR",
        abbr="NZD"
    )
    USD = dict(
        contract_name="U.S. DOLLAR-ECU - CHICAGO MERCANTILE EXCHANGE",
        name="U.S. DOLLAR",
        abbr="USD"
    )


class CryptoMarket(Market):
    """
    CryptoCurrencies that are reported in the COT reports
    """
    BTC = dict(
        contract_name="BITCOIN - CHICAGO MERCANTILE EXCHANGE",
        name="BITCOIN",
        abbr="BTC"
    )


class IndicesMarket(Market):
    """
    Indices That are reported in the COT reports
    """
    ...


class CommodityMarket(Market):
    """
    Commodities that are reported in the COT reports
    """
    GOLD = dict(
        contract_name="GOLD - COMMODITY EXCHANGE INC",
        name="GOLD",
        abbr="XAU"
    )
    PLATINUM = dict(
        contract_name="PLATINUM - COMMODITY EXCHANGE INC",
        name="PLATINUM",
        abbr="XPT"
    )
    SILVER = dict(
        contract_name="SILVER - COMMODITY EXCHANGE INC",
        name="SILVER",
        abbr="XAG"
    )


class ReportType(Enum):
    """
    Types of the COT report that can be extracted.
    """
    LEGACY_FUTURES_ONLY = "legacy_fut"
    DISAGGREGATED_FUTURES_ONLY = "disaggregated_fut"
    TRADERS_IN_FINANCIAL_FUTURES = "traders_in_financial_futures_fut"


class CotReportsHandler:
    """
    This class is responsible for handling various operations related to COT reports.
    Such operations include downloading, processing, and possibly analyzing the reports.
    """

    def __init__(self, report_type: ReportType = ReportType.LEGACY_FUTURES_ONLY) -> None:
        self._cot: CommitmentsOfTraders = CommitmentsOfTraders(report_type=report_type.value)

    def get_market_reports(self, market: Market) -> pandas.DataFrame:
        """
        Returns years of COT report of the given market.
        Args:
            market (Market): A Market is simply any asset that is reported in the COT reports.

        Returns:
            pandas.DataFrame: A pandas dataframe of the market COT report.
        """
        contract_name: str = market.value["contract_name"]
        return self._cot.report(contract_name)
