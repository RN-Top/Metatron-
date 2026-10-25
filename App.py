import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="3D Metatron's Cube")
st.title("Metatron's Cube — 3D Sacred Geometry Engine")

# Sidebar Controls
st.sidebar.header("Geometry Controls")
show_all_78 = st.sidebar.checkbox("Show All 78 Chords", value=True)
show_platonic = st.sidebar.checkbox("Highlight Dual Platonic Framework (Cube + Octahedron)", value=True)
sphere_size = st.sidebar.slider("Sphere Scale", 0.05, 0.3, 0.12)
rotation_speed = st.sidebar.slider("Line Width", 1, 6, 2)

# 1. Generate the 13 Sphere Centers of 3D Metatron's Cube (Cuboctahedron + Center)
# 1 center + 12 vertices of a cuboctahedron
c_center = np.array([[0.0, 0.0, 0.0]])

# 12 vertices defined by permutations of (±1, ±1, 0)
v = []
for s1 in [-1.0, 1.0]:
    for s2 in [-1.0, 1.0]:
        v.append([s1, s2, 0.0])
        v.append([s1, 0.0, s2])
        v.append([0.0, s1, s2])

vertices = np.array(v)
all_nodes = np.vstack([c_center, vertices])

# 2. Build 3D Spheres (Fruit of Life Nodes)
phi = np.linspace(0, np.pi, 15)
theta = np.linspace(0, 2 * np.pi, 15)
phi, theta = np.meshgrid(phi, theta)

sphere_traces = []
for idx, (x0, y0, z0) in enumerate(all_nodes):
    xs = x0 + sphere_size * np.sin(phi) * np.cos(theta)
    ys = y0 + sphere_size * np.sin(phi) * np.sin(theta)
    zs = z0 + sphere_size * np.cos(phi)
    
    color = "gold" if idx == 0 else "#00e5ff"
    sphere_traces.append(
        go.Surface(
            x=xs, y=ys, z=zs,
            colorscale=[[0, color], [1, color]],
            showscale=False,
            opacity=0.85,
            hoverinfo="skip"
        )
    )

# 3. Build All 78 Connecting Chords
edge_traces = []
if show_all_78:
    lx, ly, lz = [], [], []
    for i in range(len(all_nodes)):
        for j in range(i + 1, len(all_nodes)):
            p1 = all_nodes[i]
            p2 = all_nodes[j]
            lx.extend([p1[0], p2[0], None])
            ly.extend([p1[1], p2[1], None])
            lz.extend([p1[2], p2[2], None])

    edge_traces.append(
        go.Scatter3d(
            x=lx, y=ly, z=lz,
            mode="lines",
            line=dict(color="rgba(0, 229, 255, 0.35)", width=rotation_speed),
            hoverinfo="skip",
            name="78 Metatron Vectors"
        )
    )

# 4. Optional: Highlight the Hexahedron (Cube) Inner Framework
if show_platonic:
    # 8 corners of inscribed cube
    cube_nodes = []
    for cx in [-1.0, 1.0]:
        for cy in [-1.0, 1.0]:
            for cz in [-1.0, 1.0]:
                cube_nodes.append([cx, cy, cz])
    cube_nodes = np.array(cube_nodes) * 0.7
    
    cube_edges = [
        (0,1),(1,3),(3,2),(2,0),
        (4,5),(5,7),(7,6),(6,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
    cx, cy, cz = [], [], []
    for e in cube_edges:
        cx.extend([cube_nodes[e[0]][0], cube_nodes[e[1]][0], None])
        cy.extend([cube_nodes[e[0]][1], cube_nodes[e[1]][1], None])
        cz.extend([cube_nodes[e[0]][2], cube_nodes[e[1]][2], None])

    edge_traces.append(
        go.Scatter3d(
            x=cx, y=cy, z=cz,
            mode="lines",
            line=dict(color="#ff007f", width=rotation_speed + 2),
            name="Inscribed Hexahedron"
        )
    )

fig = go.Figure(data=sphere_traces + edge_traces)

fig.update_layout(
    scene=dict(
        bgcolor="#0a0a0f",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        camera=dict(
            eye=dict(x=1.8, y=1.8, z=1.4)
        )
    ),
    paper_bgcolor="#0a0a0f",
    margin=dict(l=0, r=0, t=10, b=10),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
