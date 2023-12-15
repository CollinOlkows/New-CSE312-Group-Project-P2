import os
import random
import game_pack_utils
import game_player_utils


def make_game_instance(players,pack,player_count,max_player_count,host,rounds,lobby):
    output = {'players' : players,
        'lobby' : lobby,
        'pack' : pack,
        'player_count' : player_count,
        'max_players' : max_player_count,
        'host' : host,
        'judge_candidate' : list(range(0,len(players))),
        'current_judge' : '',
        'current_round' : 0,
        'rounds' : rounds,
        'state' : 'Lobby',
        'current_image':''}
    return output

    

def check_game_end(game_instance):
    if(game_instance['current_round'] + 1 == game_instance['rounds']):
        return True
    else:
        return False

def award_points(game_instance,winner):
    for p in game_instance['players']:
        if p['username'] == winner:
            game_player_utils.increase_score(p)

def new_round(game_instance):
    if check_game_end(game_instance):
        pass # needs to end the game
    else:
        for p in game_instance['players']:
            game_player_utils.reset(p)
        game_instance['judge_candidate'] = list(range(0,len(game_instance['players'])))
        game_instance['current_round'] +=1

def select_judge(game_instance):
    num = game_instance['judge_candidate'][random.randint(0,len(game_instance['judge_candidate'])-1)]
    game_player_utils.set_judge(game_instance['players'][num])
    game_instance['judge_candidate'].remove(num)
    game_instance['current_judge'] = game_instance['players'][num]

#-----------------------------------------------------------------------

def get_player_scores(game_instance):
    output = {}
    for p in game_instance['players']:
        output[p['username']] = p['score']
    return output

#Pretty much only going to ever call the end turn function

def end_turn(game_instance,winner):
    if len(game_instance['judge_candidate'] == 0):
        new_round(game_instance)
    else:
        award_points(game_instance,winner)
        for p in game_instance['players']:
            game_player_utils.reset(p)
        select_judge(game_instance)
        current_image = game_pack_utils.pick_image(game_instance['pack'])
        game_instance['current_image'] = current_image
    
#Only called on initalization of game

def start_game(game_instance):
    current_image = game_pack_utils.pick_image(game_instance['pack'])
    game_instance['current_image'] = current_image
    select_judge(game_instance)