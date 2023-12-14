import os
import random

class card:
    def __init__(self):
        self.title = '' #Card text
        self.type = '' #Either Prompt or Response

class player:
    def __init__(self,username):
        self.score = 0
        self.username = username
        self.input = ''
        self.judge = False
        self.submit = False

    def set_judge(self):
        self.judge = True

    def reset(self):
        self.input = ''
        self.judge = False
        self.submit = False

    def submit_answer(self,input):
        self.input = input
        self.submit = True
    
    def increase_score(self):
        self.score +=1
    
    def print_attb(self):
        print(f'username = {self.username}\n score = {self.score}\n')
 
class pack:
    def __init__(self,pack_object):
        self.path = pack_object['path']
        self.packs_directory = './static/images/packs/' + pack_object['path']
        self.owner = pack_object['username']
        self.icon = 'logo.png'
        self.public = pack_object['public']
        self.description = pack_object['description']
        self.pack_name = pack_object['pack_name']
        self.id = pack_object['_id']
        self.deck = os.listdir(self.packs_directory)

    
    def refill_deck(self):
        self.deck = os.listdir(self.packs_directory)

    def pick_image(self):
        if(self.deck == 0):
            self.refill_deck()
        image = random.randint(0,len(self.deck)-1)
        img_url = self.deck[image]
        del self.deck[image]
        return img_url
    
    def print_attb(self):
        print(f'Directory: {self.packs_directory}\nPack Name: {self.pack_name}\nOwner: {self.owner}\nImage List {self.deck}\nID: {self.id}')
        return 'Attributes Listed'



class game:
    def __init__(self,players,pack,player_count,max_player_count,host,rounds,lobby):
        self.players = players # list of players
        self.lobby = lobby
        self.pack = pack
        self.player_count = player_count
        self.max_players = max_player_count
        self.host = host
        self.judge_candidate = list(range(0,len(players)))
        self.current_judge = ''
        self.rounds = rounds
        self.state = 'Lobby'
    

    def new_round(self):
        self.judge_candidate = list(range(0,len(self.players)))

    def end_turn(self):
        for p in self.players:
            p.reset()

    def select_judge(self):
        num = self.judge_candidate[random.randint(0,len(self.judge_candidate)-1)]
        self.players[num].set_judge()
        self.judge_candidate.remove(num)
        self.current_judge = self.players[num]

    def start_game(self):
        current_image = self.pack.pick_image()



'''def test_pack():
    p = pack()
    print(p.deck)
    card = p.pick_image()
    os.system('start ' +p.packs_directory+p.pack_name+'/'+card)
    print(p.deck)
    card = p.pick_image()
    os.system('start ' +p.packs_directory+p.pack_name+'/'+card)
    card = p.pick_image()
    os.system('start ' +p.packs_directory+p.pack_name+'/'+card)
    card = p.pick_image()
    os.system('start ' +p.packs_directory+p.pack_name+'/'+card)

def test_game():
    # Using the default image pack
    p = pack()
    # Creating a game instance
    game_state = game(p,5,2)
    # Setting Chris as the lobby host
    game_state.add_player('Chris')
    # Adding a player
    game_state.add_player('Phil')
    # adding a player
    game_state.add_player('Rob')
    # adding a player that already exists.... should print an error
    game_state.add_player('Rob')
     # adding a player
    game_state.add_player('Rob1')
     # adding a player
    game_state.add_player('Rob2')
    # adding a player when lobby full
    game_state.add_player('Rob3')
    #checking player insertion
    for player in game_state.players:
        game_state.players[player].print_attb()
    #Checking can't remove host from lobby -> require them to end the game
    game_state.remove_player('Chris')
    # Host should still exist
    game_state.players['Chris'].print_attb()
    #Printing non host user
    game_state.players['Rob'].print_attb()
    #testing deleting a player removes them from the playerlist and is no longer accessable
    game_state.remove_player('Rob')
    try:
        game_state.players['Rob'].print_attb()
    except:
        print('TEST PASSED: USER NO LONGER EXISTS')

    #Testing to verify a random image is selected from the pack folder... this will open (requires windows to work)
    try:
        os.system('start ' +p.packs_directory+p.pack_name+'/'+game_state.pack.pick_image())
    except:
        print('Either image does not exist or you are not on windows')
    #checking player insertion
    game_state.add_player('Rob')
    for player in game_state.players:
        game_state.players[player].print_attb()



def main():
    pass

if __name__ == "__main__":
    #test_pack()
    test_game()'''