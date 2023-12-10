import streamlit as st
import json
from streamlit_js_eval import get_geolocation
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


############################# READ JSON FILE -> DATAFRAME #############################
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

############################# INITIAL CONFIG #############################
if 'center_location' not in st.session_state:
    st.session_state['center_location'] = (35.67044, 139.7631)


# Front-end layout
restaurant_list, restaurant_map = st.columns([1,3])

with restaurant_list:
    ############################# GET LOCATION ###########################
    if st.button('location 1'):
        st.session_state.center_location = (35.67559, 139.6699)
        st.rerun()
    if st.button('location 12'):
        st.session_state.center_location = (35.7796, 139.7899)
        st.rerun()
    if st.button('location 123'):
        st.session_state.center_location = (35.65737, 139.3337)
        st.rerun()


with restaurant_map:
    ############################# SHOW MAP ###########################
    df = pd.DataFrame({'longitude':longtitude_all,'latitude':latitude_all,'name':name_all})
    fig = px.scatter_mapbox(df, 
                            lat="latitude", 
                            lon="longitude", 
                            hover_name='name', 
                            height=500, 
                            width=500, 
                            color_discrete_sequence=["fuchsia"],
                            )

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken='pk.eyJ1IjoicGVuZ3VpbnB1ZyIsImEiOiJjbHB1dGYyNmowb2xrMm5uNGNsaTI2NDliIn0.XkvqczYdViZXnl0iBZek4A',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=st.session_state.center_location[0],
                lon=st.session_state.center_location[1]
            ),
            pitch=0,
            zoom=15
        )
    )

    st.plotly_chart(fig)
















############################# GET LOCATION #############################
# if st.checkbox("Check my location"):
#     loc = get_geolocation()
#     st.write(loc['coords']['latitude'])
#     st.write(loc['coords']['longitude'])