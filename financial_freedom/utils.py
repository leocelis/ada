import datetime

from dateutil.relativedelta import relativedelta

from settings import *


def expected_performance():
    """
    Expected monthly income based on net worth and expected performance

    :param net_worth:
    :return:
    """
    r = round((net_worth() * AVG_PORTFOLIO_PERFORMANCE) / 12, 2)
    return r


def portfolio_distribution():
    """
    N/1 distribution among different types of assets

    :param net_worth:
    :return:
    """
    r = round(net_worth() / len(ASSET_CATEGORY), 2)
    return r


def net_worth():
    """
    Return net worth in USD
    :return:
    """
    ars_value = 60629269.44
    net_worth = round(ars_value / USD_ARS_EXCHANGE_RATE, 2)
    return net_worth


def plan_length_years():
    """
    Return the length in years for the current plan
    :return:
    """
    return RETIREMENT_AGE - CURRENT_AGE


def year_end():
    y = plan_length_years()

    add_years = datetime.datetime.today() + relativedelta(years=+y)
    return add_years


def monthly_savings():
    """
    Get the monthly savings
    :return:
    """
    monthly_savings = MONTHLY_INCOME - MONTHLY_EXPENSES
    return monthly_savings