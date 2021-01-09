"""
TODO Which feature has more value if shared with other users?
"""
from quadrant import BUSINESS_OWNER_AVAILABLE_DAILY_HOURS, SELF_EMPLOYEE_RATE

PROJECT_TASK = {
    "twitch_rank": {
        "website setup": {"hours": 40},
        "subscribers": {"hours": 40},
        "stats": {"hours": 40},
        "clips": {"hours": 40},
        "channels": {"hours": 40},
        "promotion": {"hours": 160},
        "seo": {"hours": 160},
    },
    "trabajamos_remoto": {
        "Company automatic invitations": {"hours": 80},
        "Company sign up": {"hours": 80},
        "Company admin panel": {"hours": 160},
        "Candidates sign up": {"hours": 80},
        "Candidates admin panel": {"hours": 160},
        "SEO optimization": {"hours": 160},
        "AdSense optimization": {"hours": 160},
    },
    # "cursosrosario": {
    #     "Herramienta de busqueda de cursos": {"hours": 80},
    #     "Indexador de cursos publicados en fb": {"hours": 160},
    #     "Categorias y listado de cursos": {"hours": 80},
    #     "Optimization de SEO": {"hours": 160},
    #     "Indexador de cursos de la web": {"hours": 160},
    # },
    "blog": {
        # "Optimization de SEO": {"hours": 160},
        "Posts": {"hours": 322}  # (648 posts from Andrew Chen - 322 already published 10.28.20)
    },
    "ada": {
        "home page dashboard": {"hours": 40},
        "headline analyzer": {
            "hours": 160,
            "competitor_feature": "https://coschedule.com/headline-studio"
        },
        # "ADA API": {
        #     "hours": 320,
        #     "competitor_feature": "https://docs.craft.co/"
        # },
        "Company search": {
            "hours": 960,
            "competitor_feature": "https://craft.co/search?order=size_desc"
        },
        "Content analytics": {
            "scope": "analyze content related to the company and extract metrics from social media",
            "hours": 960,
            "competitor_feature": "https://craft.co/search?order=size_desc"
        },
        "Data tracking": {
            "scope": "Alerts about executive changes, stock drops and ups",
            "hours": 960,
            "competitor_feature": "https://craft.co/palantir-technologies/executives"
        },
        "Data platform": {
            "scope": "News, website, API data collection about companies and people",
            "hours": 960,
            "competitor_feature": ""
        }
    }
}


def estimated_completion_time(total_hours, available_hours=0):
    """
    Return estimated completion time for a project in months

    :param total_hours: total hours for the project
    :return:
    """
    if not available_hours:
        available_hours = BUSINESS_OWNER_AVAILABLE_DAILY_HOURS

    months = round(((total_hours / available_hours) / 20) / 12, 2)
    return months


def estimated_total_cost(total_hours, rate=0):
    """
    Return total estimate cost for a project

    :param total_hours: total hours for the project
    :param rate: rate for the engineer assigned
    :return:
    """
    if not rate:
        rate = SELF_EMPLOYEE_RATE

    return round(rate * total_hours, 2)
