from .Color import *


class Info:
    def __init__(
            self,
            game,
            screen,
            monster_info,
            player_info,
            char_size=35,
            int_size=20,
            x_bias=20,
            monster_text_x=0,
            player_text_x=500,
            role_text_y=70,
            rect_width=250,
            rect_height=25,
            frame_border=1,
            hp_y=120
    ):
        self.game = game
        self.screen = screen

        self.monster_info = monster_info
        self.player_info = player_info

        self.char_size = char_size
        self.int_size = int_size
        self.char_text = game.font.SysFont("SimHei", char_size)
        self.int_text = game.font.SysFont("SimHei", int_size)

        self.x_bias = x_bias
        self.monster_text_x = monster_text_x + x_bias
        self.player_text_x = player_text_x + x_bias
        self.role_text_y = role_text_y

        self.rect_width = rect_width
        self.rect_height = rect_height
        self.frame_border = frame_border

        self.fame_width = rect_width + 2 * frame_border
        self.frame_height = rect_height + 2 * frame_border
        self.monster_frame_x = monster_text_x - frame_border
        self.player_frame_x = player_text_x - frame_border

        self.hp_y = hp_y
        self.mp_y = int(hp_y + rect_height * 6 / 5)
        self.hp_frame_y = self.hp_y - frame_border
        self.mp_frame_y = self.mp_y - frame_border

    def name_zip(self, name, x, y):
        return (
            self.char_text,
            name,
            Color.black,
            (x, y)
        )

    def point_zip(self, current_point, max_point, x, y):
        return (
            self.int_text,
            str(current_point) + '/' + str(max_point),
            Color.white,
            (x + int(0.4 * self.rect_width), y)
        )

    def bottom_frame_zip(self, x, y):
        return (
            Color.light_black, (
                x,
                y,
                self.fame_width,
                self.frame_height
            )
        )

    def point_strip(self, point_type, x, y, current_point, max_point):
        if point_type == 'hp':
            color = Color.green
        elif point_type == 'mp':
            color = Color.blue
        else:
            raise TypeError
        return (
            color, (
                x,
                y,
                int(self.rect_width * (current_point / max_point)),
                self.rect_height
            )
        )

    def load_text(self):
        monster_name = self.name_zip(
            self.monster_info["name"],
            self.monster_text_x,
            self.role_text_y
        )
        player_name = self.name_zip(
            self.player_info["name"],
            self.player_text_x,
            self.role_text_y
        )

        monster_hp = self.point_zip(
            self.monster_info["hp_current"],
            self.monster_info["hp_max"],
            self.monster_text_x,
            self.hp_y
        )
        monster_mp = self.point_zip(
            self.monster_info["mp_current"],
            self.monster_info["mp_max"],
            self.monster_text_x,
            self.mp_y
        )
        player_hp = self.point_zip(
            self.player_info["hp_current"],
            self.player_info["hp_max"],
            self.player_text_x,
            self.hp_y
        )
        player_mp = self.point_zip(
            self.player_info["mp_current"],
            self.player_info["mp_max"],
            self.player_text_x,
            self.mp_y
        )

        text_list = [
            monster_name,
            player_name,
            monster_hp,
            monster_mp,
            player_hp,
            player_mp
        ]

        for text_package in text_list:
            characters = text_package[0].render(text_package[1], True, text_package[2])
            self.screen.blit(characters, text_package[3])

        monster_hp_bottom_frame = self.bottom_frame_zip(self.monster_frame_x, self.hp_frame_y)
        monster_mp_bottom_frame = self.bottom_frame_zip(self.monster_frame_x, self.mp_frame_y)
        player_hp_bottom_frame = self.bottom_frame_zip(self.player_frame_x, self.hp_frame_y)
        player_mp_bottom_frame = self.bottom_frame_zip(self.player_frame_x, self.mp_frame_y)

        monster_hp_strip = self.point_strip(
            'hp',
            self.monster_text_x,
            self.hp_y,
            self.monster_info["hp_current"],
            self.monster_info["hp_max"]
        )

        monster_mp_strip = self.point_strip(
            'mp',
            self.monster_text_x,
            self.mp_y,
            self.monster_info["mp_current"],
            self.monster_info["mp_max"]
        )

        player_hp_strip = self.point_strip(
            'hp',
            self.player_text_x,
            self.hp_y,
            self.player_info["hp_current"],
            self.player_info["hp_max"]
        )

        player_mp_strip = self.point_strip(
            'mp',
            self.player_text_x,
            self.mp_y,
            self.player_info["mp_current"],
            self.player_info["mp_max"]
        )

        rect_list = [
            monster_hp_bottom_frame,
            monster_mp_bottom_frame,
            player_hp_bottom_frame,
            player_mp_bottom_frame,
            monster_hp_strip,
            monster_mp_strip,
            player_hp_strip,
            player_mp_strip
        ]

        for rect in rect_list:
            self.game.draw.rect(self.screen, rect[0], rect[1])
