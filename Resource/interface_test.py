import pygame
from Model.Color import Color
from Model.Button import Button
from Model.Image import Image
from Resource.Battle import monster_test, player_test

run = True
pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("史莱姆大战勇士")

button = Button(pygame, screen, player_test)
image = Image(pygame, screen, monster_test.image, player_test.image)


def load_text():
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

    rect_list = [
        ("怪物hp底框", Color.light_black, (monster_frame_x, hp_frame_y, fame_width, frame_height)),
        ("怪物mp底框", Color.light_black, (monster_frame_x, mp_frame_y, fame_width, frame_height)),
        ("怪物hp条", Color.green, (
            monster_text_x, hp_y, int(rect_width * (monster_current_hp / monster_max_hp)), rect_height)),
        ("怪物mp条", Color.blue, (
            monster_text_x, mp_y, int(rect_width * (monster_current_mp / monster_max_mp)), rect_height)),
        ("玩家hp底框", Color.light_black, (player_frame_x, hp_frame_y, fame_width, frame_height)),
        ("玩家mp底框", Color.light_black, (player_frame_x, mp_frame_y, fame_width, frame_height)),
        ("玩家hp条", Color.green,
         (player_text_x, hp_y, int(rect_width * (player_current_hp / player_max_hp)), rect_height)),
        ("玩家mp条", Color.blue,
         (player_text_x, mp_y, int(rect_width * (player_current_mp / player_max_mp)), rect_height))
    ]

    for rect in rect_list:
        pygame.draw.rect(screen, rect[1], rect[2])


if __name__ == '__main__':
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                tmp_skill_id = button.check_button_coordinate(event)
                if tmp_skill_id is not None:
                    skill_id = tmp_skill_id
                    print(f"图形界面{skill_id=}")

        image.load_image()
        load_text()
        button.load_button()
        pygame.display.update()
