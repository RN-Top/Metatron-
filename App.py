import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Metatron's Cube 3D")
st.title("Metatron's Cube — 3D Sacred Geometry Engine")

# Three.js 3D Metatron's Cube Engine (No external pip packages needed)
threejs_metatron_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #080810; font-family: sans-serif; }
        #canvas-container { width: 100vw; height: 100vh; }
        #legend {
            position: absolute;
            top: 15px;
            left: 15px;
            color: #00ffff;
            background: rgba(0, 0, 0, 0.6);
            padding: 10px 14px;
            border-radius: 6px;
            font-size: 13px;
            pointer-events: none;
            border: 1px solid rgba(0, 255, 255, 0.3);
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="legend">
        <b>3D Metatron's Cube</b><br>
        • 13 Fruit of Life Nodes<br>
        • 78 Interconnecting Vectors<br>
        • Platonic Hexahedron Dual
    </div>
    <div id="canvas-container"></div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 0, 4.5);

        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Group container for complete rotation
        const metatronGroup = new THREE.Group();
        scene.add(metatronGroup);

        // 1. Generate the 13 Sphere Centers (Cuboctahedron / Fruit of Life in 3D)
        const nodes = [new THREE.Vector3(0, 0, 0)];
        const scale = 1.3;

        // 12 outer vertices of a cuboctahedron (normalized permutations of [±1, ±1, 0])
        const perm = [-1, 1];
        for (let s1 of perm) {
            for (let s2 of perm) {
                nodes.push(new THREE.Vector3(s1 * scale, s2 * scale, 0));
                nodes.push(new THREE.Vector3(s1 * scale, 0, s2 * scale));
                nodes.push(new THREE.Vector3(0, s1 * scale, s2 * scale));
            }
        }

        // 2. Add Spheres
        const sphereGeo = new THREE.SphereGeometry(0.12, 24, 24);
        const centerMat = new THREE.MeshBasicMaterial({ color: 0xffd700, wireframe: false });
        const nodeMat = new THREE.MeshBasicMaterial({ color: 0x00e5ff, wireframe: false });

        nodes.forEach((pos, idx) => {
            const mesh = new THREE.Mesh(sphereGeo, idx === 0 ? centerMat : nodeMat);
            mesh.position.copy(pos);
            metatronGroup.add(mesh);
        });

        // 3. Connect All 78 Lines (Every node to every node)
        const lineMat = new THREE.LineBasicMaterial({
            color: 0x0088ff,
            transparent: true,
            opacity: 0.35
        });

        const lineGeo = new THREE.BufferGeometry();
        const positions = [];

        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                positions.push(nodes[i].x, nodes[i].y, nodes[i].z);
                positions.push(nodes[j].x, nodes[j].y, nodes[j].z);
            }
        }
        lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        const allLines = new THREE.LineSegments(lineGeo, lineMat);
        metatronGroup.add(allLines);

        // 4. Inscribed Platonic Hexahedron (Cube)
        const cubeMat = new THREE.LineBasicMaterial({
            color: 0xff007f,
            linewidth: 2,
            transparent: true,
            opacity: 0.85
        });

        const cubeGeo = new THREE.BoxGeometry(scale * 1.05, scale * 1.05, scale * 1.05);
        const cubeEdges = new THREE.EdgesGeometry(cubeGeo);
        const cubeLines = new THREE.LineSegments(cubeEdges, cubeMat);
        metatronGroup.add(cubeLines);

        // 5. Inscribed Octahedron
        const octGeo = new THREE.OctahedronGeometry(scale * 1.35);
        const octEdges = new THREE.EdgesGeometry(octGeo);
        const octMat = new THREE.LineBasicMaterial({
            color: 0x00ff88,
            transparent: true,
            opacity: 0.75
        });
        const octLines = new THREE.LineSegments(octEdges, octMat);
        metatronGroup.add(octLines);

        // Animation Loop
        function animate() {
            requestAnimationFrame(animate);
            metatronGroup.rotation.x += 0.003;
            metatronGroup.rotation.y += 0.005;
            controls.update();
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

components.html(threejs_metatron_code, height=720, scrolling=False)
