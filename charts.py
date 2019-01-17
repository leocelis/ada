import matplotlib.pyplot as plot
from entities import Country


class Charts:
    def __init__(self):
        c = Country()
        self.dataset = c.dataset

    def generate_charts(self):
        # show cpa by country
        self.dataset.plot.bar(y='cpa', x='Country', rot=0)
        plot.title('CPA by Country')
        plot.ylabel('CPA')
        plot.xlabel('Country')
        # plot.show()
        plot.savefig('cpa_by_country.png')

        # show results by country
        self.dataset.plot.bar(y='Results', x='Country', rot=0)
        plot.title('Results by Country')
        plot.ylabel('Results')
        plot.xlabel('Country')
        # plot.show()
        plot.savefig('results_by_country.png')

        fig, ax = plot.subplots()
        x = self.dataset['Country']
        y = self.dataset['Cost per 1,000 People Reached']
        y_1 = self.dataset['Cost per Result']

        line1, = ax.plot(x, y, linestyle='--')
        line2, = ax.plot(x, y_1, linestyle='--')

        ax.legend()
        # plot.show()
        plot.savefig('cost_per_reach.png')


c = Charts()
c.generate_charts()
