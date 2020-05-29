from Model.Interface.Color import *


class Button:
    def __init__(
        self,
        game,
        screen,
        player,
        spacing=80,
        font_size=20,
        button_width=100,
        button_height=50,
        button_y=500
    ):
        """
        按钮初始化
        :param game:
        :param screen: 屏幕
        :param player: 玩家，调用可用技能
        :param spacing: 按钮与按钮之间的间距
        :param font_size: 按钮文字大小
        :param button_width: 按钮宽度
        :param button_height: 按钮高度
        :param button_y: 按钮的y值
        """
        self.game = game
        self.screen = screen
        self.spacing = spacing
        self.font_size = font_size
        self.button_width = button_width
        self.button_height = button_height
        self.button_y = button_y

        # 生成button列表，是一个列表的列表
        # 子元素的属性分别为按钮x坐标, y坐标, 技能名字，是否有足够蓝释放
        self.button_list = [
            [self.spacing * (i + 1) + self.button_width * i, self.button_y] +
            list(skill.values())
            for i, skill in enumerate(player.available_skill())
        ]

    def update_button_list(self, player):
        """
        每到一个新的round更新技能状态
        :param player:
        :return:
        """
        self.button_list = [
            [self.spacing * (i + 1) + self.button_width * i, self.button_y] +
            list(skill.values())
            for i, skill in enumerate(player.available_skill())
        ]
        print(self.button_list)

    def load_button(self):
        """
        加载技能，既加载矩形，也加载技能文字
        :return:
        """
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
            # button[3] 技能是否有足够的魔法值释放

            x, y, text, available = button

            if available:
                color = Color.grey
            else:
                color = Color.grey_disable

            game.draw.rect(screen, color, (x, y, button_width, button_height))
            button_text = skill_font.render(text, True, Color.black)
            # 水平且垂直居中
            screen.blit(
                button_text,
                (
                    x + int((button_width - skill_size * len(str(text))) / 2),
                    y + int((button_height - skill_size) / 2)
                )
            )

    def check_button_coordinate(self, click_event):
        """
        检查鼠标点击区域是否在按钮上，并检查魔法值是否足够
        :param click_event:
        :return:
        """
        for index, button in enumerate(self.button_list):
            x, y, _, available = button

            if x <= click_event.pos[0] <= x + self.button_width \
                    and y <= click_event.pos[1] <= y + self.button_width:
                if available:
                    return index
                else:
                    return None
        return None
