import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_rounding_histogram(df, x_col='effect', title='Rounding Impact Distribution'):
    """Plots a histogram of rounding effects."""
    fig = px.histogram(
        df,
        x=x_col,
        nbins=20,
        title=title,
        labels={'effect': 'Rounding Impact ($)'},
        color_discrete_sequence=['#636EFA']
    )
    fig.update_layout(bargap=0.1)
    return fig

def plot_bias_line_chart(df, x_col, y_col, title, x_label, y_label):
    """Plots a line chart for bias trends."""
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels={x_col: x_label, y_col: y_label}
    )
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    return fig

def plot_heatmap(df, x_col, y_col, z_col, title):
    """Plots a heatmap of rounding impacts."""
    pivot_df = df.pivot(index=y_col, columns=x_col, values=z_col)
    fig = px.imshow(
        pivot_df,
        labels=dict(x=x_col, y=y_col, color="Avg Bias"),
        title=title,
        color_continuous_scale='RdBu_r', # Red for positive (retailer gain), Blue for negative (consumer gain)
        aspect="auto"
    )
    return fig

def plot_last_digit_distribution(df, digit_col='last_digit', title='Last Digit Distribution (Post-Tax)'):
    """Plots frequency of the last digit after tax."""
    counts = df[digit_col].value_counts().sort_index().reset_index()
    counts.columns = ['digit', 'frequency']
    fig = px.bar(
        counts,
        x='digit',
        y='frequency',
        title=title,
        labels={'digit': 'Last Digit', 'frequency': 'Frequency'}
    )
    fig.update_xaxes(tickvals=list(range(10)))
    return fig
