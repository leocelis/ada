# TODO This forecast is based on savings, use other leverages as reinvesting or debt

# With the current level of income how many months until I reach my goal
from utils import *


def run():
    print("\n================================================")
    print("FORECAST")
    print("------------------------------------------------")
    print("Expected yearly performance: {}%".format(round(AVG_PORTFOLIO_PERFORMANCE * 100)))
    # get performance of current net worth
    estimated_mo_passive_income = (net_worth() * AVG_PORTFOLIO_PERFORMANCE) / 12
    print("Estimated mo. income based on net worth: ${:,}".format(round(estimated_mo_passive_income, 2)))

    # find yearly delta
    delta_monthly_goal = MONTHLY_EXPENSES - estimated_mo_passive_income
    print("Mo. delta to meet the goal: ${:,}".format(round(delta_monthly_goal, 2)))

    # calculate how much to get that performance
    year_goal = delta_monthly_goal * 12
    delta_year_goal = year_goal / AVG_PORTFOLIO_PERFORMANCE
    print("Money left to meet the goal: ${:,}".format(round(delta_year_goal)))

    # calculate time left to goal
    months_left_to_goal = delta_year_goal / monthly_savings()
    print("Months left to meet the goal: {}".format(round(months_left_to_goal)))
    print("Years left to meet the goal: {}".format(round(months_left_to_goal / 12, 2)))
