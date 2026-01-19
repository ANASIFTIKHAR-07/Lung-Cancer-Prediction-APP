import pandas as pd
import joblib

print("Creating demo samples...")

# Load scaler
scaler = joblib.load('models/scaler.pkl')

# Read selected genes (skip header if exists)
genes_df = pd.read_csv('models/selected_genes.txt', header=None)
selected_genes = genes_df[0].tolist()

# Remove 'gene' if it's the header
if selected_genes[0] == 'gene':
    selected_genes = selected_genes[1:]

print(f"Loaded {len(selected_genes)} genes")

# Load data
expr = pd.read_csv('TCGA-LUAD.star_fpkm-uq.tsv', sep='\t', index_col=0)
clinical = pd.read_csv('TCGA-LUAD.clinical.tsv', sep='\t')

# Transpose
X = expr.T

# Find sample type column
sample_col = None
for col in clinical.columns:
    if 'sample_type' in col.lower():
        sample_col = col
        break

print(f"Using sample type column: {sample_col}")

# Create labels (using numeric codes)
labels = {}
for _, row in clinical.iterrows():
    sid = str(row.iloc[0])[:15]
    stype = row[sample_col]  # This is a number!
    for sample in X.index:
        if sid in sample:
            if stype == 1 or stype == 2:  # 1=Primary Tumor, 2=Recurrent Tumor
                labels[sample] = 1
            elif stype == 11:  # 11=Solid Tissue Normal
                labels[sample] = 0
print(f"Found {sum(1 for v in labels.values() if v == 1)} tumor, {sum(1 for v in labels.values() if v == 0)} normal")

# Get labeled samples
labeled_samples = list(labels.keys())
X_labeled = X.loc[labeled_samples]

# Select only the genes that exist in both
available_genes = [g for g in selected_genes if g in X_labeled.columns]
print(f"Using {len(available_genes)} available genes")

X_selected = X_labeled[available_genes]

# Scale
X_scaled = pd.DataFrame(
    scaler.transform(X_selected), 
    columns=available_genes, 
    index=X_selected.index
)

# Get samples
tumor_samples = [s for s, l in labels.items() if l == 1]
normal_samples = [s for s, l in labels.items() if l == 0]

# Select 5 of each
demo_tumor = X_scaled.loc[tumor_samples[:5]]
demo_normal = X_scaled.loc[normal_samples[:5]]
demo = pd.concat([demo_tumor, demo_normal])

# Save
demo.to_csv('models/demo_samples.csv')

print(f"\n✓ SUCCESS!")
print(f"Created {len(demo)} demo samples")
print(f"  Tumor: {len(demo_tumor)}")
print(f"  Normal: {len(demo_normal)}")
print(f"Saved to: models/demo_samples.csv")