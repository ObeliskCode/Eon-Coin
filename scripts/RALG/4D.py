import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def generate_toroidal_4D_points(num_points, radius=5, tube_radius=1):
    """Generate points on a toroidal surface in 4D."""
    points = []
    for _ in range(num_points):
        u = np.random.rand() * 2 * np.pi  # Angle around the toroidal hole
        v = np.random.rand() * 2 * np.pi  # Angle around the tube

        x = (radius + tube_radius * np.cos(v)) * np.cos(u)
        y = (radius + tube_radius * np.cos(v)) * np.sin(u)
        z = tube_radius * np.sin(v)
        w = np.random.rand() * 10  # Randomly spread in the fourth dimension

        points.append([x, y, z, w])
    return np.array(points)

def rotate_4D(points, angles):
    theta, phi, psi = angles

    # Create rotation matrices
    R_xy = np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta), np.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    R_xz = np.array([
        [np.cos(phi), 0, -np.sin(phi), 0],
        [0, 1, 0, 0],
        [np.sin(phi), 0, np.cos(phi), 0],
        [0, 0, 0, 1]
    ])

    R_xw = np.array([
        [np.cos(psi), 0, 0, -np.sin(psi)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [np.sin(psi), 0, 0, np.cos(psi)]
    ])

    # Combine rotations
    R = R_xy @ R_xz @ R_xw
    rotated_points = np.dot(points, R.T)
    return rotated_points

def project_to_3D(points_4D):
    # Use only the first three dimensions for projection
    return points_4D[:, :3]  

def draw_points(points):
    glBegin(GL_POINTS)
    for point in points:
        glVertex3fv(point)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -30)

    num_points = 1000
    points_4D = generate_toroidal_4D_points(num_points)
    angles = (np.pi / 4, np.pi / 4, np.pi / 4)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glRotatef(1, 0, 1, 0)  # Rotate the scene

        rotated_points = rotate_4D(points_4D, angles)
        projected_points = project_to_3D(rotated_points)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_points(projected_points)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
