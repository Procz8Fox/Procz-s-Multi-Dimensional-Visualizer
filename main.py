import sys
import subprocess

def ensure_dependencies():
    try:
        import pygame
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        import pygame

ensure_dependencies()

import pygame
import math

WIDTH, HEIGHT = 1024, 768
MAX_DIMENSION = 10
ANIMATION_SPEED = 0.5
SCALE = 100
FPS = 60

COLOR_BG = (10, 10, 12)
COLOR_NODE = (255, 255, 255)
COLOR_EDGE = (0, 200, 255)
COLOR_TEXT = (255, 255, 255)

def get_basis_vectors(n_dims, scale):
    vectors = []
    golden_angle = math.pi * (3 - math.sqrt(5))

    for i in range(n_dims):
        angle = i * golden_angle
        dampening = 0.85 ** i
        length = scale * dampening * 1.5
        vectors.append((
            math.cos(angle) * length,
            math.sin(angle) * length
        ))

    return vectors

def project_vertex(value, basis_vectors, current_dim):
    x = y = 0

    for i in range(len(basis_vectors)):
        strength = max(0.0, min(1.0, current_dim - i))
        if strength == 0:
            continue

        bx, by = basis_vectors[i]
        coefficient = 0.5 if (value >> i) & 1 else -0.5

        x += bx * coefficient * strength
        y += by * coefficient * strength

    return x, y

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Multi-Dimensional Visualizer (1D - 10D)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    basis_vectors = get_basis_vectors(MAX_DIMENSION, SCALE)

    current_dim_val = 0.0
    direction = 1
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    direction = 0
                elif event.key == pygame.K_UP:
                    direction = 1
                elif event.key == pygame.K_DOWN:
                    direction = -1
                elif event.key == pygame.K_r:
                    current_dim_val = 0.0
                    direction = 1

        current_dim_val += direction * ANIMATION_SPEED * dt

        if current_dim_val > MAX_DIMENSION:
            current_dim_val = MAX_DIMENSION
            direction = -1
        elif current_dim_val < 0:
            current_dim_val = 0
            direction = 1

        screen.fill(COLOR_BG)

        center_x, center_y = WIDTH // 2, HEIGHT // 2
        effective_dim = max(1, int(math.ceil(current_dim_val)))
        num_vertices = 1 << effective_dim

        positions = [
            (
                center_x + project_vertex(v, basis_vectors, current_dim_val)[0],
                center_y + project_vertex(v, basis_vectors, current_dim_val)[1]
            )
            for v in range(num_vertices)
        ]

        for v in range(num_vertices):
            px, py = positions[v]
            radius = 3 if effective_dim <= 6 else 1
            pygame.draw.circle(screen, COLOR_NODE, (int(px), int(py)), radius)

            for k in range(effective_dim):
                if not (v >> k) & 1:
                    neighbor = v | (1 << k)
                    if neighbor < num_vertices:
                        pygame.draw.line(
                            screen,
                            COLOR_EDGE,
                            (px, py),
                            positions[neighbor],
                            1
                        )

        screen.blit(
            font.render(f"Dimension: {current_dim_val:.2f}", True, COLOR_TEXT),
            (20, 20)
        )
        screen.blit(
            font.render("Controls: Space Pause | Up/Down | R Reset", True, COLOR_TEXT),
            (20, 50)
        )

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
