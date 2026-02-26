from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field, validator

class SinglePredictionRequest(BaseModel):
    date: str = Field(..., description="Date au format YYYY-MM-DD")
    poids_attendu: float = Field(..., gt=0, description="Poids attendu en kg")
    poids_mesure: float = Field(..., gt=0, description="Poids mesuré en kg")
    
    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date doit être au format YYYY-MM-DD")
    
    @validator('poids_mesure')
    def validate_weight_difference(cls, v, values):
        if 'poids_attendu' in values:
            diff = abs(values['poids_attendu'] - v)
            if diff > 1.0:
                raise ValueError("Différence entre les poids trop importante (> 1kg)")
        return v


class BatchPredictionRequest(BaseModel):
    start_date: str
    end_date: str
    poids_attendu: float = Field(..., gt=0)
    poids_mesure: float = Field(..., gt=0)
    
    @validator('start_date', 'end_date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date doit être au format YYYY-MM-DD")
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        if 'start_date' in values:
            start = datetime.strptime(values['start_date'], '%Y-%m-%d')
            end = datetime.strptime(v, '%Y-%m-%d')
            
            if end < start:
                raise ValueError("end_date doit être après start_date")
            
            if (end - start).days > 365:
                raise ValueError("La plage ne peut pas dépasser 365 jours")
        return v


class ToleranceBreachRequest(BaseModel):
    tolerance_g: float = Field(..., gt=0)
    start_date: str
    poids_attendu: float = Field(..., gt=0)
    poids_mesure: float = Field(..., gt=0)
    days_limit: int = Field(365, ge=1, le=365)
    
    @validator('start_date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError("Date doit être au format YYYY-MM-DD")



class RetrainRequest(BaseModel):
    model: Literal["weight", "drift", "both"] = "both"

