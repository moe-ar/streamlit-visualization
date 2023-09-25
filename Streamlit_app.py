import streamlit as st
import plotly.express as px
import pandas as pd

# Sample data (you should replace this with your actual data)

csv_file_path = 'epl2020.csv'
premier_league_data = pd.read_csv(csv_file_path)



# Visualization 1: Stacked Bar Chart

# Assuming your DataFrame is named 'premier_league_data'

st.header("Visualization 1: Premier League Team Performance (Wins, Draws, and Losses)")

# Interactive feature 1 for Visualization 1: Dropdown to select metric
metric_options = ['wins', 'draws', 'loses']
selected_metric = st.selectbox("Select Metric", metric_options)

# Interactive feature 2 for Visualization 1: Radio button to select sorting order
sort_options = ['Ascending', 'Descending']
selected_sort = st.radio("Sort Teams By", sort_options)

# Calculate the sum of the selected metric
filtered_data = premier_league_data[['teamId', selected_metric]].groupby('teamId')[selected_metric].sum().reset_index()


# Sort the data based on the selected sorting order and metric
if selected_sort == 'Ascending':
    ascending_order = True
else:
    ascending_order = False



filtered_data = filtered_data.sort_values(by=selected_metric, ascending=ascending_order)

# Create the bar chart
fig = px.bar(filtered_data, x='teamId', y=selected_metric,
             labels={'teamId': 'Team', selected_metric: 'Number of Matches'},
             title=f'Premier League Team Performance ({selected_metric.capitalize()})',
             hover_name='teamId', color_discrete_sequence=['green', 'gray', 'red'])

# Customizing layout
fig.update_layout(xaxis_title='Team', yaxis_title='Number of Matches', barmode='group')

# Show the chart
st.plotly_chart(fig)


#Visualization 2: Scatter plot 

st.header("Visualization 2: Premier League Team Performance (Bubble Chart)")

# Interactive feature 2 for Visualization 2: Radio button to select bubble size metric
bubble_size_radio = st.radio("Select Bubble Size Metric", ['xG', 'xGA', 'xG_diff_abs'])

# Interactive feature 3: Dropdown to select match type ("Home," "Away," or "Both")
match_type = st.selectbox("Select Match Type", ['Home', 'Away', 'Both'])

# Filter the data based on the selected match type
if match_type == 'Home':
    filtered_data = premier_league_data[premier_league_data['h_a'] == 'h']
elif match_type == 'Away':
    filtered_data = premier_league_data[premier_league_data['h_a'] == 'a']
else:
    filtered_data = premier_league_data

# Group the filtered data by 'teamId' and calculate the sum of relevant columns
team_performance = filtered_data.groupby('teamId').agg({
    'xG': 'sum',
    'xGA': 'sum',
}).reset_index()

# Calculate the difference between xG and xGA
team_performance['xG_diff'] = team_performance['xG'] - team_performance['xGA']

# Calculate the absolute difference between xG and xGA
team_performance['xG_diff_abs'] = team_performance['xG_diff'].abs()

# Define a function to determine bubble color based on xG and xGA comparison
def get_color(xG_diff):
    if xG_diff < 0:
        return 'red'
    elif xG_diff > 0:
        return 'green'
    else:
        return 'blue'

# Add a 'color' column based on the xG and xGA comparison
team_performance['color'] = team_performance['xG_diff'].apply(get_color)

# Interactive feature for switching X and Y axes
switch_axes = st.checkbox("Switch X and Y Axes")

# Define X and Y variables based on the switch_axes state
x_variable = 'xG' if not switch_axes else 'xGA'
y_variable = 'xGA' if not switch_axes else 'xG'

# Create the bubble chart with the selected X and Y variables
fig = px.scatter(team_performance, x=x_variable, y=y_variable, size=bubble_size_radio, color='color', hover_name='teamId',
                 title=f'Premier League Team Performance (Bubble Chart)',
                 labels={x_variable: f'Total Expected Goals ({x_variable})', y_variable: f'Total Expected Goals ({y_variable})'},
                 color_discrete_map={'red': 'red', 'green': 'green', 'blue': 'blue'})

# Customize the layout
fig.update_layout(xaxis_title=f'Total Expected Goals ({x_variable})', yaxis_title=f'Total Expected Goals ({y_variable})')

# Show the chart
st.plotly_chart(fig)
