import streamlit as st
import pdk
import datetime
import time

# Variable for date picker, default to Jan 1st 2020
date = datetime.date(2020,1,1)
# Set viewport for the deckgl map
view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)
# Create the scatter plot layer
covidLayer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        pickable=False,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position=["Longitude", "Latitude"],
        get_radius=metric_to_show_in_covid_Layer,
        get_fill_color=[252, 136, 3],
        get_line_color=[255,0,0],
        tooltip="test test",
    )

# Create the deck.gl map
r = pdk.Deck(
    layers=[covidLayer],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/light-v10",
)
# Create a subheading to display current date
subheading = st.subheader("")
# Render the deck.gl map in the Streamlit app as a Pydeck chart 
map = st.pydeck_chart(r)
# Update the maps and the subheading each day for 90 days
for i in range(0, 120, 1):
    # Increment day by 1
    date += datetime.timedelta(days=1)
    # Update data in map layers
    covidLayer.data = df[df['date'] == date.isoformat()]
    # Update the deck.gl map
    r.update()
    # Render the map
    map.pydeck_chart(r)
    # Update the heading with current date
    subheading.subheader("%s on : %s" % (metric_to_show_in_covid_Layer, date.strftime("%B %d, %Y")))
    
# wait 0.1 second before go onto next day
    time.sleep(0.05)