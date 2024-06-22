import os
import pygame
import random
import math
import imageio 

from grafos4daa import *



def spring_layout(grafo, width, height, positions, iterations=50, k=None, c=5.2, repulsion_factor=1, max_repulsive_force_distance=1.0):
    if k is None:
        k = math.sqrt((width * height) / len(grafo.nodos))
    disp = {nodo: (0, 0) for nodo in grafo.nodos}
    
    for _ in range(iterations):
        for v in grafo.nodos:
            disp[v] = (0, 0)
            for u in grafo.nodos:
                if v != u:
                    delta = (positions[v][0] - positions[u][0], positions[v][1] - positions[u][1])
                    distance = math.sqrt(delta[0]**2 + delta[1]**2)
                    if distance < 0.01:
                        distance = 0.01
                    repulsive_force = k * k / distance
                    disp[v] = (disp[v][0] + delta[0] / distance * repulsive_force, disp[v][1] + delta[1] / distance * repulsive_force)
        
        for v in grafo.aristas:
            for arista in grafo.aristas[v]:
                u = arista.destino.nombre
                delta = (positions[v][0] - positions[u][0], positions[v][1] - positions[u][1])
                distance = math.sqrt(delta[0]**2 + delta[1]**2)
                if distance < 0.01:
                    distance = 0.01
                attractive_force = (distance * distance) / k
                disp[v] = (disp[v][0] - delta[0] / distance * attractive_force, disp[v][1] - delta[1] / distance * attractive_force)
                disp[u] = (disp[u][0] + delta[0] / distance * attractive_force, disp[u][1] + delta[1] / distance * attractive_force)
        
        for v in grafo.nodos:
            delta = (disp[v][0], disp[v][1])
            distance = math.sqrt(delta[0]**2 + delta[1]**2)
            if distance > 0:
                positions[v] = (positions[v][0] + delta[0] / distance * min(c, distance), positions[v][1] + delta[1] / distance * min(c, distance))
            positions[v] = (min(width, max(0, positions[v][0])), min(height, max(0, positions[v][1])))
    
    return positions

def draw_graph(grafo, positions, width=800, height=600, delay=10, iterations_per_frame=10):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Grafo - Geográfico 100")
    clock = pygame.time.Clock()
    # Crear carpeta temporal para guardar los fotogramas
    if not os.path.exists('frames'):
        os.makedirs('frames')

    frame_count = 0
    running = True

    def draw():
        screen.fill((255, 255, 255))
        # Dibujar aristas
        for v in grafo.aristas:
            for arista in grafo.aristas[v]:
                if arista.origen.nombre in positions and arista.destino.nombre in positions:
                    pygame.draw.line(screen, (0, 0, 0), positions[arista.origen.nombre], positions[arista.destino.nombre], 1)
        
        # Dibujar nodos
        for nodo in grafo.nodos:
            if nodo in positions:
                pygame.draw.circle(screen, (0, 0, 255), (int(positions[nodo][0]), int(positions[nodo][1])), 10)
                font = pygame.font.SysFont(None, 24)
                img = font.render(str(nodo), True, (0, 0, 0))
                screen.blit(img, (positions[nodo][0] - 10, positions[nodo][1] - 10))

        pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Recalcular posiciones en cada iteración
        positions = spring_layout(grafo, width, height, positions, iterations=iterations_per_frame)
        draw()
        pygame.time.delay(delay)

        # Guardar fotograma
        frame_filename = f'frames/frame_{frame_count:04d}.png'
        pygame.image.save(screen, frame_filename)
        frame_count += 1

        clock.tick()

    pygame.quit()

    # Crear video a partir de los fotogramas
    with imageio.get_writer('Geográfico100.mp4', fps=30) as writer:
        for i in range(frame_count):
            frame_filename = f'frames/frame_{i:04d}.png'
            image = imageio.imread(frame_filename)
            writer.append_data(image)

    # Limpiar carpeta temporal
    for i in range(frame_count):
        frame_filename = f'frames/frame_{i:04d}.png'
        os.remove(frame_filename)
    os.rmdir('frames')

    print("Video guardado como 'animation.mp4'")

if __name__ == "__main__":
    # Generar un grafo utilizando uno de los modelos
    grafo = grafoGeografico(100, 0.10)
    
    width, height = 800, 600
    positions = {nodo: (random.uniform(0, width), random.uniform(0, height)) for nodo in grafo.nodos}
    draw_graph(grafo, positions, width, height, delay=10, iterations_per_frame=1)