def get_player_rank(rank_tier):
    rank = ''
    if rank_tier >= 10:
        rank = 'Рекрут'
        if rank_tier == 11:
            return rank + ' 1'
        if rank_tier == 12:
            return rank + ' 2'
        if rank_tier == 13:
            return rank + ' 3'
        if rank_tier == 14:
            return rank + ' 4'
        if rank_tier == 15:
            return rank + ' 5'
    if rank_tier >= 20:
        rank = 'Страж'
        if rank_tier == 21:
            return rank + ' 1'
        if rank_tier == 22:
            return rank + ' 2'
        if rank_tier == 23:
            return rank + ' 3'
        if rank_tier == 24:
            return rank + ' 4'
        if rank_tier == 25:
            return rank + ' 5'
    if rank_tier >= 30:
        rank = 'Рыцарь'
        if rank_tier == 31:
            return rank + ' 1'
        if rank_tier == 32:
            return rank + ' 2'
        if rank_tier == 33:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_3.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_3.png" height="100%" width="100%"></image></svg>'
        if rank_tier == 34:
            return rank + ' 4'
        if rank_tier == 35:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_3.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_5.png" height="100%" width="100%"></image></svg>'
    if rank_tier >= 40:
        rank = 'Герой'
        if rank_tier == 41:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_4.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_1.png" height="100%" width="100%"></image></svg>'
        if rank_tier == 42:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_4.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_2.png" height="100%" width="100%"></image></svg>'
        if rank_tier == 43:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_4.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_3.png" height="100%" width="100%"></image></svg>'
        if rank_tier == 44:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_4.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_4.png" height="100%" width="100%"></image></svg>'
        if rank_tier == 45:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_4.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_5.png" height="100%" width="100%"></image></svg>'
    if rank_tier >= 50:
        rank = 'Легенда'
        if rank_tier == 51:
            return rank + ' 1'
        if rank_tier == 52:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_5.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_2.png" height="100%" width="100%"></image></svg>'
        if rank_tier == 53:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_5.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_3.png" height="100%" width="100%"></image></svg>'
        if rank_tier == 54:
            return rank + ' 4'
        if rank_tier == 55:
            return rank + ' 5'
    if rank_tier >= 60:
        rank = 'Властелин'
        if rank_tier == 61:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_6.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_1.png" height="100%" width="100%"></image></svg>'
        if rank_tier == 62:
            return rank + ' 2'
        if rank_tier == 63:
            return rank + ' 3'
        if rank_tier == 64:
            return rank + ' 4'
        if rank_tier == 65:
            return rank + ' 5'   
    if rank_tier >= 70:
        rank = 'Божество'
        if rank_tier == 71:
            return rank + ' 1'
        if rank_tier == 72:
            return '<svg viewBox="0 0 256 256" style="max-width: 256px; max-height: 256px; width: 52px; height: 52px;"><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/medal_7.png" height="100%" width="100%"></image><image href="https://cdn.stratz.com/images/dota2/seasonal_rank/star_2.png" height="100%" width="100%"></image></svg>'
        if rank_tier == 73:
            return rank + ' 3'
        if rank_tier == 74:
            return rank + ' 4'
        if rank_tier == 75:
            return rank + ' 5'   