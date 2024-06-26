
import pygame
import random
import math

# Clases Nodo, Arista, y Grafo ya están definidas en el archivo proporcionado
from grafos4daa import *

def spring_layout(grafo, width, height, iterations=50, k=None, c=0.1, repulsion_factor=1, max_repulsive_force_distance=10.0):
    if k is None:
        k = math.sqrt((width * height) / len(grafo.nodos))
    positions = {nodo: (random.uniform(0, width), random.uniform(0, height)) for nodo in grafo.nodos}
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

def draw_graph(grafo, positions, width=800, height=600):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Grafo - Método de Resortes")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        
        # Dibujar aristas
        for v in grafo.aristas:
            for arista in grafo.aristas[v]:
                pygame.draw.line(screen, (0, 0, 0), positions[v], positions[arista.destino.nombre], 1)
        
        # Dibujar nodos
        for nodo in grafo.nodos:
            pygame.draw.circle(screen, (0, 0, 255), (int(positions[nodo][0]), int(positions[nodo][1])), 10)
            font = pygame.font.SysFont(None, 24)
            img = font.render(str(nodo), True, (0, 0, 0))
            screen.blit(img, (positions[nodo][0] - 10, positions[nodo][1] - 10))
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    
    grafo = grafoDorogovtsevMendes(100)

    width, height = 800, 600
    positions = spring_layout(grafo, width, height)
    draw_graph(grafo, positions, width, height)