from datetime import datetime
from app.models.poids import Poids
from app.models.database import get_db
from app.core.core import LineareRegretion, SGDRegretions
from app.core.keras import KerasLLM, KerasMultiFeatureLLM
from app.models.result import ResulttLineareRegretion, RGDResult, KerasResultSimple, KerasResultMulti
import numpy as np

kerasllm = KerasLLM()
kerasmultiFeatureLLM = KerasMultiFeatureLLM()

session = next(get_db())

def convert(value):
    """Convertit les types numpy en types Python natifs."""
    if isinstance(value, (np.float32, np.float64)):
        return float(value,1)
    return value

def enter_data(actual_date, real_weight: float, measured_weight: float, tolerance: float):
    try:
        date_obj = datetime.strptime(actual_date.strip(), "%Y-%m-%d")
    except ValueError:
        return {'error': 'Date invalide. Format attendu: YYYY-MM-DD', 'data': None}

    error = abs(measured_weight - real_weight) * 1000  # en grammes

    poids = Poids(
        date=date_obj,
        real_weight=real_weight,
        measured_weight=measured_weight,
        tolerance=tolerance
    )
    session.add(poids)
    session.commit()

    # Prédictions des modèles
    predicted_dateLR, predicted_errorLR = LineareRegretion(tolerance)
    predicted_dataSGD, predicted_errorSGD = SGDRegretions(tolerance)
    date_kerasllm, err_kerasllm, current_errorllm = kerasllm.predict_date_tolerance_exceeded(
        measured_weight,
        real_weight,
        tolerance,
        date_obj,
    )    
    date_multi, err_multi = kerasmultiFeatureLLM.predict_date_tolerance_exceeded(
        real_weight,
        measured_weight,
        tolerance,
        date_obj,
    )

    # Sauvegarde résultats (optionnel - tu peux retirer si tu ne veux pas persister ici)
    if predicted_dateLR:
        session.add(ResulttLineareRegretion(
            predicted_date=predicted_dateLR.date(),
            predicted_error=predicted_errorLR,
            tolerance=tolerance,
        ))

    if predicted_dataSGD:
        session.add(RGDResult(
            predicted_date=predicted_dataSGD.date(),
            predicted_error=predicted_errorSGD,
            tolerance=tolerance,
        ))

    if date_kerasllm:
        session.add(KerasResultSimple(
            predicted_date=date_kerasllm,
            predicted_error=err_kerasllm,
            tolerance=tolerance,
        ))

    if date_multi:
        session.add(KerasResultMulti(
            predicted_date=date_multi,
            predicted_error=err_multi,
            tolerance=tolerance,
        ))

    session.commit()

    # Construire la réponse propre
    response = {
        'error': None,
        'data': {
            'current_error': convert(error),
            'linear_regression': {
                'date': predicted_dateLR.date().isoformat() if predicted_dateLR else None,
                'error': convert(predicted_errorLR),
            },
            'sgd_regression': {
                'date': predicted_dataSGD.date().isoformat() if predicted_dataSGD else None,
                'error': convert(predicted_errorSGD),
            },
            'keras_simple': {
                'date': date_kerasllm.isoformat() if date_kerasllm else None,
                'error': convert(err_kerasllm),
                'current_error': convert(current_errorllm),
            },
            'keras_multi': {
                'date': date_multi.isoformat() if date_multi else None,
                'error': convert(err_multi),
            }
        }
    }

    return response


data = enter_data("2025-05-16", 1.5, 1.6, 2.0)

print(data)