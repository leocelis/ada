"""
Delivery Analysis on Facebook

Steps:
1. In FB Ads Reporting, export a CSV with Country, Amount Spent, Reach, Results
2. Rename it to results-by-country.csv and paste it in this folder
3. Run python3 delivery.py
4. Review png files generated

"""
import matplotlib.pyplot as plot
import pandas as pd

# =================
# Country Analysis
# =================

# min relevant total results
results_threshold = 1
# min spend
min_spend = 10

# load results by country
dataset = pd.DataFrame.from_csv("results-by-country.csv", index_col=None)  # ignore index column

# remove countr without reach
dataset = dataset[dataset.Reach > 0]

# remove countries without min spend
dataset = dataset[dataset['Amount Spent (USD)'] >= min_spend]

# remove countries with more than one result
dataset = dataset[dataset.Results > results_threshold]

# add cost per result column
dataset['cpa'] = (dataset['Amount Spent (USD)'] / dataset.Results)

# add cost per reach
dataset['cpr'] = (dataset['Amount Spent (USD)'] / dataset.Reach)

# countries with most conversions
results_max = dataset.loc[dataset["Results"].idxmax()]
cpa_min = dataset.loc[dataset["cpa"].idxmin()]

# outputs
print()
print("========================")
print("Country with most results")
print("========================")
print(results_max)
print()
print()
print("========================")
print("Country with lowest CPA")
print("========================")
print(cpa_min)

# show cpa by country
dataset.plot.bar(y='cpa', x='Country', rot=0)
plot.title('CPA by Country')
plot.ylabel('CPA')
plot.xlabel('Country')
# plot.show()
plot.savefig('cpa_by_country.png')

# show results by country
dataset.plot.bar(y='Results', x='Country', rot=0)
plot.title('Results by Country')
plot.ylabel('Results')
plot.xlabel('Country')
# plot.show()
plot.savefig('results_by_country.png')
