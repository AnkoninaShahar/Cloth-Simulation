import pygame
import manager

pygame.init()
screen = pygame.display.set_mode((1280, 960))
clock = pygame.time.Clock()
running = True

manager = manager.Manager()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(pygame.Color(41, 41, 41))

    manager.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()