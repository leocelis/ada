import locale

from dimensions import Country

locale.setlocale(locale.LC_ALL, '')


class Insight:
    def __init__(self):
        self.results_max = None
        self.cpa_min = None
        self.cpa_max = None
        self.reach_min = None
        self.cpr_max = None
        self.load_country_insights()

    def load_country_insights(self):
        c = Country()
        dataset = c.dataset
        self.results_max = dataset.loc[dataset["Results"].idxmax()]
        self.cpa_min = dataset.loc[dataset["cpa"].idxmin()]
        self.cpa_max = dataset.loc[dataset["cpa"].idxmax()]
        self.reach_delta = dataset.loc[dataset["reach_delta"].idxmin()]
        self.cpr_max = dataset.loc[dataset["Cost per 1,000 People Reached"].idxmax()]

    def print_insights(self):
        # Most expensive to reach
        c = self.cpr_max
        country = c['Country']
        cppr = locale.currency(c['Cost per 1,000 People Reached'], grouping=True)
        msg = "\nThe country {} has the most expensive cost per 1,000 people reach of {}" \
              "".format(country, cppr)
        print(msg)
        print()

        # Most expensive to reach vs. cpa
        c = self.reach_delta
        country = c['Country']
        cpr = locale.currency(c['Cost per Result'], grouping=True)
        cppr = locale.currency(c['Cost per 1,000 People Reached'], grouping=True)
        msg = "\nThe country {} has the biggest delta between CPA ({}) and reaching 1,000 people ({})" \
              "".format(country, cpr, cppr)
        print(msg)
        print()

        # Most expensive CPA
        c = self.cpa_max
        country = c['Country']
        cpr = locale.currency(c['Cost per Result'], grouping=True)
        msg = "\nThe country {} has the most expensive CPA of {}".format(country, cpr)
        print(msg)
        print()

        # Least expensive CPA
        c = self.cpa_min
        country = c['Country']
        cpr = locale.currency(c['Cost per Result'], grouping=True)
        msg = "\nThe country {} has the least expensive CPA of {}".format(country, cpr)
        print(msg)
        print()


r = Insight()
r.print_insights()
