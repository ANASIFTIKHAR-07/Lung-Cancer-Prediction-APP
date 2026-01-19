from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from io import StringIO
import uvicorn
import joblib
import os

app = FastAPI(title="Lung Cancer Prediction API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globals
model = None
scaler = None
gene_selector = None
selected_genes = []

# Load files safely
try:
    model = joblib.load("random_forest_model.pkl")
    scaler = joblib.load("scaler.pkl")
    gene_selector = joblib.load("gene_selector.pkl")

    selected_genes_df = pd.read_csv("selected_genes.csv")
    selected_genes = (
        selected_genes_df.iloc[:, 0].tolist()
        if selected_genes_df.shape[1] == 1
        else selected_genes_df.columns.tolist()
    )

    print("✓ All model files loaded successfully")
    print(f"✓ Model: {type(model).__name__}")
    print(f"✓ Genes: {len(selected_genes)}")

except Exception as e:
    print("✗ FAILED TO LOAD MODEL FILES")
    print(e)

@app.get("/")
def read_root():
    return {
        "message": "Lung Cancer Prediction API",
        "status": "running",
    }

@app.get("/health")
def health_check():
    return {
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "gene_selector_loaded": gene_selector is not None,
        "num_genes": len(selected_genes),
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

        # Sample IDs handling
        if df.columns[0].startswith("TCGA") or df.columns[0] == "":
            sample_ids = df.iloc[:, 0].tolist()
            X = df.iloc[:, 1:].values
        else:
            sample_ids = [f"Sample_{i+1}" for i in range(len(df))]
            X = df.values

        # Gene selection
        if hasattr(gene_selector, "transform"):
            X = gene_selector.transform(X)

        # Scaling
        X = scaler.transform(X)

        preds = model.predict(X)
        probs = model.predict_proba(X)

        results = []
        for sid, p, pr in zip(sample_ids, preds, probs):
            results.append({
                "sample_id": sid,
                "prediction": "Tumor" if p == 1 else "Normal",
                "confidence": float(np.max(pr)),
                "tumor_probability": float(pr[1]),
                "normal_probability": float(pr[0]),
            })

        return {
            "success": True,
            "total_samples": len(results),
            "results": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
