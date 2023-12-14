import os
import databaseutils
#packs_directory = './static/images/packs/default'
#print(os.listdir(packs_directory))
databaseutils.make_default_pack()
databaseutils.get_pack_by_username_and_pack_name('collin','default').print_attb()