import locale

from entities import Country

locale.setlocale(locale.LC_ALL, '')


class Insight:
    def __init__(self):
        self.results_max = None
        self.cpa_min = None
        self.cpa_max = None
        self.reach_min = None
        self.load_country_insights()

    def load_country_insights(self):
        c = Country()
        dataset = c.dataset
        self.results_max = dataset.loc[dataset["Results"].idxmax()]
        self.cpa_min = dataset.loc[dataset["cpa"].idxmin()]
        self.cpa_max = dataset.loc[dataset["cpa"].idxmax()]
        self.reach_delta = dataset.loc[dataset["reach_delta"].idxmin()]

    def print_insights(self):
        # Most expensive to reach
        c = self.reach_delta
        country = c['Country']
        cpr = locale.currency(c['Cost per Result'], grouping=True)
        cppr = locale.currency(c['Cost per 1,000 People Reached'], grouping=True)
        msg = "The country {} has a CPA of {} greater than reaching 1,000 users ({})" \
              "".format(country, cpr, cppr)
        print(msg)
        print()

        # Most expensive CPA
        c = self.cpa_max
        country = c['Country']
        cpr = locale.currency(c['Cost per Result'], grouping=True)
        msg = "The country {} has the most expensive CPA of {}".format(country, cpr)
        print(msg)
        print()

        # Least expensive CPA
        c = self.cpa_min
        country = c['Country']
        cpr = locale.currency(c['Cost per Result'], grouping=True)
        msg = "The country {} has the least expensive CPA of {}".format(country, cpr)
        print(msg)
        print()


r = Insight()
r.print_insights()
