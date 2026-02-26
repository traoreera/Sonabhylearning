from sqlalchemy.orm import Session
from app.models import RGDResult,KerasResultMulti, KerasResultSimple, ResulttLineareRegretion, Poids





class ModelsCRUD:
    def __init__(self, session:Session):
        self.session = session
    
    
    def resultRDG(self,):
        response = self.session.query(RGDResult).all()
        errorRGD = [f'{i.predicted_error:.1f}' for i in response ]
        dataRGD = [i.predicted_date for i in response ]
        return errorRGD, dataRGD
    
    def resultLR(self,):
        response = self.session.query(ResulttLineareRegretion).all()
        errorLR = [f'{i.predicted_error:.1f}' for i in response]
        dataLR = [i.predicted_date for i in response]
        return errorLR, dataLR
    
    def resultKeras(self,):
        response = self.session.query(KerasResultSimple).all()
        
        errorSGD = [f'{i.predicted_error:.1f}' for i in response]
        dataSGD = [i.predicted_date for i in response]
        
        return errorSGD, dataSGD
    
    def resultKerasM(self,):
        response = self.session.query(KerasResultMulti).all()
        
        error =[f'{i.predicted_error:.1f}' for i in response ]
        dataM = [i.predicted_date for i in response]
        
        return error, dataM

class Difter:
    
    def __init__(self, session: Session):
        
        self.session = session
    
    
    def add(self,poid:Poids):
        self.session.add(poid)
        return poid
    
    def get_alls(self):
        return [i.responseModels() for i in self.session.query(Poids).all()]
    
    
    def commiting(self,poid: Poids):
        try:
            self.session.commit()
            self.session.refresh(poid)
            return True
        except Exception as e : 
            self.session.rollback()
            print(e)