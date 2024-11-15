def get_is_win(radiant_win, player_slot):
    is_win = ''
    if radiant_win:
        if player_slot < 128:
            is_win = 'Победа'
            return is_win
        else:
            is_win = 'Поражение'
            return is_win
    else:
        if player_slot >= 128:
            is_win = 'Победа'
            return is_win
        else: 
            is_win = 'Поражение'
            return is_win