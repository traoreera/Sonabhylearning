import shutil
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import numpy as np
from microframe.engine import TemplateEngine
from app.tools.csv import CSVTools

# ==================== MODÈLES PYDANTIC ====================
from app.schemas import SinglePredictionRequest, BatchPredictionRequest, ToleranceBreachRequest, RetrainRequest

# Importer vos modèles
from app.IA import DriftRegressor, WeightErrorRegressor




# Initialiser FastAPI
app = FastAPI(
    title="API de Prédiction de Dérive de Poids",
    description="API pour prédire les erreurs de mesure de poids",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = TemplateEngine(directory="./templates",)



# Initialiser les modèles au démarrage
weight_model = None
drift_model = None

@app.on_event("startup")
async def load_models():
    global weight_model, drift_model
    try:
        weight_model = WeightErrorRegressor()
        drift_model = DriftRegressor(model_type="sgd", tolerance=100, model_dir="models")
        print("✅ Modèles chargés avec succès")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des modèles: {e}")



# ==================== ROUTES HTML ====================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Page d'accueil avec l'interface de prédiction"""
    return await templates.render("index.html",request=request)


@app.get("/docs-page", response_class=HTMLResponse)
async def docs_page(request: Request):
    """Page de documentation"""
    return await templates.render("docs.html", {"request": request})


@app.get('/load-data', response_class=HTMLResponse)
async def load_data(request: Request):
    return await templates.render("load_data.html", {"request": request})




# ==================== ROUTES API ====================

@app.get("/api/health")
async def health_check():
    """Vérifier l'état de santé du service"""
    return {
        "status": "healthy" if (weight_model and drift_model) else "degraded",
        "models": {
            "weight_model": weight_model is not None,
            "drift_model": drift_model is not None
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/models/info")
async def models_info():
    """Obtenir les informations sur les modèles"""
    info = {
        "weight_model": {
            "loaded": weight_model is not None,
            "type": "Neural Network (WeightErrorRegressor)",
        },
        "drift_model": {
            "loaded": drift_model is not None,
            "type": drift_model.model_type.upper() if drift_model else None,
        }
    }
    
    if weight_model:
        metrics = weight_model.evaluate()
        info["weight_model"]["metrics"] = metrics
        info["weight_model"]["dataset_size"] = len(weight_model.records)
    
    if drift_model:
        metrics = drift_model.evaluate()
        info["drift_model"]["metrics"] = metrics
        info["drift_model"]["dataset_size"] = len(drift_model.errors) if drift_model.errors is not None else 0
        info["drift_model"]["tolerance"] = drift_model.tolerance
    
    return info


@app.post("/api/predictions/single")
async def predict_single(request: SinglePredictionRequest):
    """Prédire l'erreur pour une date et des poids spécifiques"""
    if weight_model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    try:
        date = datetime.strptime(request.date, '%Y-%m-%d')
        predicted_error = weight_model.predict(date, request.poids_attendu, request.poids_mesure)
        current_error = abs(request.poids_attendu - request.poids_mesure) * 1000
        
        # Déterminer le statut
        if predicted_error < 50:
            status, severity = "OK", "success"
        elif predicted_error < 100:
            status, severity = "Attention", "warning"
        else:
            status, severity = "Critique", "error"
        
        return {
            "success": True,
            "date": request.date,
            "poids_attendu": request.poids_attendu,
            "poids_mesure": request.poids_mesure,
            "current_error_g": round(current_error, 2),
            "predicted_error_g": round(predicted_error, 2),
            "difference_g": round(predicted_error - current_error, 2),
            "status": status,
            "severity": severity,
            "days_from_now": (date - datetime.now()).days
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predictions/batch")
async def predict_batch(request: BatchPredictionRequest):
    """Prédire l'erreur sur une plage de dates"""
    if weight_model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    try:
        start_date = datetime.strptime(request.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(request.end_date, '%Y-%m-%d')
        days_diff = (end_date - start_date).days
        
        # Générer les dates
        dates = [start_date + timedelta(days=i) for i in range(days_diff + 1)]
        poids_attendus = [request.poids_attendu] * len(dates)
        poids_mesures = [request.poids_mesure] * len(dates)
        
        # Prédiction par lot
        predictions = weight_model.predict_batch(dates, poids_attendus, poids_mesures)
        
        # Construire les résultats
        results = []
        for i, (date, error) in enumerate(zip(dates, predictions)):
            if error < 50:
                status, severity = "OK", "success"
            elif error < 100:
                status, severity = "Attention", "warning"
            else:
                status, severity = "Critique", "error"
            
            results.append({
                "date": date.strftime('%Y-%m-%d'),
                "poids_attendu": request.poids_attendu,
                "poids_mesure": request.poids_mesure,
                "predicted_error_g": round(float(error), 2),
                "status": status,
                "severity": severity,
                "day_index": i
            })
        
        # Statistiques
        errors = [r['predicted_error_g'] for r in results]
        stats = {
            "total_predictions": len(results),
            "avg_error_g": round(float(np.mean(errors)), 2),
            "max_error_g": round(float(np.max(errors)), 2),
            "min_error_g": round(float(np.min(errors)), 2),
            "std_error_g": round(float(np.std(errors)), 2),
            "ok_count": sum(1 for r in results if r['severity'] == 'success'),
            "warning_count": sum(1 for r in results if r['severity'] == 'warning'),
            "error_count": sum(1 for r in results if r['severity'] == 'error')
        }
        
        return {
            "success": True,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "statistics": stats,
            "predictions": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predictions/tolerance-breach")
async def tolerance_breach(request: ToleranceBreachRequest):
    """Trouver quand l'erreur dépassera la tolérance"""
    if weight_model is None:
        raise HTTPException(status_code=503, detail="Modèle non disponible")
    
    try:
        start_date = datetime.strptime(request.start_date, '%Y-%m-%d')
        
        breach_date = weight_model.predict_tolerance_breach(
            request.tolerance_g, start_date, 
            request.poids_attendu, request.poids_mesure, 
            request.days_limit
        )
        
        if breach_date:
            days_until = (breach_date - datetime.now()).days
            predicted_error = weight_model.predict(breach_date, request.poids_attendu, request.poids_mesure)
            
            urgency = "urgent" if days_until <= 7 else "attention" if days_until <= 30 else "normal"
            
            return {
                "success": True,
                "breach_detected": True,
                "breach_date": breach_date.strftime('%Y-%m-%d'),
                "days_until_breach": days_until,
                "predicted_error_g": round(predicted_error, 2),
                "tolerance_g": request.tolerance_g,
                "urgency": urgency
            }
        else:
            return {
                "success": True,
                "breach_detected": False,
                "message": f"Aucun dépassement prévu dans les {request.days_limit} prochains jours",
                "tolerance_g": request.tolerance_g
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/predictions/drift-analysis")
async def drift_analysis(tolerance: float = 100):
    """Obtenir l'analyse complète de la dérive"""
    if drift_model is None:
        raise HTTPException(status_code=503, detail="Modèle de dérive non disponible")
    
    try:
        drift_model.refresh_data()
        summary ="drif model "
        drift_rate_g_per_day = drift_model.evaluate()['drift_rate_kg_per_day'] if drift_model else None
        
        return {
            "success": True,
            "drift_summary": summary,
            "drift_rate_g_per_day": drift_rate_g_per_day,
            "breach_date": drift_model.get_date_tolerance_breach(),
            "days_until_breach": len(drift_model.errors) if drift_model.errors is not None else 0
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predictions/retrain")
async def retrain_models(request: RetrainRequest = RetrainRequest()):
    """Réentraîner les modèles avec les dernières données"""
    results = {}
    
    if request.model in ['weight', 'both']:
        if weight_model is None:
            results['weight'] = {"success": False, "error": "Modèle non disponible"}
        else:
            try:
                weight_model.retrain()
                metrics = weight_model.evaluate()
                results['weight'] = {
                    "success": True,
                    "metrics": metrics,
                    "message": "Modèle de prédiction d'erreur réentraîné"
                }
            except Exception as e:
                results['weight'] = {"success": False, "error": str(e)}
    
    if request.model in ['drift', 'both']:
        if drift_model is None:
            results['drift'] = {"success": False, "error": "Modèle non disponible"}
        else:
            try:
                success = drift_model.train()
                weight_model.retrain() # type: ignore
                if success:
                    metrics = drift_model.evaluate()
                    results['drift'] = {
                        "success": True,
                        "metrics": metrics,
                        "message": "Modèle de dérive réentraîné"
                    }
                else:
                    results['drift'] = {"success": False, "error": "Échec du réentraînement"}
            except Exception as e:
                results['drift'] = {"success": False, "error": str(e)}
    
    return {"success": True, "results": results}



@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Le fichier doit être un CSV")

    # Chemin temporaire
    save_path = f"./downloads/{file.filename}"

    try:
        # Sauvegarde du fichier
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Lecture / Import DB
        csv = CSVTools(file=save_path)
        success = csv.importCSV()

        return {
            "filename": file.filename,
            "status": "success" if success else "failed",
            "message": "CSV importé avec succès" if success else "Erreur lors de l'import"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {e}")


# ==================== LANCER L'APPLICATION ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)