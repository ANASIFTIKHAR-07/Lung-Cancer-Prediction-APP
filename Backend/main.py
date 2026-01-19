from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import numpy as np
from io import StringIO
import uvicorn
import joblib
import os

# --------------------
# Initialize FastAPI
# --------------------
app = FastAPI(title="Lung Cancer Prediction API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Globals
# --------------------
model = None
scaler = None
gene_selector = None
selected_genes = []

# --------------------
# Helper function
# --------------------
def check_model_loaded():
    if model is None or scaler is None or gene_selector is None:
        raise HTTPException(status_code=500, detail="Model files not loaded")

# --------------------
# Load model files safely
# --------------------
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

# --------------------
# Root & Health Check
# --------------------
@app.get("/")
def read_root():
    return {"message": "Lung Cancer Prediction API", "status": "running"}

@app.get("/health")
def health_check():
    return {
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "gene_selector_loaded": gene_selector is not None,
        "num_genes": len(selected_genes),
    }

# --------------------
# Predict from uploaded CSV
# --------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    check_model_loaded()
    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

        if df.columns[0].startswith("TCGA") or df.columns[0] == "":
            sample_ids = df.iloc[:, 0].tolist()
            X = df.iloc[:, 1:].values
        else:
            sample_ids = [f"Sample_{i+1}" for i in range(len(df))]
            X = df.values

        # Adjust X if smaller demo CSV
        if X.shape[1] != len(selected_genes):
            # keep only columns in selected_genes if present
            X_df = pd.DataFrame(X, columns=df.columns)
            missing_cols = set(selected_genes) - set(X_df.columns)
            for c in missing_cols:
                X_df[c] = 0  # fill missing features with 0
            X_df = X_df[selected_genes]
            X = X_df.values

        X = gene_selector.transform(X)
        X = scaler.transform(X)

        preds = model.predict(X)
        probs = model.predict_proba(X)

        results = [
            {
                "sample_id": sid,
                "prediction": "Tumor" if p == 1 else "Normal",
                "confidence": float(np.max(pr)),
                "tumor_probability": float(pr[1]),
                "normal_probability": float(pr[0]),
            }
            for sid, p, pr in zip(sample_ids, preds, probs)
        ]

        return {"success": True, "total_samples": len(results), "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------
# Demo prediction endpoint
# --------------------
@app.get("/demo_predict")
def demo_predict():
    check_model_loaded()
    demo_path = os.path.join(os.path.dirname(__file__), "temp", "models", "demo_samples.csv")
    if not os.path.exists(demo_path):
        raise HTTPException(status_code=404, detail="Demo CSV not found")

    try:
        df = pd.read_csv(demo_path)
        sample_ids = [f"Sample_{i+1}" for i in range(len(df))]
        X = df.values

        # Adjust for missing columns like above
        if X.shape[1] != len(selected_genes):
            X_df = pd.DataFrame(X, columns=df.columns)
            missing_cols = set(selected_genes) - set(X_df.columns)
            for c in missing_cols:
                X_df[c] = 0
            X_df = X_df[selected_genes]
            X = X_df.values

        X = gene_selector.transform(X)
        X = scaler.transform(X)

        preds = model.predict(X)
        probs = model.predict_proba(X)

        results = [
            {
                "sample_id": sid,
                "prediction": "Tumor" if p == 1 else "Normal",
                "confidence": float(np.max(pr)),
                "tumor_probability": float(pr[1]),
                "normal_probability": float(pr[0]),
            }
            for sid, p, pr in zip(sample_ids, preds, probs)
        ]

        return {"success": True, "total_samples": len(results), "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------------------
# Optional: Download demo CSV
# --------------------
@app.get("/demo_download")
def demo_download():
    demo_path = os.path.join(os.path.dirname(__file__), "temp", "demo_samples.csv")
    if not os.path.exists(demo_path):
        raise HTTPException(status_code=404, detail="Demo CSV not found")
    return FileResponse(demo_path, media_type="text/csv", filename="demo_samples.csv")

# --------------------
# Run server
# --------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
