from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import numpy as np
from io import StringIO
import uvicorn

app = FastAPI(title="Lung Cancer Prediction API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model and preprocessing files
try:
    with open('best_luad_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    with open('selected_genes.pkl', 'rb') as f:
        selected_genes = pickle.load(f)
    
    print("✓ Model and preprocessing files loaded successfully")
except Exception as e:
    print(f"✗ Error loading files: {e}")
    print("Make sure best_luad_model.pkl, scaler.pkl, and selected_genes.pkl are in the backend folder")

@app.get("/")
def read_root():
    return {
        "message": "Lung Cancer Prediction API",
        "status": "running",
        "endpoints": {
            "predict": "/predict (POST - upload CSV file)",
            "health": "/health (GET)"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read the uploaded CSV file
        contents = await file.read()
        csv_data = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        # Extract sample IDs if present
        if csv_data.columns[0] == '' or 'TCGA' in str(csv_data.iloc[0, 0]):
            sample_ids = csv_data.iloc[:, 0].tolist()
            X = csv_data.iloc[:, 1:].values
        else:
            sample_ids = [f"Sample_{i+1}" for i in range(len(csv_data))]
            X = csv_data.values
        
        # Ensure we have the right number of features
        if X.shape[1] != len(selected_genes):
            raise HTTPException(
                status_code=400,
                detail=f"Expected {len(selected_genes)} genes, but got {X.shape[1]}"
            )
        
        # Scale the data
        X_scaled = scaler.transform(X)
        
        # Make predictions
        predictions = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)
        
        # Prepare results
        results = []
        for i, (sample_id, pred, prob) in enumerate(zip(sample_ids, predictions, probabilities)):
            results.append({
                "sample_id": sample_id,
                "prediction": "Tumor" if pred == 1 else "Normal",
                "confidence": float(max(prob)),
                "tumor_probability": float(prob[1]),
                "normal_probability": float(prob[0])
            })
        
        return {
            "success": True,
            "total_samples": len(results),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)