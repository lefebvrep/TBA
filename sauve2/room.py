# Define the Room class.

class Room:

    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        # --- Nouvel attribut : personnages présents dans la pièce ---
        # Dictionnaire : { "nom_personnage" : objet Character }
        self.characters = {}
        self.items = {}  # nom_item -> Item
       # --- Nouvel attribut : inventaire de la pièce ---
        # On utilise un dictionnaire vide : { "nom_objet": objet }
        self.inventory = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"
    
    # --- Nouvelle méthode : afficher le contenu de la pièce ---
    def get_inventory(self):
        if not self.inventory:
            return "Il n'y a rien ici."

        result = "La pièce contient :\n"
        for item_key, item in self.inventory.items():
            # On suppose que l'objet a les attributs name, description, weight
            result += f"    - {item_key} : {item.description} ({item.weight} kg)\n"
         # Affichage des personnages
        if not self.characters:
            result += "Il n'y a aucun personnage ici.\n"
        else:
            result += "Personnages présents :\n"
            for character in self.characters.values():
                result += f"    - {character}\n"
        return result
