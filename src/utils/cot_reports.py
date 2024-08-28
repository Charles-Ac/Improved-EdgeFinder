from enum import Enum

import numpy as np
from pycot.reports import CommitmentsOfTraders


def print_all_contract_names():
    contracts: np.ndarray = cot.list_available_contracts()
    for contract in contracts:
        print(contract)


class Market(Enum):
    ...


class CurrencyMarket(Market):
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
    BTC = dict(
        contract_name="BITCOIN - CHICAGO MERCANTILE EXCHANGE",
        name="BITCOIN",
        abbr="BTC"
    )


class IndicesMarket(Market):
    ...


class CommodityMarket(Market):
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


class CotReportsHandler:
    """
    This class is responsible for handling various operations related to COT reports.
    Such operations include downloading, processing, and possibly analyzing the reports.
    """

    def __init__(self) -> None:
        self.cot: CommitmentsOfTraders = CommitmentsOfTraders(report_type="legacy_fut")


if __name__ == '__main__':
    cot = CommitmentsOfTraders(report_type="legacy_fut")
    contract_names = ("AUSTRALIAN DOLLAR", "EURO FX")
    print(cot.report(contract_names).head())

