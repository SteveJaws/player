import pygame
from player import Player

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()
dt = 0
running = True

player = Player(0, 0, 64, 64, 400, "white")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    player.draw(screen, dt)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()