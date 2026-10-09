import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column

# Load a quick summary or sample of your data to keep it light
df = pd.read_csv('nyc_311_2024.csv', low_memory=False, nrows=50_000)
df['Created Date'] = pd.to_datetime(df['Created Date'], format='mixed', errors='coerce')
daily_counts = df.groupby(df['Created Date'].dt.date).size().reset_index(name='count')

# Create a Bokeh figure
p = figure(title="Daily NYC 311 Complaints", x_axis_type='datetime', width=800, height=400)
p.line(pd.to_datetime(daily_counts['Created Date']), daily_counts['count'], line_width=2, color='navy')

# Add to Bokeh document root
curdoc().add_root(column(p))
curdoc().title = "NYC 311 Dashboard"
