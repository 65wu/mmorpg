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


def load_image():
    bg = pygame.image.load(data_dir + bg_dir)

    monster_source = pygame.image.load(data_dir + monster_dir)
    monster = pygame.transform.scale(monster_source, (300, 300))

    player_source = pygame.image.load(data_dir + player_dir)
    player_scale = pygame.transform.scale(player_source, (300, 300))
    player = pygame.transform.flip(player_scale, True, False)

    screen.blit(bg, (0, 0))
    screen.blit(monster, (0, 160))
    screen.blit(player, (500, 160))


def load_text():
    font = pygame.font.SysFont("SimHei", 35)
    monster_name = font.render("骑士", True, (0, 0, 0))
    player_name = font.render("史莱姆", True, (0, 0, 0))

    # 角色名称
    screen.blit(monster_name, (20, 70))
    screen.blit(player_name, (520, 70))


def load_hp_and_mp():
    # 血条和蓝条
    pygame.draw.rect(screen, (0, 255, 0), (20, 120, 250, 25))
    pygame.draw.rect(screen, (0, 0, 255), (20, 150, 250, 25))


if __name__ == '__main__':
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                skill_id = 1
                print(f"图形界面{skill_id=}")

        load_image()
        load_text()
        load_hp_and_mp()
        pygame.display.update()
