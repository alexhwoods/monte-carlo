from monte_carlo.components.models.Player import Player
import uuid


players = []


def create(name, chips):
    player = Player(name, chips)
    players.append(player)


def getByID(id):
    for player in players:
        if player.id == id:
            return player
    return None




