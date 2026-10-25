import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Live 3D Metatron's Cube")

# 1. Define the 13 centers of the Fruit of Life
centers = [(0, 0, 0)]
for i in range(6):
    angle = i * np.pi / 3
    centers.append((np.cos(angle), np.sin(angle), 0))
outer_r = np.sqrt(3)
for i in range(6):
    angle = i * np.pi / 3 + np.pi / 6
    centers.append((outer_r * np.cos(angle), outer_r * np.sin(angle), 0))

def get_sphere(center, radius=0.1, resolution=20):
    phi = np.linspace(0, 2*np.pi, resolution)
    theta = np.linspace(0, np.pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    x = center[0] + radius * np.sin(theta) * np.cos(phi)
    y = center[1] + radius * np.sin(theta) * np.sin(phi)
    z = center[2] + radius * np.cos(theta)
    return x, y, z

traces = []
for center in centers:
    x, y, z = get_sphere(center)
    traces.append(go.Surface(x=x, y=y, z=z, colorscale="Viridis", showscale=False))

points = np.array(centers)
lines = []
for i in range(len(points)):
    for j in range(i+1, len(points)):
        p1 = points[i]
        p2 = points[j]
        dist = np.linalg.norm(p1 - p2)
        if np.isclose(dist, 1.0) or np.isclose(dist, outer_r):
            lines.append(go.Scatter3d(x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
                                      mode='lines', line=dict(color='cyan', width=4)))

fig = go.Figure(data=traces + lines)
fig.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)),
                  showlegend=False, margin=dict(l=0, r=0, t=0, b=0))

st.plotly_chart(fig, use_container_width=True)
