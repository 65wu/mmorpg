from Model.Interface.Color import *


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
        """
        信息类初始化
        :param game: pygame
        :param screen: 屏幕
        :param monster_info: 怪物信息，是个字典，会含有名称，当前和最大hp、mp
        :param player_info: 玩家信息，数据类型同上
        :param char_size: 文字大小
        :param int_size: 数字大小
        :param x_bias: x偏移值，使文字不是紧贴左边的
        :param monster_text_x: 怪物名称的x坐标
        :param player_text_x: 玩家名称的x坐标
        :param role_text_y: 名称文本的y坐标
        :param rect_width: 矩形宽度
        :param rect_height: 矩形高度
        :param frame_border: 边框厚度
        :param hp_y: hp放置的y值
        """
        self.game = game
        self.screen = screen

        self.monster_info = monster_info
        self.player_info = player_info

        # 加载字体
        self.char_size = char_size
        self.int_size = int_size
        self.char_text = game.font.SysFont("SimHei", char_size)
        self.int_text = game.font.SysFont("SimHei", int_size)

        # 设定文本x,y值
        self.x_bias = x_bias
        self.monster_text_x = monster_text_x + x_bias
        self.player_text_x = player_text_x + x_bias
        self.role_text_y = role_text_y

        self.rect_width = rect_width
        self.rect_height = rect_height
        self.frame_border = frame_border

        # 生成x值
        self.fame_width = rect_width + 2 * frame_border
        self.frame_height = rect_height + 2 * frame_border
        self.monster_frame_x = self.monster_text_x - frame_border
        self.player_frame_x = self.player_text_x - frame_border

        # 生成y值
        self.hp_y = hp_y
        self.mp_y = int(hp_y + rect_height * 6 / 5)
        self.hp_frame_y = self.hp_y - frame_border
        self.mp_frame_y = self.mp_y - frame_border

    def update_info(self, monster_info, player_info):
        """
        每轮结束更新信息
        :param monster_info:
        :param player_info:
        :return:
        """
        self.monster_info = monster_info
        self.player_info = player_info

    def name_zip(self, name, x, y):
        """
        名称元祖封装
        :param name:
        :param x:
        :param y:
        :return:
        """
        return (
            self.char_text,
            name,
            Color.black,
            (x, y)
        )

    def point_zip(self, current_point, max_point, x, y):
        """
        hp、mp数值封装
        :param current_point:
        :param max_point:
        :param x:
        :param y:
        :return:
        """
        return (
            self.int_text,
            str(current_point) + '/' + str(max_point),
            Color.white,
            (x + int(0.4 * self.rect_width), y)
        )

    def bottom_frame_zip(self, x, y):
        """
        底框封装
        :param x:
        :param y:
        :return:
        """

        return (
            Color.light_black, (
                x,
                y,
                self.fame_width,
                self.frame_height
            )
        )

    def point_strip(self, point_type, x, y, current_point, max_point):
        """
        hp、mp条封装
        :param point_type:
        :param x:
        :param y:
        :param current_point:
        :param max_point:
        :return:
        """
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

        for text_package in text_list:
            characters = text_package[0].render(text_package[1], True, text_package[2])
            self.screen.blit(characters, text_package[3])
