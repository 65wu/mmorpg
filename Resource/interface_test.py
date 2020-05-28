import pygame
import os
from Resource.Battle import player_test

run = True
pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("史莱姆大战勇士")

data_dir = os.path.dirname(os.path.dirname(__file__)) + '/Data'
bg_dir = "/Image/Background/background.png"
monster_dir = "/Image/Role/knight.png"
player_dir = "/Image/Role/slime.png"

color_black = (0, 0, 0)
color_light_black = (40, 40, 40)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_grey = (240, 240, 240)
color_white = (255, 255, 255)

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
    int_size = 20
    int_font = pygame.font.SysFont("SimHei", int_size)

    player_max_hp = 500
    player_current_hp = 400
    player_max_mp = 100
    player_current_mp = 50

    monster_max_hp = 250
    monster_current_hp = 200
    monster_max_mp = 25
    monster_current_mp = 5

    monster_text_x = 20
    player_text_x = 500 + monster_text_x
    role_text_y = 70

    # 血条和蓝条
    rect_width = 250
    rect_height = 25

    frame_border = 1
    fame_width = rect_width + 2 * frame_border
    frame_height = rect_height + 2 * frame_border

    monster_frame_x = monster_text_x - frame_border
    player_frame_x = player_text_x - frame_border

    hp_y = 120
    mp_y = int(hp_y + rect_height * 6 / 5)

    hp_frame_y = hp_y - frame_border
    mp_frame_y = mp_y - frame_border

    text_list = [
        ("怪物名", font, "骑士", color_black, (monster_text_x, role_text_y)),
        ("玩家名", font, "史莱姆", color_black, (player_text_x, role_text_y)),
        ("怪物血量", int_font, str(monster_current_hp) + '/' + str(monster_max_hp), color_white, (
            monster_text_x + int(0.4 * rect_width), hp_y)),
        ("怪物魔法量", int_font, str(monster_current_mp) + '/' + str(monster_max_mp), color_white, (
            monster_text_x + int(0.4 * rect_width), mp_y)),
        ("玩家血量", int_font, str(player_current_hp) + '/' + str(player_max_hp), color_white, (
            player_text_x + int(0.4 * rect_width), hp_y)),
        ("玩家魔法量", int_font, str(player_current_mp) + '/' + str(player_max_mp), color_white, (
            player_text_x + int(0.4 * rect_width), mp_y))
    ]

    rect_list = [
        ("怪物hp底框", color_light_black, (monster_frame_x, hp_frame_y, fame_width, frame_height)),
        ("怪物mp底框", color_light_black, (monster_frame_x, mp_frame_y, fame_width, frame_height)),
        ("怪物hp条", color_green, (
            monster_text_x, hp_y, int(rect_width * (monster_current_hp / monster_max_hp)), rect_height)),
        ("怪物mp条", color_blue, (
            monster_text_x, mp_y, int(rect_width * (monster_current_mp / monster_max_mp)), rect_height)),
        ("玩家hp底框", color_light_black, (player_frame_x, hp_frame_y, fame_width, frame_height)),
        ("玩家mp底框", color_light_black, (player_frame_x, mp_frame_y, fame_width, frame_height)),
        ("玩家hp条", color_green, (player_text_x, hp_y, int(rect_width * (player_current_hp / player_max_hp)), rect_height)),
        ("玩家mp条", color_blue, (player_text_x, mp_y, int(rect_width * (player_current_mp / player_max_mp)), rect_height))
    ]

    for rect in rect_list:
        pygame.draw.rect(screen, rect[1], rect[2])

    for text_package in text_list:
        characters = text_package[1].render(text_package[2], True, text_package[3])
        screen.blit(characters, text_package[4])


spacing = 80
button_list = [
    [spacing * (i + 1) + button_width * i, 500] +
    list(skill.values())
    for i, skill in enumerate(player_test.available_skill())
]


print(button_list)


def load_button():
    skill_size = 20
    skill_font = pygame.font.SysFont("SimHei", skill_size)
    for button in button_list:
        # button[0] 按钮x坐标
        # button[1] 按钮y坐标
        # button[2] 按钮上的技能文字
        pygame.draw.rect(screen, color_grey, (*button[:2], button_width, button_height))
        button_text = skill_font.render(button[2], True, color_black)
        # 水平且垂直居中
        screen.blit(
            button_text,
            (
                button[0] + int((button_width - skill_size * len(str(button[2]))) / 2),
                button[1] + int((button_height - skill_size) / 2)
            )
        )


def check_button_coordinate(click_event):
    for index, button in enumerate(button_list):
        if button[0] <= click_event.pos[0] <= button[0] + button_width \
                and button[1] <= click_event.pos[1] <= button[1] + button_width:
            return index
    return None


if __name__ == '__main__':
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                tmp_skill_id = check_button_coordinate(event)
                if tmp_skill_id is not None:
                    skill_id = tmp_skill_id
                    print(f"图形界面{skill_id=}")

        load_image()
        load_text()
        load_button()
        pygame.display.update()
