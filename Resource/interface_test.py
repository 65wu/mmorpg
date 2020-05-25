import pygame
import os


run = True
pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("史莱姆大战勇士")

data_dir = os.path.dirname(os.path.dirname(__file__)) + '/Data'
bg_dir = "/Image/Background/background.jpg"
monster_dir = "/Image/Role/knight.png"
player_dir = "/Image/Role/slime.png"

bg = pygame.image.load(data_dir + bg_dir)

monster_source = pygame.image.load(data_dir + monster_dir)
monster = pygame.transform.scale(monster_source, (200, 200))

player_source = pygame.image.load(data_dir + player_dir)
player_scale = pygame.transform.scale(player_source, (200, 200))
player = pygame.transform.flip(player_scale, True, False)

font = pygame.font.SysFont("SimHei", 60)
text = font.render("中文", False, (255, 255, 255))


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            skill_id = 1
            print(f"图形界面{skill_id=}")
    screen.blit(bg, (0, 0))
    screen.blit(monster, (0, 150))
    screen.blit(player, (600, 150))
    screen.blit(text, (0, 100))
    pygame.display.update()

print(pygame.quit())
