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
    """raises the exception, performs cleanup if needed"""
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


class Battle_logic:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.game_round = Round(player, monster)

    def round_status_print(self, round_result):
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
        print(f"""
        {self.player}对{self.monster}造成了{round_result["damage"]["by_player"]}伤害
        {self.monster}对{self.player}造成了{round_result["damage"]["by_monster"]}伤害
        """)

    def start(self):
        global skill_id, round_info

        game_round = self.game_round
        round_result = dict()
        round_result["battle_state"] = Battle_state.be_in_progress

        while round_result["battle_state"] == Battle_state.be_in_progress:
            if game_round.count:
                self.round_status_print(round_result)
                self.round_damage_print(round_result)
            game_round.count += 1

            skill_choose_event.clear()
            skill_choose_event.wait()

            round_result = game_round.exec(skill_id)
            round_info = round_result["round_info"]
            round_info_event.set()

        self.round_status_print(round_result)
        time.sleep(2)
        stop_thread(interface)


class Battle_interface:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster

    def start(self):
        global skill_id, round_info

        run = True
        pygame.init()

        screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption("史莱姆大战勇士")

        button = Button(pygame, screen, self.player)
        image = Image(pygame, screen, self.monster.image, self.player.image)
        info = Info(pygame, screen, self.monster.basic_info(), self.player.basic_info())

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tmp_skill_id = button.check_button_coordinate(event)
                    if tmp_skill_id is not None:
                        skill_id = tmp_skill_id
                        skill_choose_event.set()

                        round_info_event.clear()
                        round_info_event.wait()

                        info.update_info(round_info["monster_info"], round_info["player_info"])
                        button.update_button_list(self.player)
            image.load_image()
            info.load_text()
            button.load_button()
            pygame.display.update()

        pygame.quit()
        skill_choose_event.set()
        stop_thread(logic)


skill_choose_event = threading.Event()
round_info_event = threading.Event()

skill_id = 0
round_info = {}

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
battle_logic = Battle_logic(player_test, monster_test)
battle_interface = Battle_interface(player_test, monster_test)

if __name__ == '__main__':
    logic = threading.Thread(target=battle_logic.start)
    interface = threading.Thread(target=battle_interface.start)
    logic.start()
    interface.start()
    logic.join()
    interface.join()

