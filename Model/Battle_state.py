def battle_state_detail(state_code):
    detail_map = {
        Battle_state.lose: "战斗失败",
        Battle_state.be_in_progress: "战斗进行中",
        Battle_state.win: "战斗胜利"
    }
    return detail_map[state_code]


class Battle_state:
    lose = -1
    be_in_progress = 0
    win = 1