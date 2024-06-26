import math

def quantize():
    pass

def get_radius(f: float, ior: float):
    R_1 = 1 / ((1/f) / (ior-1))
    return R_1

def get_fov(f: float, D: float):
    return 2 * math.atan(D / (2 * f))

def rad_to_deg(rad: float):
    return str(round(rad * (180 / math.pi), 2)) + "°"

import numpy as np
import matplotlib.pyplot as plt

def circle_angle_from_x(x: float, radius: float):
    hypo = radius / radius
    adj = x / radius
    return math.acos(adj / hypo)

def render_lens_2d(radius: float, diameter: float, rings: int):
    if diameter > radius * 2:
        raise ValueError("Diameter cannot be greater than twice the radius")
    
    # Find the points
    points = []
    for i in range(rings):
        x = diameter * (i / (rings - 1) - 0.5)
        y = math.sin(circle_angle_from_x(x, radius)) * radius
        points.append((x, y))

    # Shift the points to the center
    max_angle = circle_angle_from_x(diameter / 2, radius)
    min_y = math.sin(max_angle) * radius
    for i in range(len(points)):
        points[i] = (points[i][0], points[i][1] - min_y)
    
    # Render curve
    for line in zip(points[:-1], points[1:]):
        start, end = line
        x0, y0 = start
        x1, y1 = end
        plt.plot([x0, x1], [y0, y1], color='black')
    # Render flat side
    plt.plot([-diameter/2, diameter/2], [0, 0], color='black')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

import scipy as sp
from scipy.spatial.transform import Rotation

def render_lens_3d(radius: float, diameter: float, segments: int, rings: int):
    convex = radius > 0
    radius = abs(radius)
    if diameter > radius * 2:
        raise ValueError("Diameter cannot be greater than twice the radius")

    verticies, faces = render_lens_arcs(radius, diameter, segments, rings)

    # Adjust to origin
    min_angle = circle_angle_from_x(diameter / 2, radius)
    min_y = math.sin(min_angle) * radius
    for v in range(len(verticies)):
        verticies[v][2] -= min_y

    if convex:
        # Add backside (for Convex)
        faces.append(([s * rings for s in range(segments)] + [s * rings + (rings - 1) for s in range(segments)])[::-1])
    else:
        # Flip all normals
        faces = [f[::-1] for f in faces]

        # Add frontside
        front_verticies_index = len(verticies)
        max_y = radius - min_y
        for s in range(segments * 2):
            angle = math.pi * (s / segments) - (math.pi / 2)
            verticies.append([math.cos(angle) * (diameter / 2), math.sin(angle) * (diameter / 2), max_y])
        faces.append(list(range(front_verticies_index, len(verticies))))
        # faces.append([front_verticies_index, 0 * rings, 1 * rings, front_verticies_index + 1])
        double_segments = segments * 2
        for s in range(double_segments):
            next_s = (s + 1) % double_segments
            a = front_verticies_index + s
            b = ((s) % segments) * rings
            c = ((s + 1) % segments) * rings
            if s == double_segments - 1:
                b += rings - 1
                c = 0
            else:
                if s >= segments:
                    b += rings - 1
                if s + 1 >= segments:
                    c += rings - 1
            d = front_verticies_index + next_s

            faces.append([a, b, c, d])

            # s0 * rings + 0,
            # s0 * rings + 0,
            # s1 * rings + (rings - 0 - 1),
            # s1 * rings + (rings - 0 - 1)



    return to_obj(verticies, faces)

def render_lens_arcs(radius: float, diameter: float, segments: int, rings: int):
    # Find the points in one arc
    arc = []
    for i in range(rings):
        x = diameter * (i / (rings - 1) - 0.5)
        y = math.sin(circle_angle_from_x(x, radius)) * radius
        arc.append([0, x, y])
    
    # Concat all 3d points
    points = []
    for i in range(segments):
        r = Rotation.from_euler('xyz', [0, 0, i * (180 / segments)], degrees=True)
        arc_rotated = r.apply(np.array(arc))
        points.append(arc_rotated)
    points = np.concatenate(points)

    faces = []
    for s in range(segments):
        for r in range(rings - 1):
            s0 = s
            s1 = (s + 1) % segments
            r0 = r
            r1 = r + 1
            if s == segments - 1:
                faces.append([
                    s0 * rings + r0,
                    s0 * rings + r1,
                    s1 * rings + (rings - r1 - 1),
                    s1 * rings + (rings - r0 - 1)
                ])
            else:
                faces.append([
                    s0 * rings + r0,
                    s0 * rings + r1,
                    s1 * rings + r1,
                    s1 * rings + r0
                ])
            # After half of the rings, you're on the other side, which accidentally flips the normals; so correct for that:
            if r < rings // 2:
                faces[-1] = faces[-1][::-1]
    
    return points.tolist(), faces

def to_obj(verticies, faces):
    txt = ""
    for vertex in verticies:
        txt += f"v {vertex[0]} {vertex[1]} {vertex[2]}\n"
    for face in faces:
        face = [str(i + 1) for i in face]
        txt += f"f " + " ".join(face) + "\n"
    return txt

def main():
    focal_length = 3 # cm
    material_ior = 300 / 200 # Air vs Glass (optical)
    material_ior = 150 / 300 # Air vs Glass (optical)
    # material_ior = 1500 / 2230 # Water vs ABS (acoustic)
    diameter = 1.5 # cm
    radius = get_radius(focal_length, material_ior)
    fov = get_fov(focal_length, diameter)
    print("R1:", radius)
    print("FoV:", rad_to_deg(fov))
    pixels = render_lens_3d(radius, diameter, 20, 100)
    with open("lens.obj", "w") as file:
        file.write(pixels)
    # plt.imshow(pixels, cmap='gray')
    # plt.show()

if __name__ == "__main__":
    main()
