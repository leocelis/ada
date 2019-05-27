import matplotlib.pyplot as plot
from dimensions import Country, Day


class Charts:
    def __init__(self):
        c = Country()
        d = Day()
        self.country_dataset = c.dataset
        self.day_dataset = d.dataset

    def country_generate_charts(self):
        # show cpa by country
        self.country_dataset.plot.bar(y='cpa', x='Country', rot=0)
        plot.title('CPA by Country')
        plot.ylabel('CPA')
        plot.xlabel('Country')
        plot.show()
        # plot.savefig('reports/cpa_by_country.png')

        # show results by country
        self.country_dataset.plot.bar(y='Leads (Form)', x='Country', rot=0)
        plot.title('Results by Country')
        plot.ylabel('Leads (Form)')
        plot.xlabel('Country')
        plot.show()
        # plot.savefig('reports/results_by_country.png')

        fig, ax = plot.subplots()
        x = self.country_dataset['Country']
        y = self.country_dataset['Cost per 1,000 People Reached']
        y_1 = self.country_dataset['Cost per Lead (Form)']
        ax.plot(x, y, linestyle='--')
        ax.plot(x, y_1, linestyle='--')
        ax.set_title("Cost per 1,000 People Reached vs. Cost per Lead")
        plot.show()
        # plot.savefig('reports/cost_per_reach.png')

    def day_generate_charts(self):
        # show cost per reach daily variation
        self.day_dataset.plot(y='Cost per 1,000 People Reached', x='Day')
        plot.title('Cost per reach daily variation')
        plot.ylabel('Cost per 1,000 People Reached')
        plot.xlabel('Day')
        plot.xticks(self.day_dataset.index, self.day_dataset['Day'], rotation=90)  # rotate x legends
        ax = plot.gca()
        ax.invert_xaxis()  # invert x orientation
        plot.show()
        # plot.savefig('reports/reach_daily_variation.png')


c = Charts()
c.country_generate_charts()
c.day_generate_charts()
