import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st  # Since streamlit is used for st.error()

# Function for Scatter Plot
def scatter_plot(df, x_axis, y_axis):
    fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis, color_continuous_scale='Viridis',
                     title=f"Scatter Plot: {x_axis} vs {y_axis}")
    return fig

# Function for Bar Plot
def bar_plot(df, x_axis, y_axis):
    fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, color_continuous_scale='Viridis',
                 title=f"Bar Plot: {x_axis} vs {y_axis}")
    return fig

# Function for Box Plot
def box_plot(df, x_axis, y_axis):
    fig = px.box(df, x=x_axis, y=y_axis, color=x_axis, color_discrete_sequence=px.colors.sequential.Viridis,
                 title=f"Box Plot: {x_axis} vs {y_axis}")
    return fig

# Function for Histogram
def histogram_plot(df, x_axis):
    fig = px.histogram(df, x=x_axis, color=x_axis, color_discrete_sequence=px.colors.sequential.Viridis,
                       title=f"Histogram of {x_axis}")
    return fig

# Function for Pie Chart
def pie_chart(df, x_axis, y_axis):
    fig = px.pie(df, names=x_axis, values=y_axis, color=x_axis, color_discrete_sequence=px.colors.sequential.Viridis,
                 title=f"Pie Chart: {x_axis} vs {y_axis}")
    return fig

# Function for Sunburst Plot
def sunburst_plot(df, x_axis, y_axis):
    fig = px.sunburst(df, path=[x_axis, y_axis], color=x_axis, color_continuous_scale='Viridis',
                      title=f"Sunburst Plot: {x_axis} and {y_axis}")
    return fig
