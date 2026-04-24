import numpy as np
import os
import time
import sys

def get_terminal_size():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines - 2
    except:
        return 80, 40

def rotate_coords(coords, ax, ay, az):
    # Convertir a radianes y rotar
    rad = np.radians([ax, ay, az])
    cx, cy, cz = np.cos(rad)
    sx, sy, sz = np.sin(rad)
    
    # Matriz de rotación combinada (XYZ)
    R = np.array([
        [cy*cz, -cy*sz, sy],
        [sx*sy*cz + cx*sz, -sx*sy*sz + cx*cz, -sx*cy],
        [-cx*sy*cz + sx*sz, cx*sy*sz + sx*cz, cx*cy]
    ])
    return coords @ R.T

def animate_structure(pdb_lines, steps=150, chain_filter=None):
    ca_coords = []
    for line in pdb_lines:
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            chain_id = line[21].strip()
            if chain_filter and chain_id != chain_filter:
                continue
            ca_coords.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    
    if not ca_coords:
        return f"❌ No CA atoms found for chain: {chain_filter}"

    coords = np.array(ca_coords)
    coords -= np.mean(coords, axis=0) # Centrado riguroso

    width, height = get_terminal_size()
    # El ratio de aspecto 2.2 es ideal para que los puntos no se vean estirados
    aspect_ratio = 2.2 
    # Escala máxima para llenar la terminal
    scale = min(width, height * aspect_ratio) / (np.ptp(coords) * 1.05)

    try:
        for i in range(steps):
            # Rotación suave para apreciar la topología
            rotated = rotate_coords(coords, i * 2, i * 4, i * 1)
            
            # Canvas de alta densidad
            canvas = [[" " for _ in range(width)] for _ in range(height)]
            
            for x, y, z in rotated:
                ix = int(x * scale + width / 2)
                iy = int(y * scale / aspect_ratio + height / 2)
                
                if 0 <= ix < width and 0 <= iy < height:
                    # Usamos solo puntos. 
                    # El insight viene del movimiento, no del caracter.
                    canvas[iy][ix] = "."

            # Renderizado ultra-rápido
            output = "\n".join(["".join(row) for row in canvas])
            sys.stdout.write("\033[H" + output)
            sys.stdout.flush()
            time.sleep(0.03) # ~30 FPS para suavidad máxima
            
    except KeyboardInterrupt:
        pass
    return "\n"