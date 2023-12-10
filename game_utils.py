import os
import random

class card:
    def __init__(self):
        self.title = '' #Card text
        self.type = '' #Either Prompt or Response

class player:
    def __init__(self,username):
        self.hand = []
        self.score = 0
        self.username = username
    
    def print_attb(self):
        print(f'username = {self.username}\n hand = {self.hand} \n score = {self.score}\n')
    
    def add_card(self):
        pass

class deck:
    def __init__(self) -> None:
        pass

class pack:
    def __init__(self,pack='default'):
        self.packs_directory = './static/images/packs/'
        self.pack_name = pack
        self.deck = os.listdir(self.packs_directory+pack)
    
    def pick_image(self):
        image = random.randint(0,len(self.deck)-1)
        img_url = self.deck[image]
        del self.deck[image]
        return img_url



class game:
    def __init__(self,pack,max_player_count,rounds):
        self.players = {}
        self.pack = pack
        self.player_count = 0
        self.max_players = max_player_count
        self.host = ''
        self.rounds = rounds
        self.state = 'Lobby'
    
    def start_game(self):
        pass

    def deal_cards(self):
        pass

    #Adds a player to the dictionary of player. The key is the number they joined in and the value is their username
    def add_player(self,username):
        if(self.player_count < self.max_players and self.players.get(username,'')==''):
            if(len(self.players)==0):
                self.host = username
            self.players[username] = player(username) 
            self.player_count += 1
        else:
            print('Error, Game is no longer accepting players. Max players have been reached or user already in game')

    #Removes a player based on their player number
    def remove_player(self,username):
        if(username == self.host or len(self.players)<=1 or self.player_count<=1):
            print('error, lobby empty, need to delete the lobby now')
        else:
            del self.players[username]
            self.player_count -= 1

def test_pack():
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
    test_game()