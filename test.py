import os
import databaseutils
import game_instance_utils
import game_pack_utils
import game_player_utils
#packs_directory = './static/images/packs/default'
#print(os.listdir(packs_directory))
#databaseutils.make_default_pack()
#databaseutils.get_pack_by_username_and_pack_name('collin','default').print_attb()

player1 = game_player_utils.make_player_instance('William')
player2 = game_player_utils.make_player_instance('Joe')
player3 = game_player_utils.make_player_instance('Steve')
p = databaseutils.get_pack_by_path('default')

pack_inst = game_pack_utils.make_pack_instance(p)

p_list = [player1,player2,player3]

game_hand = game_instance_utils.make_game_instance(p_list,pack_inst,len(p_list),3,'William',2,'test_lobby')

databaseutils.db_test.insert_one(game_hand)
databaseutils.get_game_inst_by_host('William')