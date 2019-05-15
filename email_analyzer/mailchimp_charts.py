import os
import sys

import plotly
import plotly.graph_objs as go
import plotly.plotly as py

sys.path.append(os.path.dirname(os.getcwd()))
from ada.email_analyzer.utils import get_top_opens, get_top_open_rate

PLOTLY_USERNAME = os.environ.get('PLOTLY_USERNAME')
PLOTLY_API_KEY = os.environ.get('PLOTLY_API_KEY')
plotly.plotly.sign_in(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)

# top opens
top_opens = get_top_opens(limit=5)
x = []
y = []
for o in top_opens:
    x.append(o.get('email_subject'))
    y.append(o.get('unique_opens'))

data = [go.Bar(
    x=x,
    y=y,
    # orientation='h',
    text=y,
    textposition='inside',
    opacity=0.7,
    marker=dict(
        color=['rgb(49,130,189)', 'rgb(58,200,225)', 'rgb(58,200,225)', 'rgb(58,200,225)', 'rgb(58,200,225)'],
        line=dict(
            color='rgb(49,130,189)',
            width=1.5,
        )
    ))]

layout = go.Layout(
    title='Top 5 Posts by Email Opens',
)

fig = go.Figure(data=data, layout=layout)

# top open rate
top_open_rate = get_top_open_rate(limit=5)
x = []
y = []
for o in top_open_rate:
    open_rate = "{}%".format(int(o.get('open_rate', 0) * 100))
    x.append(o.get('email_subject'))
    y.append(open_rate)

data2 = [go.Bar(
    x=x,
    y=y,
    # orientation='h',
    text=y,
    textposition='inside',
    opacity=0.7,
    marker=dict(
        color=['rgb(49,130,189)', 'rgb(58,200,225)', 'rgb(58,200,225)', 'rgb(58,200,225)', 'rgb(58,200,225)'],
        line=dict(
            color='rgb(49,130,189)',
            width=1.5,
        )
    ))]

layout2 = go.Layout(
    title='Top 5 Posts by Open Rate',
)

fig2 = go.Figure(data=data2, layout=layout2)

# update charts
py.plot(fig, filename='Top 5 Posts by Email Opens')
py.plot(fig2, filename='Top 5 Posts by Open Rate')
