"""
RULES
- Clone a site for Latam

Projected revenue:
1) Find 3 business that are similar
2) Find the visits (https://app.neilpatel.com/en/traffic_analyzer/overview)
3) Use AdSense calculator (https://www.google.com/adsense/start/#calculator)
"""
from plan import perc_of_goal
from project import estimated_completion_time, estimated_total_cost, PROJECT_TASK

REVENUE_SOURCE = ('ADSENSE', 'AFFILIATE', 'PAID_SUBSCRIPTION')

COMPETITORS = {
    "twitchtracker.com": {
        "organic_monthly_traffic": 187484,
        "potential_monthly_revenue": (9320 / 12)
    },
    "neilpatel.com": {
        "organic_monthly_traffic": 3292343,
        "potential_monthly_revenue": (719293 / 12)
    },
    "andrewchen.co": {
        "organic_monthly_traffic": 50643,
        "potential_monthly_revenue": (10986 / 12)
    },
    "sitechecker.pro": {
        "organic_monthly_traffic": 499230,
        "potential_monthly_revenue": (79888 / 12)
    },
    "coschedule.com": {
        "organic_monthly_traffic": 438098,
        "potential_monthly_revenue": (94781 / 12)
    },
    "weworkremotely.com": {
        "organic_monthly_traffic": 128218,
        "potential_monthly_revenue": (14505 / 12)
    },
    "jeffbullas.com": {
        "organic_monthly_traffic": 145594,
        "potential_monthly_revenue": (31699 / 12)
    },
    "statista.com": {
        "organic_monthly_traffic": 145594,
        "potential_monthly_revenue": (31699 / 12)
    },
    "emagister.com.ar": {
        "organic_monthly_traffic": 60022,
        "potential_monthly_revenue": (7298 / 12)
    }
}

BUSINESS_PORTFOLIO = {
    # 'twitch_rank': {
    #     'monthly_traffic_estimate': COMPETITORS["twitchtracker.com"]['organic_monthly_traffic'],
    #     'revenue_monthly_estimate': COMPETITORS["twitchtracker.com"]['potential_monthly_revenue'],
    #     'main_strategy': "Copycat of TwitchTracker for Latin America",
    #     'story': "Discover what to watch next on Twitch.tv",
    #     'minimum_viable_audience': "twitch streamers",
    #     'turn_down_reason': "it doesn't add value to the rest of the quadrants"
    # },
    'blog': {
        'monthly_traffic_estimate': COMPETITORS["andrewchen.co"]['organic_monthly_traffic'],
        'revenue_monthly_estimate': COMPETITORS["andrewchen.co"]['potential_monthly_revenue'],
        'main_strategy': "",
        'minimum_viable_audience': "Growth hackers"
    },
    # 'leocelis': {
    #     'monthly_traffic_estimate': 0,
    #     'revenue_monthly_estimate': 0,
    #     'main_strategy': "",
    #     'minimum_viable_audience': "Silicon Valley startups founders with no P&E experience"
    # },
    'ada': {
        'monthly_traffic_estimate': COMPETITORS["sitechecker.pro"]['organic_monthly_traffic'],
        'revenue_monthly_estimate': COMPETITORS["sitechecker.pro"]['potential_monthly_revenue'],
        'main_strategy': "free without wait marketing analytics alternative",
        "tech_strategy": "Automate to bring the cost to nearly free (yahoo > to pagerank)",
        'story': "Advanced Data Analytics and Tracking for Marketing Professionals",
        'minimum_viable_audience': "Growth hackers"
    },
    'trabajamos_remoto': {
        'monthly_traffic_estimate': COMPETITORS["weworkremotely.com"]['organic_monthly_traffic'],
        'revenue_monthly_estimate': COMPETITORS["weworkremotely.com"]['potential_monthly_revenue'],
        'main_strategy': "Copycat of WWR for Latin America",
        'minimum_viable_audience': "latin america small business founders",
        'purchased_daily_hours': 2
    },
    # 'cursosrosario': {
    #     'revenue_monthly_estimate': COMPETITORS["emagister.com.ar"]['potential_monthly_revenue'],
    #     'main_strategy': "Indexador de cursos en rosario",
    #     'minimum_viable_audience': "rosarinos que buscan cursos",
    #     'turn_down_reason': "it doesn't add value to the rest of the quadrants"
    # }
}


def run():
    # Revenue potential by project
    for key, value in BUSINESS_PORTFOLIO.items():
        print()
        print(str(key).upper())
        est_monthly_rev = round(BUSINESS_PORTFOLIO[key]['revenue_monthly_estimate'], 2)
        est_monthly_traffic = round(BUSINESS_PORTFOLIO[key]['monthly_traffic_estimate'], 2)
        perc = round(perc_of_goal(est_monthly_rev), 2)

        print("Estimated monthly views: {:,}".format(est_monthly_traffic))
        print("Estimated monthly revenue: {:,}".format(est_monthly_rev))
        print("Percentage of the monthly goal: {:,}".format(perc))

        # if there are tasks for this business
        tasks = PROJECT_TASK.get(key)
        if tasks:
            hours = 0
            for k, v in tasks.items():
                hours += tasks[k].get('hours', 0)
            est_total_cost = estimated_total_cost(total_hours=hours)

            # if there are purchased time
            available_hours = BUSINESS_PORTFOLIO[key].get('purchased_daily_hours', 0)
            est_comp_time = estimated_completion_time(total_hours=hours,
                                                      available_hours=available_hours)
            print("Estimated hours: {}".format(hours))
            print("Estimated cost: {:,}".format(est_total_cost))
            print("Estimated completion time: {:,} year(s)".format(est_comp_time))
