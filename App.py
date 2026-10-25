import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide", page_title="Metatron's Cube 3D")
st.title("Live 3D Metatron's Cube")

# 1. 13 Spheres (Centers) of Metatron's Cube
coords = [[0.0, 0.0, 0.0]]
# Inner ring (6 points)
for i in range(6):
    a = i * np.pi / 3
    coords.append([float(np.cos(a)), float(np.sin(a)), 0.0])
# Outer ring (6 points)
r_out = np.sqrt(3)
for i in range(6):
    a = i * np.pi / 3 + np.pi / 6
    coords.append([float(r_out * np.cos(a)), float(r_out * np.sin(a)), 0.0])

pts = np.array(coords)

# 2. Build full interconnection lines
line_data = []
for i in range(len(pts)):
    for j in range(i + 1, len(pts)):
        line_data.append({
            "start": [pts[i][0], pts[i][1], pts[i][2]],
            "end": [pts[j][0], pts[j][1], pts[j][2]],
            "color": [0, 255, 255, 180]
        })

nodes_df = pd.DataFrame({
    "x": pts[:, 0],
    "y": pts[:, 1],
    "z": pts[:, 2],
    "radius": [0.12] * len(pts)
})

# 3. Render 3D layers
node_layer = pdk.Layer(
    "ScatterplotLayer",
    data=nodes_df,
    get_position="[x, y, z]",
    get_radius="radius * 1000",
    get_fill_color=[255, 64, 129, 230],
    pickable=True
)

line_layer = pdk.Layer(
    "LineLayer",
    data=pd.DataFrame(line_data),
    get_source_position="start",
    get_target_position="end",
    get_color="color",
    get_width=3
)

view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=14,
    pitch=45,
    bearing=30
)

st.pydeck_chart(pdk.Deck(
    layers=[line_layer, node_layer],
    initial_view_state=view_state,
    views=[pdk.View(type="OrbitView", controller=True)]
))
