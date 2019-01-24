import pandas as pd


class Dimension:
    def __init__(self):
        return

    def data_load(self, filename="default.csv"):
        self.dataset = pd.DataFrame.from_csv(filename, index_col=None)  # ignore index column


class Day(Dimension):
    """
    Analyze data by day
    """

    def __init__(self):
        super().__init__()

        self.data_load(filename='day.csv')
        return


class Country(Dimension):
    """
    Analyze data by country
    """

    def __init__(self):
        super().__init__()
        # in dollars
        self.min_spend = 1
        self.results_threshold = 0
        self.dataset = None

        # initialize
        self.data_load(filename='country.csv')
        self.data_cleanup()
        self.add_extra_fields()

    def data_cleanup(self):
        # remove country without reach
        self.dataset = self.dataset[self.dataset.Reach > 0]

        # remove countries without min spend
        self.dataset = self.dataset[self.dataset['Amount Spent (USD)'] >= self.min_spend]

        # remove countries with more than one result
        self.dataset = self.dataset[self.dataset.Results > self.results_threshold]

    def add_extra_fields(self):
        # add cost per result column
        self.dataset['cpa'] = (self.dataset['Amount Spent (USD)'] / self.dataset.Results)

        # add cost per reach
        self.dataset['cpr'] = (self.dataset['Amount Spent (USD)'] / self.dataset.Reach)

        # delta between cost per reach and cost per result
        reach_delta = self.dataset['Cost per 1,000 People Reached'] - self.dataset['Cost per Result']
        self.dataset['reach_delta'] = reach_delta
