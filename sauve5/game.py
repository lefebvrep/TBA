# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions
from character import Character
from item import Item

from config import DEBUG

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.characters = []   # liste de tous les PNJ du jeu

    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        # dans Game.setup() (exemple)
        take= Command("take", "Prendre un objet : take <item>", Actions.take, 1)
        self.commands["take"]=take
        # ⭐ Nouvelle commande : look
        look = Command("look", " : observer la pièce et voir ce qu'elle contient", Actions.look, 0)
        self.commands["look"] = look
        self.commands["drop"] = Command("drop"," : poser un objet de l'inventaire dans la pièce",Actions.drop,
    1)
        self.commands["check"] = Command("check"," : afficher l'inventaire du joueur",Actions.check,
    0)
        back = Command("back", " : revenir dans la pièce précédente", Actions.back, 0)
        self.commands["back"] = back

        drop = Command("drop"," : poser un objet de l'inventaire dans la pièce",Actions.drop,1)
        self.commands["drop"]=drop

        talk = Command("talk"," <nom> : parler à un personnage",Actions.talk,1)
        self.commands["talk"]=talk

       
        # Setup rooms

        forest = Room("Forest", " une forêt enchantée. Vous entendez une brise légère à travers la cime des arbres.")
        self.rooms.append(forest)
        tower = Room("Tower", " une immense tour en pierre qui s'élève au dessus des nuages.")
        self.rooms.append(tower)
        cave = Room("Cave", " une grotte profonde et sombre. Des voix semblent provenir des profondeurs.")
        self.rooms.append(cave)
        cottage = Room("Cottage", " un petit chalet pittoresque avec un toit de chaume. Une épaisse fumée verte sort de la cheminée.")
        self.rooms.append(cottage)
        swamp = Room("Swamp", " un marécage sombre et ténébreux. L'eau bouillonne, les abords sont vaseux.")
        self.rooms.append(swamp)
        castle = Room("Castle", " un énorme château fort avec des douves et un pont levis. Sur les tours, des flèches en or massif.")
        self.rooms.append(castle)

# ⭐ Ajout d'objets dans certaines pièces

        forest.inventory["shield"] = Item(
            "shield",
            "un bouclier léger et résistant",
            1
        )

        forest.inventory["helmet"] = Item(
            "helmet",
            "un casque en métal",
            1
        )

        cave.inventory["sword"] = Item(
            "sword",
            "une épée ancienne couverte de runes",
            3
        )

        cottage.inventory["potion"] = Item(
            "potion",
            "une petite fiole contenant un liquide lumineux",
            0.5
        )


        # Create exits for rooms

        forest.exits = {"N" : cave, "E" : tower, "S" : castle, "O" : None}
        tower.exits = {"N" : cottage, "E" : None, "S" : swamp, "O" : forest}
        cave.exits = {"N" : None, "E" : cottage, "S" : forest, "O" : None}
        cottage.exits = {"N" : None, "E" : None, "S" : tower, "O" : cave}
        swamp.exits = {"N" : tower, "E" : None, "S" : None, "O" : castle}
        castle.exits = {"N" : forest, "E" : swamp, "S" : None, "O" : None}
        # Setup characters (PNJ)

        guardian = Character("Gardien","un homme sévère en armure",forest,["Personne ne passe sans autorisation.", "Faites demi-tour."])
        witch = Character("Sorcière","une vieille femme au regard perçant",cottage,["Bienvenue, voyageur.", "Méfiez-vous du marécage."])
        gandalf = Character("Gandalf","un magicien blanc",forest,["Je suis Gandalf","Abracadabra !"])

        forest.characters["gardien"] = guardian
        cottage.characters["sorcière"] = witch
        forest.characters["gandalf"] = gandalf 
        self.characters.append(guardian)
        self.characters.append(witch)
        self.characters.append(gandalf)

        # Setup player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = swamp

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            cmd = input("> ")
            self.process_command(cmd)
            command_word = cmd.split(" ")[0] if cmd.strip() else ""
            if command_word not in ["look", "help", "check", "talk"]:
                moved = self.move_characters()
                if moved:
                    print("\n(Info) PNJ déplacés :", ", ".join(moved), "\n")
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if(len(command_word)==0):
            print("")
        elif command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
        room = self.player.current_room
        if room.characters:
            print("Personnages présents :")
            for c in room.characters.values():
                print(" -", c)

    def move_characters(self):
        moved = []
        for c in self.characters:
            if c.move():
                moved.append(c.name)
        return moved

    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
