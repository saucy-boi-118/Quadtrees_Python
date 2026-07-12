import pygame
import numpy as np
import settings as s

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((s.WINW,s.WINH))
Clock = pygame.time.Clock()
pygame.display.set_caption(s.TITLE)
running = True

# Variables
arr = np.random.randint(s.WINW,size=10)

while running:
    # Loop through events for input
    for event in pygame.event.get():
        # X button on the screen
        if event.type == pygame.QUIT: 
            running = False
        # Escape button
        elif event.type == pygame.K_ESCAPE:
            running = False

    # Clear the screen every frame
    screen.fill(s.WHITE)

    # Rendering the game

    # Updating the screen
    pygame.display.flip()

    # limit the FPS
    Clock.tick(60)

    
pygame.quit()