import os
import random

def make_pack_instance(pack_object):
    output = {'path':pack_object.path,
              'packs_directory':pack_object.packs_directory,
              'owner':pack_object.owner,
              'icon':pack_object.icon,
              'public':pack_object.public,
              'description':pack_object.description,
              'pack_name':pack_object.pack_name,
              'id':pack_object.id,
              'deck':pack_object.deck
              }
    return output
    
def refill_deck(pack_object):
    pack_object['deck'] = os.listdir(pack_object['packs_directory'])

def pick_image(pack_object):
    if(pack_object['deck'] == 0):
        refill_deck(pack_object)
    image = random.randint(0,len(pack_object['deck'])-1)
    img_url = pack_object['deck'][image]
    del pack_object['deck'][image]
    return img_url

def print_pack_attb(pack_object):
    print(f'Directory: {pack_object["packs_directory"]}\nPack Name: {pack_object["pack_name"]}\nOwner: {pack_object["owner"]}\nImage List {pack_object["deck"]}\nID: {pack_object["id"]}')
    return 'Attributes Listed'