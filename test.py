# create sample data
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
data = px.data.gapminder().query("year == 2007").sort_values(by="pop", ascending=False).head(10)

# create bar chart
fig = px.bar(data, x="pop", y="country", orientation="h", title="Population of the Top 10 Most Populous Countries in 2007")

# add custom text
annotations = []
for country, population in zip(data["country"], data["pop"]):
    annotations.append(dict(xref='x', yref='y', x=population+3, y=country,
                            text='{:,}'.format(population), font=dict(size=15),
                            showarrow=False))
fig.update_layout(annotations=annotations)

# show chart
fig.show()