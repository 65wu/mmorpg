import pygame
from Model.Button import Button
from Model.Image import Image
from Model.Info import Info
from Resource.Battle import monster_test, player_test

run = True
pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("史莱姆大战勇士")

button = Button(pygame, screen, player_test)
image = Image(pygame, screen, monster_test.image, player_test.image)
info = Info(pygame, screen, player_test.basic_info(), monster_test.basic_info())


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
        info.load_text()
        button.load_button()
        pygame.display.update()
