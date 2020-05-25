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

    role_size = 300, 300
    role_y = 160
    monster_x = 0
    player_x = 500

    monster_source = pygame.image.load(data_dir + monster_dir)
    monster = pygame.transform.scale(monster_source, role_size)

    player_source = pygame.image.load(data_dir + player_dir)
    player_scale = pygame.transform.scale(player_source, role_size)
    player = pygame.transform.flip(player_scale, True, False)

    screen.blit(bg, (0, 0))
    screen.blit(monster, (monster_x, role_y))
    screen.blit(player, (player_x, role_y))


def load_text():
    font_size = 35
    font = pygame.font.SysFont("SimHei", font_size)
    monster_name = font.render("骑士", True, (0, 0, 0))
    player_name = font.render("史莱姆", True, (0, 0, 0))

    monster_text_x = 20
    player_text_x = 500 + monster_text_x
    role_text_y = 70

    # 角色名称
    screen.blit(monster_name, (monster_text_x, role_text_y))
    screen.blit(player_name, (player_text_x, role_text_y))

    # 血条和蓝条
    rect_width = 250
    rect_height = 25
    hp_y = 120
    mp_y = int(hp_y + rect_height * 6 / 5)

    pygame.draw.rect(screen, (0, 255, 0), (monster_text_x, hp_y, rect_width, rect_height))
    pygame.draw.rect(screen, (0, 0, 255), (monster_text_x, mp_y, rect_width, rect_height))


if __name__ == '__main__':
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_LEFT]:
            #     skill_id = 1
            #     print(f"图形界面{skill_id=}")

        load_image()
        load_text()
        pygame.display.update()
