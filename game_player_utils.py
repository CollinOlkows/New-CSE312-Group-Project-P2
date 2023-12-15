import os
import random


def make_player_instance(username,score=0,input='',judge=False,submit=False):
    output = {'username':username,'score':score,'input':input,'judge':judge,'submit':submit}
    return output

def set_judge(player_instance):
    player_instance['judge'] = True

def reset(player_instance):
    player_instance['input'] = ''
    player_instance['judge'] = False
    player_instance['submit'] = False

def submit_answer(player_instance,input):
    player_instance['input'] = input
    player_instance['submit'] = True

def increase_score(player_instance):
    player_instance['score'] +=1

def print_player_attb(player_instance):
        print(f'username: {player_instance["username"]}\nscore: {player_instance["score"]}\ninput: {player_instance["input"]}\njudge: {player_instance["judge"]}\nsubmit: {player_instance["submit"]}')



