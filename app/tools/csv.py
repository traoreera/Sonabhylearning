from time import sleep
import pandas as pd
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.db.crud import Difter
from app.database import get_db
from app.models import Poids

class CSVTools:
    
    def __init__(self, file:str):
        try:
            self.session=next(get_db())
            self.differ = Difter(self.session)
            self.df = pd.read_csv(file)
        except:
            raise FileNotFoundError("File not found")
    
    
    def importCSV(self):
        try:
            for _, row in self.df.iterrows():  
                p = Poids(
                    date=datetime.strptime(row['date'], '%Y-%m-%d'),
                    real_weight=row['real_weight'],
                    measured_weight=row['measured_weight'],
                    tolerance=row['tolerance']
                )
                print(f"Imported {row['date']} with real weight {row['real_weight']} and measured weight {row['measured_weight']}")
                self.session.add(p)
                self.session.commit()
                sleep(0.1)
        except Exception as e:
            print(e)