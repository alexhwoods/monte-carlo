import json

with open('config.json', 'r') as f:
    config = json.load(f)

#edit the data
config['user_id'] = 'user_id_goes_here'

#write it back to the file
with open('config.json', 'w') as f:
    json.dump(config, f)