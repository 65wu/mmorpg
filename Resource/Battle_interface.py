import pygame


pygame.init()
screen = pygame.display.set_mode([500, 500])
pygame.display.set_caption("史莱姆大战勇士")

run = True

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
