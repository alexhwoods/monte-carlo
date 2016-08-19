from monte_carlo.components.models.Player import Player


players = {}


def create(name, chips):
    player = Player(name, chips)
    players[player.id] = player
    return player


def getByID(id):
    if id in players.keys():
        return players[id]
    else:
        return None




