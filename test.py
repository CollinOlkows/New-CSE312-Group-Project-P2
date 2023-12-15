import os
import databaseutils
import game_instance_utils
import game_pack_utils
import game_player_utils
#packs_directory = './static/images/packs/default'
#print(os.listdir(packs_directory))
#databaseutils.make_default_pack()
#databaseutils.get_pack_by_username_and_pack_name('collin','default').print_attb()
databaseutils.make_default_pack()
databaseutils.make_cats_pack()
databaseutils.make_will_pack()