import ctypes
import inspect
import pygame
import time
import threading
from Model.Interface.Button import Button
from Model.Interface.Image import Image
from Model.Interface.Info import Info
from Model.Logic.Battle_state import Battle_state, battle_state_detail
from Model.Logic.Role import Monster, Player
from Model.Logic.Round import Round
from Model.Logic.Skill import Skill


def _async_raise(tid, exec_type):
    """
    杀死线程
    raises the exception, performs cleanup if needed
    """
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exec_type):
        exec_type = type(exec_type)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exec_type))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class Battle:
    class Battle_interface:
        def __init__(self, player, monster, battle):
            """
            战斗逻辑层初始化
            :param player: 玩家
            :param monster: 怪物
            :param battle: 战斗类，方便拿外部类的公有属性
            """
            self.player = player
            self.monster = monster
            self.battle = battle

        def start(self):
            """
            逻辑启动
            :return: 无
            """
            # 初始化pygame，我塞__init__里会爆bug，拿不到处理过的pygame, 不晓得为什么
            run = True
            pygame.init()

            # 初始化屏幕
            screen = pygame.display.set_mode([800, 600])
            pygame.display.set_caption("史莱姆大战勇士")

            # 初始化按钮类、图片类和信息类
            button = Button(pygame, screen, self.player)
            image = Image(pygame, screen, self.monster.image, self.player.image)
            info = Info(pygame, screen, self.monster.basic_info(), self.player.basic_info())

            # pygame事件循环
            while run:
                for event in pygame.event.get():
                    # 如果点右上角，设定循环条件为否
                    if event.type == pygame.QUIT:
                        run = False
                    # 如果有点击事件
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # 调用按钮类的检查函数，会去判断点击的坐标是不是在按钮上，并判断点的是哪个技能按钮
                        tmp_skill_id = button.check_button_coordinate(event)
                        # 如果点的是按钮
                        if tmp_skill_id is not None:
                            self.battle.skill_id = tmp_skill_id
                            # 释放逻辑层的技能等待锁
                            self.battle.skill_choose_event.set()

                            # 重置本轮信息锁为锁定，并等待逻辑层响应
                            self.battle.round_info_event.clear()
                            self.battle.round_info_event.wait()

                            # 拿到逻辑层信息后，更新血条蓝条
                            info.update_info(
                                self.battle.round_info["monster_info"],
                                self.battle.round_info["player_info"]
                            )
                            # 更新技能状况，蓝不够的技能会变灰
                            button.update_button_list(self.player)

                image.load_image()
                info.load_text()
                button.load_button()
                pygame.display.update()

            pygame.quit()
            # 用户主动关闭窗口，先释放逻辑层的锁，再杀死逻辑线程
            self.battle.skill_choose_event.set()
            stop_thread(self.battle.logic)

    class Battle_logic:
        def __init__(self, player, monster, battle):
            """
            逻辑层初始化
            :param player: 玩家对象
            :param monster: 怪物对象
            :param battle: 战斗类，拿公有属性和方法
            """
            self.player = player
            self.monster = monster
            self.battle = battle

            # 初始化round类，并设定战斗结果为-2，意味着异常退出
            self.game_round = Round(player, monster)
            self._result = -2

        def round_status_print(self, round_result):
            """
            本轮信息log打印函数
            :param round_result:
            :return:
            """
            game_round = self.game_round
            print(f"""
            {game_round},
            {battle_state_detail(round_result["battle_state"])}

            当前{self.player}
            血量为{round_result["round_info"]["player_info"]["hp_current"]},
            魔法量为{round_result["round_info"]["player_info"]["mp_current"]}

            {self.monster}
            血量为{round_result["round_info"]["monster_info"]["hp_current"]},
            魔法量为{round_result["round_info"]["monster_info"]["mp_current"]}
            """)

        def round_damage_print(self, round_result):
            """
            伤害打印函数
            :param round_result:
            :return:
            """
            print(f"""
            {self.player}对{self.monster}造成了{round_result["damage"]["by_player"]}伤害
            {self.monster}对{self.player}造成了{round_result["damage"]["by_monster"]}伤害
            """)

        def start(self):
            """
            逻辑层启动
            :return:
            """

            game_round = self.game_round
            round_result = dict()
            round_result["battle_state"] = Battle_state.be_in_progress

            # 如果游戏未结束，则继续循环
            while round_result["battle_state"] == Battle_state.be_in_progress:
                # 第一轮不打印信息
                if game_round.count:
                    self.round_status_print(round_result)
                    self.round_damage_print(round_result)
                game_round.count += 1

                # 重置技能选择锁，等待用户在界面上的操作
                self.battle.skill_choose_event.clear()
                self.battle.skill_choose_event.wait()

                # 技能选择锁释放后，计算这轮的伤害和角色当前信息，信息是储存在外部公有属性里的
                round_result = game_round.exec(self.battle.skill_id)
                self.battle.round_info = round_result["round_info"]
                # 释放本轮信息锁
                self.battle.round_info_event.set()

            # 战斗结束，打印最终结果，并休眠两秒，以免退出太快看不清
            self.round_status_print(round_result)
            time.sleep(2)
            # 更新battle_state信息
            self._result = round_result["battle_state"]

            stop_thread(self.battle.interface)

        def get_result(self):
            """
            获取战斗结果，以调用exp函数
            :return:
            """
            return battle_state_detail(self._result)

    def __init__(self, player, monster):
        """
        战斗类初始化，负责储藏公有属性，和初始化逻辑层和界面层线程
        :param player: 玩家对象
        :param monster: 怪物对象
        """
        self.player = player
        self.monster = monster

        # 初始化两把进程锁
        self.skill_choose_event = threading.Event()
        self.round_info_event = threading.Event()
        # 技能id和战斗信息，作为公有信息，因为两个线程都需要使用
        self.skill_id = 0
        self.round_info = {}

        # 初始化两个类
        self.battle_logic = self.Battle_logic(self.player, self.monster, self)
        self.battle_interface = self.Battle_interface(self.player, self.monster, self)
        # 初始化它们的线程
        self.logic = threading.Thread(target=self.battle_logic.start)
        self.interface = threading.Thread(target=self.battle_interface.start)

    def run(self):
        # 线程启动
        self.logic.start()
        self.interface.start()
        # 阻塞主线程
        self.logic.join()
        self.interface.join()
        # 返回战斗结果状态码
        return self.battle_logic.get_result()


def test():
    """
    测试方法
    :return:
    """
    monster_test = Monster(
        name="骑士",
        level=1,
        hp=100,
        mp=25,
        attack=25,
        defence=15,
        speed=1,
        skill_list=[
            Skill("盾击", 20, 12),
            Skill("挥砍", 30, 15)
        ],
        image="/Image/Role/knight.png"
    )
    player_test = Player(
        name="史莱姆",
        level=1,
        exp=0,
        hp=500,
        mp=100,
        attack=30,
        defence=10,
        speed=3,
        skill_list=[
            Skill("粘液喷吐", 10, 30),
            Skill("肉弹冲击", 25, 50),
            Skill("猛击", 35, 80)
        ],
        image="/Image/Role/slime.png"
    )
    battle_test = Battle(player_test, monster_test)
    print(battle_test.run())


if __name__ == '__main__':
    test()
