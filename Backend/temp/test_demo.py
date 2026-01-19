import joblib
import pandas as pd

print("Testing demo samples...\n")

# Load models
rf = joblib.load('models/random_forest_model.pkl')
svm = joblib.load('models/svm_model.pkl')
demo = pd.read_csv('models/demo_samples.csv', index_col=0)

print(f"✓ Loaded {len(demo)} demo samples\n")

# Test first 3 samples
for i in range(min(3, len(demo))):
    sample = demo.iloc[i:i+1]
    sample_id = sample.index[0]
    
    # RF prediction
    rf_pred = rf.predict(sample)[0]
    rf_conf = rf.predict_proba(sample)[0]
    
    print(f"{i+1}. Sample: {sample_id}")
    print(f"   RF Prediction: {'🔴 Tumor' if rf_pred == 1 else '🟢 Normal'}")
    print(f"   Confidence: {max(rf_conf)*100:.2f}%")
    print()

print(" Everything works! Demo samples are ready!")