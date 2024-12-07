import pandas as pd
import plotly.express as px
import streamlit as st
import io
import matplotlib.pyplot as plt
from adjustText import adjust_text


st.set_page_config(page_title="Mutual Fund Dashboard",
                   page_icon=":bar_chart:",
                   layout="centered")

df = pd.read_excel('quad_data-2.xlsx')

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

fig, ax = plt.subplots(figsize=(8, 8))

x = [z for z in df_selection['qty_change']]
y = [z for z in df_selection['price_change']]
labels = [z for z in df_selection['Symbol']]

# Scatter plot
ax.scatter(x, y, color='#ff5f13', label='Data Points', s=100)

# Add labels

texts = [ax.text(x[i], y[i], f' {label}', fontsize=10) for i, label in enumerate(labels)]


adjust_text(texts, arrowprops=dict(arrowstyle="->", color='#ff5f13'))
# Add dotted quadrant lines
ax.axhline(11.4, color='black', linestyle='--', linewidth=1)
ax.axvline(0, color='black', linestyle='--', linewidth=1)

# Customize axes and title
ax.set_xlabel('Quantity Change %')
ax.set_ylabel('Price Change %')
ax.set_title('Price vs Quantity Change %')

# Save the plot with specific DPI
plt.savefig("scatter_plot.png")  # High-resolution output

st.pyplot(fig)
