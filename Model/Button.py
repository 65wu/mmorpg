from .Color import *


class Button:
    def __init__(
        self,
        game,
        screen,
        player,
        spacing=80,
        font_size=20,
        button_width=100,
        button_height=50
    ):
        self.game = game
        self.screen = screen
        self.spacing = spacing
        self.font_size = font_size
        self.button_width = button_width
        self.button_height = button_height

        self.button_list = [
            [self.spacing * (i + 1) + self.button_width * i, 500] +
            list(skill.values())
            for i, skill in enumerate(player.available_skill())
        ]

    def update_button_list(self, player):
        self.button_list = [
            [self.spacing * (i + 1) + self.button_width * i, 500] +
            list(skill.values())
            for i, skill in enumerate(player.available_skill())
        ]

    def load_button(self):
        game = self.game
        screen = self.screen
        skill_size = self.font_size
        skill_font = game.font.SysFont("SimHei", skill_size)
        button_width = self.button_width
        button_height = self.button_height

        for button in self.button_list:
            # button[0] 按钮x坐标
            # button[1] 按钮y坐标
            # button[2] 按钮上的技能文字
            game.draw.rect(screen, Color.grey, (*button[:2], button_width, button_height))
            button_text = skill_font.render(button[2], True, Color.black)
            # 水平且垂直居中
            screen.blit(
                button_text,
                (
                    button[0] + int((button_width - skill_size * len(str(button[2]))) / 2),
                    button[1] + int((button_height - skill_size) / 2)
                )
            )

    def check_button_coordinate(self, click_event):
        for index, button in enumerate(self.button_list):
            if button[0] <= click_event.pos[0] <= button[0] + self.button_width \
                    and button[1] <= click_event.pos[1] <= button[1] + self.button_width:
                return index
        return None
