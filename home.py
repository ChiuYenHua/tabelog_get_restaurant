import streamlit as st
import json
from streamlit_js_eval import get_geolocation
import pandas as pd
import plotly.express as px
from map import build_map
from streamlit_folium import st_folium


# if st.checkbox("Check my location"):
#     loc = get_geolocation()
#     st.write(loc['coords']['latitude'])
#     st.write(loc['coords']['longitude'])

# Read json file
with open('tabelog_#tokyo_restaurants_score_above_3.5.json', 'r') as f:
    tabelog_info = json.load(f)

# Initial info list
longtitude_all = []
latitude_all = []
name_all = []

for key, value in tabelog_info.items():
    if 'chinese' not in key:
        for every_restaurant in value:                                  
            longtitude_all.append(float(every_restaurant['data-lng'][1:-1]))
            latitude_all.append(float(every_restaurant['data-lat'][1:-1]))
            name_all.append(every_restaurant['data-name-ja'][1:-1])


# map = build_map()


# # Rrender Folium map in Streamlit
# st_data = st_folium(map.map, width=725)















########################################### 1
df = pd.DataFrame({'longitude':longtitude_all,'latitude':latitude_all,'name':name_all})
fig = px.scatter_mapbox(df, 
                        lat="latitude", 
                        lon="longitude", 
                        hover_name='name', 
                        zoom=8, 
                        height=1000, 
                        width=1000, 
                        color_discrete_sequence=["fuchsia"],
                        )

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html('test.html')
st.plotly_chart(fig)


########################################### 2
# import plotly.graph_objects as go

# fig = go.Figure(go.Scattermapbox(
#         lat=['45.5017'],
#         lon=['-73.5673'],
#         mode='markers',
#         marker=go.scattermapbox.Marker(
#             size=14
#         ),
#         text=['Montreal'],
#     ))

# fig.update_layout(
#     hovermode='closest',
#     mapbox=dict(
#         accesstoken=mapbox_access_token,
#         bearing=0,
#         center=go.layout.mapbox.Center(
#             lat=45,
#             lon=-73
#         ),
#         pitch=0,
#         zoom=5
#     )
# )

# st.plotly_chart(fig)