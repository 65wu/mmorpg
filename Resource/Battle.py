import pygame
import threading
from Model.Battle_state import Battle_state, battle_state_detail
from Model.Role import Monster, Player
from Model.Round import Round
from Model.Skill import Skill


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
        game_round = self.game_round
        thread_event.wait()
        print(f"{skill_id=}")
        round_result = game_round.exec(skill_id)

        while round_result["battle_state"] == Battle_state.be_in_progress:
            self.round_status_print(round_result)
            self.round_damage_print(round_result)
            game_round.count += 1
            thread_event.wait()
            print(f"{skill_id=}")
            round_result = game_round.exec(skill_id)

        self.round_status_print(round_result)


def interface():
    run = True
    pygame.init()
    pygame.display.set_mode([500, 500])
    pygame.display.set_caption("史莱姆大战勇士")
    global skill_id
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                skill_id = 1
                print(f"图形界面{skill_id=}")
                thread_event.set()
    pygame.quit()


thread_event = threading.Event()
lock = threading.Lock()
skill_id = 0

monster_b = Monster(
    name="骑士",
    level=1,
    hp=250,
    mp=25,
    attack=25,
    defence=15,
    speed=1,
    skill_list=[
        Skill("盾击", 20, 12),
        Skill("挥砍", 30, 15)
    ]
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
        Skill("粘液喷吐", 10, 5),
        Skill("肉弹冲击", 25, 15),
        Skill("猛击", 35, 20)
    ]
)
battle = Battle_logic(player_test, monster_b)

if __name__ == '__main__':
    p = threading.Thread(target=battle.start)
    p.start()
    c = threading.Thread(target=interface)
    c.start()
