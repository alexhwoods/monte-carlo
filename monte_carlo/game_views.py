from monte_carlo import app

@app.route('/test', methods=['GET'])
def test_method():
    return 'THIS IS A TEST'
