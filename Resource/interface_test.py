import pygame
import os

run = True
pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("史莱姆大战勇士")

data_dir = os.path.dirname(os.path.dirname(__file__)) + '/Data'
bg_dir = "/Image/Background/background.png"
monster_dir = "/Image/Role/knight.png"
player_dir = "/Image/Role/slime.png"

button_x = 100
button_y = 500
button_width = 100
button_height = 50


def load_image():
    bg_source = pygame.image.load(data_dir + bg_dir)
    bg = pygame.transform.scale(bg_source, (800, 600))

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
    global run
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
    rect_height = 20
    hp_y = 120
    mp_y = int(hp_y + rect_height * 6 / 5)

    pygame.draw.rect(screen, (0, 255, 0), (monster_text_x, hp_y, rect_width, rect_height))
    pygame.draw.rect(screen, (0, 0, 255), (monster_text_x, mp_y, rect_width, rect_height))

    pygame.draw.rect(screen, (0, 255, 0), (player_text_x, hp_y, rect_width, rect_height))
    pygame.draw.rect(screen, (0, 0, 255), (player_text_x, mp_y, rect_width, rect_height))

    player_max_hp = 500
    player_current_hp = 400
    player_max_mp = 100
    player_current_mp = 50

    monster_max_hp = 250
    monster_current_hp = 200
    monster_max_mp = 25
    monster_current_mp = 5

    int_size = 20
    int_font = pygame.font.SysFont("SimHei", int_size)

    monster_hp = int_font.render(str(monster_current_hp) + '/' + str(monster_max_hp), True, (0, 0, 0))
    monster_mp = int_font.render(str(monster_current_mp) + '/' + str(monster_max_mp), True, (0, 0, 0))

    player_hp = int_font.render(str(player_current_hp) + '/' + str(player_max_hp), True, (0, 0, 0))
    player_mp = int_font.render(str(player_current_mp) + '/' + str(player_max_mp), True, (0, 0, 0))

    screen.blit(monster_hp, (monster_text_x + int(0.4 * rect_width), hp_y))
    screen.blit(monster_mp, (monster_text_x + int(0.4 * rect_width), mp_y))

    screen.blit(player_hp, (player_text_x + int(0.4 * rect_width), hp_y))
    screen.blit(player_mp, (player_text_x + int(0.4 * rect_width), mp_y))


spacing = 80
button_vector_list = [
    (spacing * (i + 1) + button_width * i, 500)
    for i in range(4)
]


def load_button():
    for button_vector in button_vector_list:
        pygame.draw.rect(screen, (200, 200, 200), (*button_vector, button_width, button_height))


if __name__ == '__main__':
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN \
                    and button_x <= event.pos[0] <= button_x + button_width \
                    and button_y <= event.pos[1] <= button_y + button_height:
                skill_id = 1
                print(f"图形界面{skill_id=}")

        load_image()
        load_text()
        load_button()
        pygame.display.update()
