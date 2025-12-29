# character.py
# Classe Character : représente un personnage non joueur (PNJ)
from config import DEBUG

class Character:
    """
    Cette classe représente un personnage non joueur.

    Attributs :
        name (str)         : nom du personnage
        description (str)  : description du personnage
        current_room (Room): pièce où se trouve le personnage
        msgs (list[str])   : messages prononcés par le personnage
    """

    def __init__(self, name, description, current_room=None, msgs=None):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs if msgs is not None else []

    def get_description(self):
        """Retourne la description du personnage."""
        return f"{self.name} : {self.description}"

    def speak(self):
        """
        Retourne les messages du personnage.
        S'il n'a rien à dire, retourne un message par défaut.
        """
        if not self.msgs:
            return f"{self.name} n'a rien à dire."
        
        result = f"{self.name} dit :\n"
        for msg in self.msgs:
            result += f"  - {msg}\n"
        return result.strip()
    
    def move(self) -> bool:
        import random

    # 1 chance sur 2 de rester sur place
        if random.choice([True, False]) is False:
            if DEBUG:
                print(f"DEBUG: {self.name} reste dans {self.current_room.name}")
            return False

    # Liste des pièces voisines accessibles
        voisins = []
        for room in self.current_room.exits.values():
            if room is not None:
                voisins.append(room)

        if not voisins:
            if DEBUG:
                print(f"DEBUG: {self.name} n'a aucune sortie")
            return False

        nouvelle_piece = random.choice(voisins)
        if DEBUG:
            print(f"DEBUG: {self.name} se déplace de {self.current_room.name} vers {nouvelle_piece.name}")
    # Retirer de l'ancienne pièce
        self.current_room.characters.pop(self.name)

    # Ajouter dans la nouvelle pièce
        nouvelle_piece.characters[self.name] = self

    # Mettre à jour la position
        self.current_room = nouvelle_piece

        return True

    
    def __str__(self):
        """Retourne une représentation textuelle du personnage."""
        return f"{self.name} : {self.description}"
