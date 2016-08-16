from monte_carlo import app
from monte_carlo.components.models import Game

games = []


@app.route('/test', methods=['GET'])
def test_method():
    return 'THIS IS A TEST'


@app.route('/start-game', methods=['POST'])
def create_game():
    game = Game()
    games.append(game)
    return game


