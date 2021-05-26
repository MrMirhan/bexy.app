import json
with open("users/10001/openOrders.json") as json_data:
    nations = json.load(json_data)
nations_new = [x for x in nations if x['coin'] != "ADA"]
with open("users/10001/openOrders.json", 'w') as json_data:
    json.dump(nations_new, json_data, indent=2)