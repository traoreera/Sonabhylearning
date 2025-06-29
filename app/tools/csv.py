import pandas as pd
from app.db.crud import Difter
from app.models.database import get_db
from app.models.poids import Poids

differ = Difter(next(get_db()))

class CSVTools:
    
    def __init__(self, file:str):
        
        try:
            self.df = pd.read_csv(file)
        except:
            raise 'file as been not read ...'
    
    
    def importCSV(self):
        try:
            for column, row in self.df.iterrows():
                date = float(row['date'])
                real_weight = float(row['real_weight'])
                mesured_weight = row['measured_weight']
                tolerance = row['tolerance']
                poids = Poids(date=date, real_weight=real_weight, measured_weight=mesured_weight, tolerance=tolerance)
                differ.add(poids)
            differ.commiting(poids)
            return True
        except Exception as e :
            differ.session.rollback()
            return False, e