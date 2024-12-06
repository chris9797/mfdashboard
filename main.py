import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Mutual Fund Dashboard",
                   page_icon=":bar_chart:",
                   layout="centered")

df = pd.read_excel('quad_data.xlsx')

st.sidebar.header("Filter:")

df = df[df['P_Oct-24'] != 0].copy()

df = df[df['P_Nov-23'] != 0].copy()

df.reset_index(drop=True, inplace=True)

df['price_change'] = round(((df['P_Oct-24'] - df['P_Nov-23'])/df['P_Nov-23']) * 100)

df['qty_change'] = round(((df['S_Oct-24'] - df['S_Nov-23'])/df['S_Nov-23']) * 100)

stocks = st.sidebar.multiselect(
    "Select the stocks:",
    options=df['Stocks'].unique(),
    default=df['Stocks'].unique()[0:5]
)

sectors = st.sidebar.multiselect(
    "Select the sectors:",
    options=df['Sector'].unique(),
    default=['Bank']
)

indices = st.sidebar.multiselect(
    "Select the indices:",
    options=df['Indices'].unique(),
    default=['Nifty', 'NiftyJr']
)

st.title(":bar_chart: Mutual Fund Dashboard")
st.markdown('##')

st.text("Selection:")

df_selection = df.query(
    "Stocks == @stocks or (Sector == @sectors and Indices == @indices)"
)

st.dataframe(df_selection)

scatter_pl = px.scatter(
    df_selection,
    x='qty_change',
    y='price_change',
    title='Price vs Quantity Change %',
    text='Stocks'
)

# Define the midpoints for the quadrants
x_mid = 0
y_mid = 0

# Add quadrant lines

mx = max(abs(df_selection.qty_change.min()), abs(df_selection.qty_change.max()))
my = max(abs(df_selection.price_change.min()), abs(df_selection.price_change.max()))

scatter_pl.update_layout(
    xaxis=dict(title='Quantity Change %', range=[-mx, mx], zeroline=True, zerolinecolor='white'),
    yaxis=dict(title='Price Change %', range=[-my, my], zeroline=True, zerolinecolor='white'),
    shapes=[
        # Vertical line
        dict(type='line', x0=0, y0=-my*2, x1=0, y1=my*2, line=dict(color='black', width=1, dash='dot')),
        # Horizontal line
        dict(type='line', x0=-mx*2, y0=0, x1=mx*2, y1=0, line=dict(color='black', width=1, dash='dot'))
    ],
    width=700,
    height=500
)

scatter_pl.update_traces(
    textposition='middle right',  # Position text to the right of the points
    textfont=dict(size=10, color='black'),
    marker=dict(color='rgb(277,95,19)',size=12)
)

scatter_pl['layout']['yaxis'].update(autorange = True)
scatter_pl['layout']['xaxis'].update(autorange = True)

st.plotly_chart(scatter_pl)
