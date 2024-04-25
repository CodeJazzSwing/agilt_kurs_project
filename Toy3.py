import pandas as pd
import streamlit as st
import plotly.express as px


df = pd.read_csv(r'YOUR_PATH_FILE_HERE', sep=';')



image = 'StockholmsStad_logotypeStandardA3_300ppi_svart.png'

df['Tidpunkt_'] = pd.to_datetime(df['Tidpunkt_'], format='%Y%m%d')

#---------SIDEBAR-------------

st.sidebar.header('Filter Here:')

# Date range filter
start_date = st.sidebar.date_input('Startdatum', df['Tidpunkt_'].min().date())
end_date = st.sidebar.date_input('Slutdatum', df['Tidpunkt_'].max().date())

if start_date > end_date:
    st.sidebar.error('Misstag: Slutdatum måste vara efter startdatum.')


# Filter the DF based on the sidebar selection
df_selection = df[(df['Tidpunkt_'].dt.date >= start_date) & (df['Tidpunkt_'].dt.date <= end_date)]


#---------LAYOUT-------------

# Create a new layout with 2 columns
col1, col2 = st.columns(2)

# Display the image in the left column
col1.image(image, use_column_width=True)

#---------CATEGORIES-------------

#Create color dictionary för column "Swecos_kategorisering_" categories
color_dict = {"Brand i byggnad" : "red", "Brand i container" : "blue", "Fordonsbrand" : "green", "Mark-/skogsbrand" : "orange", "Övrigt" : "purple"}
categories = df_selection['Swecos_kategorisering_'].unique()
colors = [color_dict[cat] for cat in categories]


#---------INTERACTIVE PLOT ON MAP-------------

fig = px.scatter_mapbox(df_selection,
                        lon = df_selection['lng'],
                        lat = df_selection['lat'],
                        zoom = 10,
                        width = 1000,
                        height= 1000,
                        title = 'Bränder i Stockholm stad',
                        text = df_selection['Swecos_kategorisering_'],
                        hover_data = {'Swecos_kategorisering_': True, 'lng': False, 'lat': False},
                        color = df_selection["Swecos_kategorisering_"],
                        color_discrete_sequence = colors
                        )


#---------UPDATE/EDIT MAP-------------

fig.update_traces(marker=dict(size = 12))
fig.update_layout(mapbox_style='open-street-map')
fig.update_layout(margin={'r':0,'t':50,'l':0,'b':10})


# Display  plot in Streamlit
st.plotly_chart(fig)