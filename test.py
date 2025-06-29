import json
from time import sleep
from app.models import poids, database
from app.db.crud import Difter
from datetime import datetime
difter = Difter(next(database.get_db()))

with open('data.json','r') as file:
    data = json.load(file)

for key, values in data.items():
    for value in values:
        poid = poids.Poids(
            date = datetime.strptime(key,"%Y-%m-%d"),
            real_weight =20,
            measured_weight = value,tolerance=0.02
        )
        difter.add(poid=poid)
        response =  difter.commiting(poid=poid)
        print(f'{key}: data {value} as set in db' if response else f'{key}: data {value} as not  set in db')