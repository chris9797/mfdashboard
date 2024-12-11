import pandas as pd
import plotly.express as px
import streamlit as st
import io
import matplotlib.pyplot as plt
from adjustText import adjust_text
import matplotlib
from matplotlib import rcParams
import matplotlib.font_manager as fm
import random


colors = ["#D0CEBB", "#023D6D", "#4D1413", "#F4A980"]
fm.fontManager.addfont("Mulish-Bold.ttf")

matplotlib.rcParams.update(matplotlib.rcParamsDefault)
matplotlib.rcParams['font.weight'] = 'bold'


rcParams['font.family'] = 'Mulish'  # Example: 'serif', 'sans-serif', 'monospace'
rcParams['font.size'] = 12

st.set_page_config(page_title="Mutual Fund Dashboard",
                   page_icon=":bar_chart:",
                   layout="centered")

df = pd.read_excel('quad_data-2.xlsx')

st.sidebar.header("Filter:")

#df = df[df['P_Nov-24'] != 0].copy()

#df = df[df['P_Nov-23'] != 0].copy()

df.reset_index(drop=True, inplace=True)

#df['price_change'] = round(((df['P_Nov-24'] - df['P_Nov-23'])/df['P_Nov-23']) * 100)

#df['qty_change'] = round(((df['S_Nov-24'] - df['S_Nov-23'])/df['S_Nov-23']) * 100)

df_sec = pd.read_excel("Sectors.xlsx")

stocks = st.sidebar.multiselect(
    "Select the stocks:",
    options=df['Stocks'].unique(),
    default=[]
)

sectors = st.sidebar.multiselect(
    "Select the sectors:",
    options=df_sec['Sectors'].unique(),
    default=df_sec['Sectors'].unique()
)

indices = st.sidebar.multiselect(
    "Select the indices:",
    options=df['Indices'].unique(),
    default=['Nifty', 'NiftyJr', 'Nifty Midcap 150', 'Nifty Small Cap 250']
)

st.title(":bar_chart: Mutual Fund Dashboard")
st.markdown('##')

st.text("Selection:")

df_selection = df.query(
    "Stocks == @stocks or (Sector == @sectors and Indices == @indices)"
)

st.dataframe(df_selection)

df_sec['%p_chg'] = [round(((-v['Dec-23'] + v['Nov-24']) / v['Dec-23']) * 100, 2) for i, v in df_sec.iterrows()]

df_plot = df_selection.groupby(['Sector']).sum()
df_plot['%aum_chg'] = [round(((-v['V_Nov-23'] + v['V_Nov-24']) / v['V_Nov-23']) * 100, 2) if v['V_Nov-23'] != 0 else 0 for i, v in df_plot.iterrows()]

df_plot.reset_index(inplace=True)
aum = []
for sec in df_plot['Sector']:
  aum.append(df_sec[df_sec['Sectors'] == sec]['%p_chg'].iloc[0])
df_plot['%p_chg'] = aum
st.dataframe(df_plot[['Sector', '%aum_chg', '%p_chg']])

x = [z for z in df_plot['%aum_chg']]
y = [z for z in df_plot['%p_chg']]

fig, ax = plt.subplots(figsize=(8, 8))
csfont = {'fontname':'Comic Sans MS'}
hfont = {'fontname':'Helvetica'}

# x = [z for z in df_selection['qty_change']]
# y = [z for z in df_selection['price_change']]

point_colors = []
col = 0
for _ in x:
  try:
    point_colors.append(colors[col])
  except:
    col = 0
    point_colors.append(colors[col])
  col += 1
labels = ['Technology' if z == 'IT' else z for z in df_plot['Sector']]

st.text(f"Selection:")
st.text(f"Sectors: {", ".join(sectors)}")
st.text(f"Indices: {", ".join(indices)}")
# Scatter plot
ax.scatter(x, y, color=point_colors, label='Data Points', s=100)

# Add labels

texts = [ax.text(x[i]+0.5, y[i]+0.5, f' {label}', fontsize=10, ha='right', va='bottom', fontweight='bold') for i, label in enumerate(labels)]

# Add dotted quadrant lines

nif = 0
nif100 = 0
nifmid = 0

for indice in indices:
  if indice == "Nifty":
    nif = 1
  if indice == "NiftyJr":
    nif100 = 1
  if indice == "Nifty Midcap 150":
    nifmid = 1

if nif == 1 and nif100 == 0:
  ax.axhline(11, color='#ff5f13', linestyle='--', linewidth=1)
  ax.text(ax.get_xlim()[1] + 1.5, 10.6, f'Nifty')

if nif100 == 1:
  ax.axhline(14.3, color='#ff5f13', linestyle='--', linewidth=1)
  ax.text(ax.get_xlim()[1] + 1.5, 13.9, f'Nifty 100', fontweight='bold')

#if nifmid == 1:
  #ax.axhline(22.4, color='#ff5f13', linestyle='--', linewidth=1)
  #ax.text(ax.get_xlim()[1] + 1.5, 22.0, f'Nifty Midcap 150')

ax.axvline(0, color='black', linestyle='--', linewidth=1)
ax.axhline(0, color='black', linestyle='--', linewidth=1)

# Customize axes and title
ax.set_xlabel('AUM Change %', fontweight='bold')
ax.set_ylabel('Price Change %', fontweight='bold')
ax.set_title('Price vs AUM Change %', fontweight='bold')
# adjust_text(texts, arrowprops=dict(arrowstyle="->", color='black'))
# Save the plot with specific DPI
#plt.savefig("scatter_plot.png")  # High-resolution output

st.pyplot(fig)
