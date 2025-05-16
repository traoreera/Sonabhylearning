from datetime import datetime
from app.models.poids import Poids
from app.models.database import get_db
from app.models.example import inserer_donnees_exemple
from app.core.core import LineareRegretion,SGDRegretions
from app.core.keras import KerasLLM, KerasMultiFeatureLLM
from app.models.result import ResulttLineareRegretion, RGDResult, KerasResultSimple, KerasResultMulti


kerasllm = KerasLLM()
kerasmultiFeatureLLM = KerasMultiFeatureLLM()



session = next(get_db())

inserer_donnees_exemple()


def enter_data():
    try:
        date_input = input("Entrez la date (YYYY-MM-DD) : ").strip()
        date_obj = datetime.strptime(date_input, "%Y-%m-%d")
        real_weight = float(input("Entrez le poids réel (kg) : "))
        measured_weight = float(input("Entrez le poids mesuré (kg) : "))
        tolerance = float(input("Entrez la tolérance (g) : "))
    except ValueError:
        print("❌ Entrée invalide. Réessayez.")
        return

    error = abs(measured_weight - real_weight) * 1000  # en grammes

    poids = Poids(
        date=date_obj,
        real_weight=real_weight,
        measured_weight=measured_weight,
        tolerance=tolerance
    )
    session.add(poids)
    session.commit()
    print(f"📏 Erreur calculée : {error:.2f} g")

    predicted_dateLR, predicted_errorLR = LineareRegretion(tolerance)
    predicted_dataSGD, predicted_errorSGD = SGDRegretions(tolerance)
    date_kerasllm, err_kerasllm, current_errorllm = kerasllm.predict_date_tolerance_exceeded(
        measured_weight,
        real_weight,
        tolerance,
        date_obj,
        )    
    if predicted_dateLR:
        print(f"🔮 Date estimée de dépassement de tolérance LR: {predicted_dateLR.date()}")
        print(f"📉 Erreur prédite ce jour-là LR: {predicted_errorLR:.2f} g")
        
        result = ResulttLineareRegretion(
            predicted_date=predicted_dateLR.date(),
            predicted_error=predicted_errorLR,
            tolerance=tolerance,
        )
        session.add(result)
    if predicted_dataSGD:
        print(f"🔮 Date estimée de dépassement de tolérance SGD: {predicted_dataSGD.date()}")
        print(f"📉 Erreur prédite ce jour-là SGD: {predicted_errorSGD:.2f} g")
        
        result = RGDResult(
            predicted_date=predicted_dataSGD.date(),
            predicted_error=predicted_errorSGD,
            tolerance=tolerance,
        )
        session.add(result)
    
        session.commit()

    date_multi, err_multi = kerasmultiFeatureLLM.predict_date_tolerance_exceeded(
        real_weight,
        measured_weight,
        tolerance,
        date_obj,
    )
    
    
    if date_kerasllm:
        print(f"🔮 Dépassement Keras (simple): {date_kerasllm.strftime('%Y-%m-%d')} | Erreur prédite : {err_kerasllm:.2f} g | Erreur actuelle : {current_errorllm:.2f} g")
        simple_result = KerasResultSimple(
            predicted_date= date_multi,
            predicted_error= err_multi,
            tolerance = tolerance
        )
        session.add(simple_result)
        session.commit()
    else:
        print("🔮 Keras simple : Aucun dépassement prévu dans la plage analysée")

    if date_multi:
        print(f"🔮 Dépassement Keras (multi): {date_multi.strftime('%Y-%m-%d')} | Erreur prédite : {err_multi:.2f} g")
        multi_result = KerasResultMulti(
            predicted_date= date_kerasllm,
            predicted_error= err_kerasllm,
            tolerance = tolerance
        )
        session.add(multi_result)
        session.commit()

    else:
        print("🔮 Keras multi : Aucun dépassement prévu dans la plage analysée")
enter_data()