import json

sid_list = ['005930']

with open('sid_list_test.json', 'w') as j:
    json.dump(sid_list, j)