# Define the Player class.
from config import DEBUG

class Player():
    
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.room_history = []     # Historique des salles visitées
        self.inventory = {}        # Inventaire du joueur (dict)
        self.max_weight = 10.0  # poids max transportable (à ajuster)


    def add_room(self, room):
        self.room_history.append(room)

    def move(self, direction):
        next_room = self.current_room.exits[direction]

        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        self.add_room(self.current_room)
        print(self.get_history())

        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True
    
    def print_room_history(self):
        print("\nHistorique des salles visitées :")
        if not self.room_history:
            print("  (aucune salle)")
        else:
            for i, room in enumerate(self.room_history, 1):
                print(f"{i:2} - {room.name}")

    def get_history(self):
        if not self.room_history:
            return "Aucune pièce visitée pour l'instant."

        result = "Historique des pièces visitées :\n"
        for i, room in enumerate(self.room_history, 1):
            result += f"{i}. {room.name}\n"

        return result.strip()

    def get_inventory(self):
        """Retourne une chaîne décrivant le contenu de l'inventaire du joueur."""
        if not self.inventory:
            return "Votre inventaire est vide."
        
        result = "Vous disposez des items suivants :\n"
        for name, item in self.inventory.items():
            result += f"    - {name} : {item.description} ({item.weight} kg)\n"

        return result.strip()
    
    def check(self) -> bool:
        """Affiche l'inventaire du joueur."""
        print(self.get_inventory())
        print(f"Poids total : {self.get_total_weight():.2f} kg / {self.max_weight:.2f} kg")
        return True
    
    def get_total_weight(self) -> float:
        """Retourne le poids total des objets dans l'inventaire."""
        total = 0.0
        for item in self.inventory.values():
            total += item.weight
        return total
    
    def take(self, item_key: str) -> bool:
        """Prend un item de la pièce courante et le met dans l'inventaire du joueur
        si le poids total ne dépasse pas max_weight.
        """
        if DEBUG:
            print(f"DEBUG: tentative de prise de {item_key}")
        if self.current_room is None:
            print("\nVous n'êtes dans aucune pièce.\n")
            return False

        room = self.current_room
        key = item_key.strip()

        if key not in room.inventory:
            print(f"\nIl n'y a pas '{key}' dans cette pièce.\n")
            return False

        item = room.inventory[key]  # on regarde l'objet sans le retirer tout de suite

        current_weight = self.get_total_weight()
        new_weight = current_weight + item.weight

        if new_weight > self.max_weight:
            print(
                f"\nImpossible de prendre '{key}' : trop lourd.\n"
                f"Poids actuel : {current_weight:.2f} kg / {self.max_weight:.2f} kg\n"
                f"Poids de l'objet : {item.weight:.2f} kg\n"
            )
            return False

        # Transfert pièce -> joueur (ok)
        item = room.inventory.pop(key)
        self.inventory[key] = item
        print(f"\nVous avez pris : {key}\n")
        return True
    
    def drop(self, item_key: str) -> bool:
        """
        Dépose un item de l'inventaire du joueur dans la pièce courante.
        Usage attendu : drop <nom_item>
        """
        if self.current_room is None:
            print("\nVous n'êtes dans aucune pièce.\n")
            return False

        key = item_key.strip()

        if key not in self.inventory:
            print(f"\nVous n'avez pas '{key}' dans votre inventaire.\n")
            return False

    # Transfert joueur -> pièce
        item = self.inventory.pop(key)
        self.current_room.inventory[key] = item

        print(f"\nVous avez posé : {key}\n")
        return True





