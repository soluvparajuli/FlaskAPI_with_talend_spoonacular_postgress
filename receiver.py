import pika, sys, os
import requests
import json
import csv
from config import config
apikey=config.api_key



def main():
    connection = pika.BlockingConnection (pika.ConnectionParameters (host= 'localhost') )
    channel = connection. channel()
    channel.queue_declare ( queue="hello")
    def callback( ch, method, properties , body):
        name_of_ingredient = body.decode('utf-8')
        print(name_of_ingredient)
        def get_recipe_by_ingredient(name_of_ingredient):
            payload = {
                'ingredients':name_of_ingredient ,
                'number': 2,
                # can be changed according to required number of receipe we are getting only 2 receipe for now
                'ranking': 1  # ranking is done by system , I am unknown about the ranking
            }
            endpoint = "https://api.spoonacular.com/recipes/findByIngredients"
            headers = {
                'x-api-key': apikey
            }
            try:
                observation = requests.get(endpoint, params=payload, headers=headers)
                observation = observation.json()
                if len(observation) > 0:
                    return observation
                else:
                    pass
            except:
                print("Provide ingredient is not in our any receipe")

        input_for_json=get_recipe_by_ingredient(name_of_ingredient)
        if input_for_json is None:
            print("Invalid search")
            pass
        else:

            s = json.dumps(input_for_json)
            with open(".\jsonfiles\data1.json", 'w') as f:
                f.write(s)
            f = open('.\jsonfiles\data1.json')  # open a json file
            data = json.load(f)  # returns JSON object as a dictionary or mero case ma list ko rup ma aaherayeko xa as we have move inside the dictionary maybe or doctionary outerma theyena
            missed = "Missed"
            used = "Used"

            for obser in data:
                for missIngre in obser['missedIngredients']:
                    fieldnames = ['Search_Query', 'Recipe_id', 'title', 'usedIngredientCount', 'missedIngredientCount','ingredients_id', 'ingredients_name', 'aisle', 'MissedorUsed', 'amount', 'unit']
                    rows = [
                        {'Search_Query':name_of_ingredient,
                         'Recipe_id': obser['id'],
                         'title': obser['title'],
                         'usedIngredientCount': obser['usedIngredientCount'],
                         'missedIngredientCount': obser['missedIngredientCount'],
                         'ingredients_id': missIngre['id'],
                         'ingredients_name': missIngre['name'],
                         'aisle': missIngre['aisle'],
                         'MissedorUsed': missed,
                         'amount': missIngre['amount'],
                         'unit': missIngre['unit']
                         }
                    ]

                    with open('./csvfiles/Final.csv','r') as infocsv:
                        reader = [i for i in csv.DictReader(infocsv)]
                        if len(reader) > 0:
                            pass
                        else:
                            header = ['Search_Query', 'Recipe_id', 'title', 'usedIngredientCount', 'missedIngredientCount','ingredients_id', 'ingredients_name', 'aisle', 'MissedorUsed', 'amount', 'unit']
                            with open('./csvfiles/Final.csv', 'a', newline='') as f:
                                dw = csv.DictWriter(f, delimiter=',',fieldnames=header)
                                dw.writeheader()
                    with open('./csvfiles/Final.csv', 'a', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writerows(rows)

                for usedIngre in obser['usedIngredients']:
                    fieldnames = ['Search_Query', 'Recipe_id', 'title', 'usedIngredientCount', 'missedIngredientCount',
                                  'ingredients_id', 'ingredients_name', 'aisle', 'MissedorUsed', 'amount', 'unit']
                    rows = [
                        {'Search_Query': name_of_ingredient,
                         'Recipe_id': obser['id'],
                         'title': obser['title'],
                         'usedIngredientCount': obser['usedIngredientCount'],
                         'missedIngredientCount': obser['missedIngredientCount'],
                         'ingredients_id': usedIngre['id'],
                         'ingredients_name': usedIngre['name'],
                         'aisle': usedIngre['aisle'],
                         'MissedorUsed': used,
                         'amount': usedIngre['amount'],
                         'unit': usedIngre['unit']
                         }
                    ]
                    with open('./csvfiles/Final.csv', 'a', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writerows(rows)
            print(data)


    channel. basic_consume ( queue= "hello", on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for messages. To exit press CTRL+C ")
    channel. start_consuming ( )
if __name__ == '__main__':
    try:
        main ()
    except KeyboardInterrupt :
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit :
            os.exit(0)