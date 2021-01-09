"""
GOAL: monthly cash flow from my assets is equal to or greater than my monthly living expenses

STRATEGY:
- Buy or create assets that generate cash flow
- Cash flow from assets pay living expenses

RULES:
- 1/N = divide the same amount across all the assets
- Choose asset where time to cash flow is less than the longest asset's life expectancy
- $500 - $1,000 / mo. potential range
"""

from utils import *

# ============================================
# INPUTS
# ============================================

# Assets options
assets = {
    "stocks": {
        "category": ASSET_CATEGORY[0],
        "market_avg_return": 9.2,  # https://www.businessinsider.com/personal-finance/average-stock-market-return
        "total_investment": 121580,
        "monthly_hours": 2
    },
    "real_estate": {
        "category": ASSET_CATEGORY[1],
        # https://www.on24.com.ar/negocios/barrio-martin-se-posiciona-como-el-mas-rentable-de-rosario-segun-mercado-libre-cuanto-rinde/
        "market_avg_return": 2.4,
        "total_investment": (175000 + 150000),
        "price_per_unit": 150000,
        "monthly_hours": 15
    },
    # "don_mateo": {
    #     "category": ASSET_CATEGORY[1],
    #     # https://www.on24.com.ar/negocios/barrio-martin-se-posiciona-como-el-mas-rentable-de-rosario-segun-mercado-libre-cuanto-rinde/
    #     "market_avg_return": 2.4,
    #     "total_investment": 100000,
    #     "monthly_hours": 15
    # },
    # "trabajamos_remoto": {
    #     "category": ASSET_CATEGORY[2],
    #     "market_avg_return": 14.71,  # https://csimarket.com/Industry/industry_ManagementEffectiveness.php?ind=1011
    #     "total_investment": 5000,
    #     "monthly_hours": 2
    # },
    "business": {
        "category": ASSET_CATEGORY[2],
        "market_avg_return": 14,  # https://csimarket.com/Industry/industry_ManagementEffectiveness.php?ind=1011
        "total_investment": 0,
        "monthly_hours": 15
    },
    # "twitch_rank": {
    #     "category": ASSET_CATEGORY[2],
    #     "market_avg_return": 14.71,  # https://csimarket.com/Industry/industry_ManagementEffectiveness.php?ind=1011
    #     "total_investment": 0,
    #     "monthly_hours": 15
    # },
    # "rings": {
    #     "category": ASSET_CATEGORY[2],
    #     "market_avg_return": 14.71,  # https://csimarket.com/Industry/industry_ManagementEffectiveness.php?ind=1011
    #     "total_investment": 0,
    #     "monthly_hours": 160
    # },
    # "casa_celis": {
    #     "category": ASSET_CATEGORY[2],
    #     # https://www.on24.com.ar/negocios/barrio-martin-se-posiciona-como-el-mas-rentable-de-rosario-segun-mercado-libre-cuanto-rinde/
    #     "market_avg_return": 2.4,
    #     "total_investment": 75000,
    #     "monthly_hours": 15
    # },
}

# settings
current_currency = CURRENCY[0]  # set to USD first

# plan
# monthly_goal = MONTHLY_EXPENSES * 1.5  # 50% safety net
monthly_goal = MONTHLY_EXPENSES
safety_net = monthly_goal * 12


# available_to_invest = LIQUID_ASSETS_TOTAL - safety_net


def perc_of_goal(monthly_revenue):
    """
    Return the percentage that represents of the monthly goal

    :param monthly_revenue:
    :return:
    """
    perc = (monthly_revenue * 100) / monthly_goal
    return perc


def run():
    # distribution
    print("================================================")
    print("SUMMARY")
    print("------------------------------------------------")
    print("Net worth: {:,}".format(net_worth()))
    print("Expected monthly passive income: {:,}".format(expected_performance()))
    print("Monthly goal: {:,}".format(monthly_goal))
    print("N/1 distribution per asset category: {:,}".format(portfolio_distribution()))
    print("Monthly savings: {:,}".format(monthly_savings()))
    print("Safety net: {:,}".format(safety_net))
    print("Years left in plan: {}".format(plan_length_years()))
    print("Plan end year: {}".format(year_end()))
    # print("Available to invest: {:,}".format(available_to_invest))
    print("================================================")

    # investment needed for each asset
    accumulated_monthly_investment = 0
    for key, value in assets.items():
        market_avg_return = assets[key]['market_avg_return']
        total_investment = assets[key]['total_investment']
        market_monthly_return = round(((market_avg_return * UNIT) / 100) / 12, 4)
        total_investment_needed = round((monthly_goal * UNIT) / market_monthly_return, 2)
        total_investment_left = round(total_investment_needed - total_investment, 2)
        months_needed = round(total_investment_left / monthly_savings(), 2)
        years_needed = round(months_needed / 12)

        print("\n{}".format(str(key).upper()))
        print("market monthly return (USD{}): {:,}".format(UNIT, market_monthly_return))
        print("total investment needed: {:,}".format(total_investment_needed))
        print("total investment left: {:,}".format(total_investment_left))
        # print("time required left: {} months ({} year(s))".format(months_needed, years_needed))

        # check if meets the plan
        years_spare = plan_length_years() - years_needed
        if years_spare < 0:
            print("**** ALERT! THIS IS BEYOND THE PLAN ****")
        else:
            recommended_monthly_investment = round(total_investment_left / (plan_length_years() * 12), 2)
            estimate_year_completion = int(datetime.datetime.now().year) + years_needed
            # print("Estimate completion: {}".format(estimate_year_completion))
            print("Recommended monthly investment: {:,}".format(recommended_monthly_investment))

            # accumulated monthly investment
            accumulated_monthly_investment += recommended_monthly_investment

        # Don Mateo
        # if key == 'don_mateo' or key == 'casa_celis':
        #     how_many = round(total_investment_needed / total_investment)
        #     print("*** How many are needed: {}".format(how_many))    # Don Mateo

        if key == 'real_estate':
            how_many = round(total_investment_left / assets[key]['price_per_unit'])
            print("*** How many are needed: {}".format(how_many))

    print("\n================================================")
    print("Total accumulated monthly investment: {:,}".format(round(accumulated_monthly_investment, 2)))
    if accumulated_monthly_investment > monthly_savings():
        print("**** MORE THAN YOU CAN INVEST!")
    print(
        "Total available monthly investment: {:,}".format(round(monthly_savings() - accumulated_monthly_investment, 2)))
    print("================================================\n")
