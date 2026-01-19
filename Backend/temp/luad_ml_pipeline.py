"""
TCGA-LUAD Machine Learning Pipeline
Purpose: Tumor vs Normal Classification using Gene Expression Data

This code implements best practices to avoid:
- Data leakage
- Overfitting
- Class imbalance issues
- Feature selection bias
- Incorrect preprocessing order
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import os
import joblib

# Machine Learning
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    roc_curve, accuracy_score, precision_score, recall_score, 
    f1_score, make_scorer
)
from sklearn.decomposition import PCA

# Imbalanced learning
try:
    from imblearn.over_sampling import SMOTE
    SMOTE_AVAILABLE = True
except ImportError:
    print("WARNING: imbalanced-learn not installed. Install with: pip install imbalanced-learn")
    SMOTE_AVAILABLE = False

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-darkgrid')

# Create output directories
os.makedirs('models', exist_ok=True)
os.makedirs('visualizations', exist_ok=True)
os.makedirs('results', exist_ok=True)

print("="*100)
print("TCGA-LUAD MACHINE LEARNING PIPELINE - PRODUCTION VERSION")
print("="*100)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


# PART 1: DATA LOADING

def load_gene_expression(filepath):
    """
    Load FPKM-UQ gene expression data from UCSC XENA
    
    File format: genes (rows) x samples (columns)
    Values: FPKM-UQ normalized expression
    
    Handles various file format quirks from UCSC Xena
    """
    print("\n" + "="*100)
    print("STEP 1: LOADING GENE EXPRESSION DATA")
    print("="*100)
    
    print(f"Loading file: {filepath}")
    
    # Try multiple loading strategies
    strategies = [
        {'compression': 'gzip', 'encoding': 'utf-8', 'on_bad_lines': 'skip'},
        {'compression': None, 'encoding': 'utf-8', 'on_bad_lines': 'skip'},
        {'compression': 'infer', 'encoding': 'utf-8', 'on_bad_lines': 'skip'},
        {'compression': None, 'encoding': 'latin-1', 'on_bad_lines': 'skip'},
    ]
    
    expression_df = None
    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"  Attempt {i}: compression={strategy['compression']}, encoding={strategy['encoding']}")
            expression_df = pd.read_csv(
                filepath,
                sep='\t',
                index_col=0,
                **strategy
            )
            print(f"  ✓ Success with strategy {i}!")
            break
        except Exception as e:
            print(f"  ✗ Failed: {str(e)[:100]}")
            continue
    
    if expression_df is None:
        raise ValueError("Could not load file with any strategy. Please run inspect_files.py first.")
    
    print(f"\n✓ Loaded successfully!")
    print(f"  Genes (rows): {len(expression_df):,}")
    print(f"  Samples (columns): {len(expression_df.columns):,}")
    print(f"  Shape: {expression_df.shape}")
    print(f"  Memory usage: {expression_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Display sample of data
    print(f"\nFirst 5 genes, first 3 samples:")
    print(expression_df.iloc[:5, :3])
    
    return expression_df


def load_clinical_data(filepath):
    """
    Load clinical metadata
    
    Handles various file format quirks
    """
    print(f"\nLoading clinical data: {filepath}")
    
    strategies = [
        {'compression': 'gzip', 'encoding': 'utf-8', 'on_bad_lines': 'skip'},
        {'compression': None, 'encoding': 'utf-8', 'on_bad_lines': 'skip'},
        {'compression': 'infer', 'encoding': 'utf-8', 'on_bad_lines': 'skip'},
    ]
    
    clinical_df = None
    for strategy in strategies:
        try:
            clinical_df = pd.read_csv(filepath, sep='\t', **strategy)
            break
        except Exception:
            continue
    
    if clinical_df is None:
        raise ValueError("Could not load clinical file. Please run inspect_files.py first.")
    
    print(f"✓ Clinical data loaded!")
    print(f"  Samples: {len(clinical_df):,}")
    print(f"  Clinical variables: {len(clinical_df.columns):,}")
    
    return clinical_df



# PART 2: LABEL EXTRACTION (CRITICAL - NO DATA LEAKAGE)

def extract_labels_from_barcodes(expression_df):
    """
    Extract tumor/normal labels from TCGA sample barcodes
    
    TCGA Barcode Structure:
    TCGA-XX-XXXX-XXA-XXX-XXXX-XX
                 ^^
                 Sample Type Code (positions 13-14)
                 01 = Primary Solid Tumor
                 11 = Solid Tissue Normal
    
    CRITICAL: This is ground truth - NO data leakage possible
    """
    print("\n" + "="*100)
    print("STEP 2: EXTRACTING LABELS FROM TCGA BARCODES")
    print("="*100)
    
    labels = []
    sample_ids = []
    sample_types = []
    
    for sample_barcode in expression_df.columns:
        # Extract sample type code from barcode
        # Position 13-14 (0-indexed: 13:15)
        try:
            sample_type_code = sample_barcode[13:15]
            
            if sample_type_code == '01':
                labels.append(1)  # Tumor
                sample_ids.append(sample_barcode)
                sample_types.append('Tumor')
            elif sample_type_code == '11':
                labels.append(0)  # Normal
                sample_ids.append(sample_barcode)
                sample_types.append('Normal')
            # Ignore other types (02=Recurrent, 06=Metastatic, etc.)
            
        except IndexError:
            print(f"WARNING: Could not parse barcode: {sample_barcode}")
            continue
    
    # Create label DataFrame
    label_df = pd.DataFrame({
        'sample_id': sample_ids,
        'label': labels,
        'class_name': sample_types
    })
    
    # Print statistics
    print(f"\n✓ Labels extracted successfully!")
    print(f"\nClass Distribution:")
    class_counts = label_df['class_name'].value_counts()
    print(class_counts)
    
    tumor_count = sum(labels)
    normal_count = len(labels) - tumor_count
    imbalance_ratio = tumor_count / normal_count if normal_count > 0 else float('inf')
    
    print(f"\nDetailed Statistics:")
    print(f"  Total samples: {len(labels)}")
    print(f"  Tumor samples: {tumor_count} ({tumor_count/len(labels)*100:.1f}%)")
    print(f"  Normal samples: {normal_count} ({normal_count/len(labels)*100:.1f}%)")
    print(f"  Imbalance ratio: {imbalance_ratio:.2f}:1 (Tumor:Normal)")
    
    if imbalance_ratio > 5:
        print(f"\n⚠️  WARNING: Significant class imbalance detected!")
        print(f"  Will use class_weight='balanced' and stratified sampling")
    
    # Filter expression data to keep only labeled samples
    expression_filtered = expression_df[sample_ids]
    
    return label_df, expression_filtered


# PART 3: DATA QUALITY CHECKS

def perform_quality_checks(expression_df):
    """
    Comprehensive data quality assessment
    """
    print("\n" + "="*100)
    print("STEP 3: DATA QUALITY CHECKS")
    print("="*100)
    
    print("\n1. Missing Values Assessment:")
    total_values = expression_df.size
    missing_values = expression_df.isnull().sum().sum()
    missing_percent = (missing_values / total_values) * 100
    
    print(f"  Total values: {total_values:,}")
    print(f"  Missing values: {missing_values:,} ({missing_percent:.4f}%)")
    
    if missing_values > 0:
        genes_with_missing = expression_df.isnull().any(axis=1).sum()
        print(f"  Genes with missing values: {genes_with_missing:,}")
    
    print("\n2. Expression Value Range:")
    print(f"  Minimum: {expression_df.min().min():.4f}")
    print(f"  Maximum: {expression_df.max().max():.4f}")
    print(f"  Mean: {expression_df.mean().mean():.4f}")
    print(f"  Median: {expression_df.median().median():.4f}")
    
    # Check if data is already log-transformed
    max_value = expression_df.max().max()
    if max_value < 50:
        print(f"\n⚠️  WARNING: Max value is {max_value:.2f}")
        print(f"  Data may already be log-transformed!")
        print(f"  FPKM-UQ values are typically in range [0, 1000+]")
    else:
        print(f"\n✓ Data appears to be in raw FPKM-UQ scale")
    
    print("\n3. Zero/Low Expression Analysis:")
    zero_genes = (expression_df == 0).all(axis=1).sum()
    low_expr_genes = (expression_df < 1).all(axis=1).sum()
    
    print(f"  Genes with all zeros: {zero_genes:,}")
    print(f"  Genes with all values < 1: {low_expr_genes:,}")
    
    return {
        'missing_percent': missing_percent,
        'max_value': max_value,
        'zero_genes': zero_genes
    }


# ============================================================================
# PART 4: PREPROCESSING PIPELINE (CORRECT ORDER - NO DATA LEAKAGE)
# ============================================================================
def preprocess_expression_data(expression_df, label_df, 
                                remove_low_expr=True,
                                log_transform=True,
                                handle_missing=True):
    """
    Complete preprocessing pipeline
    
    CRITICAL ORDER (to avoid data leakage):
    1. Handle missing values
    2. Remove low expression genes
    3. Log2 transformation
    4. NO SCALING YET (scaling must be done AFTER train-test split)
    """
    print("\n" + "="*100)
    print("STEP 4: PREPROCESSING")
    print("="*100)
    
    expr_processed = expression_df.copy()
    
    # -------------------- 4.1 Handle Missing Values --------------------
    if handle_missing:
        print("\n4.1 Handling Missing Values...")
        
        missing_before = expr_processed.isnull().sum().sum()
        
        if missing_before > 0:
            # Strategy: Remove genes with >30% missing, impute rest with median
            missing_threshold = 0.3
            missing_percent_per_gene = expr_processed.isnull().sum(axis=1) / len(expr_processed.columns)
            
            genes_to_keep = missing_percent_per_gene[missing_percent_per_gene < missing_threshold].index
            genes_removed = len(expr_processed) - len(genes_to_keep)
            
            expr_processed = expr_processed.loc[genes_to_keep]
            print(f"  Removed {genes_removed:,} genes with >{missing_threshold*100}% missing values")
            
            # Impute remaining missing values with gene-wise median
            expr_processed = expr_processed.T.fillna(expr_processed.T.median()).T
            
            missing_after = expr_processed.isnull().sum().sum()
            print(f"  Missing values: {missing_before:,} → {missing_after:,}")
        else:
            print(f"  ✓ No missing values detected")
    
    # -------------------- 4.2 Remove Low Expression Genes --------------------
    if remove_low_expr:
        print("\n4.2 Filtering Low Expression Genes...")
        
        genes_before = len(expr_processed)
        
        # Keep genes expressed (>1 FPKM-UQ) in at least 10% of samples
        min_samples = int(0.1 * len(expr_processed.columns))
        expressed_count = (expr_processed > 1).sum(axis=1)
        genes_to_keep = expressed_count[expressed_count >= min_samples].index
        
        expr_processed = expr_processed.loc[genes_to_keep]
        genes_after = len(expr_processed)
        
        print(f"  Genes before: {genes_before:,}")
        print(f"  Genes after: {genes_after:,}")
        print(f"  Removed: {genes_before - genes_after:,} low-expression genes")
    
    # -------------------- 4.3 Log2 Transformation --------------------
    if log_transform:
        print("\n4.3 Applying Log2 Transformation...")
        
        # Check if already transformed
        if expr_processed.max().max() < 50:
            print("  ⚠️  Data appears already log-transformed (max < 50)")
            print("  Skipping log transformation...")
        else:
            expr_before_range = (expr_processed.min().min(), expr_processed.max().max())
            
            # Apply log2(x + 1) to handle zeros
            expr_processed = np.log2(expr_processed + 1)
            
            expr_after_range = (expr_processed.min().min(), expr_processed.max().max())
            
            print(f"  Before: [{expr_before_range[0]:.2f}, {expr_before_range[1]:.2f}]")
            print(f"  After:  [{expr_after_range[0]:.2f}, {expr_after_range[1]:.2f}]")
            print(f"  ✓ Log2 transformation complete")
    
    print(f"\n✓ Preprocessing complete!")
    print(f"  Final gene count: {len(expr_processed):,}")
    print(f"  Sample count: {len(expr_processed.columns):,}")
    
    return expr_processed


# ============================================================================
# PART 5: TRAIN-TEST SPLIT (BEFORE FEATURE SELECTION - CRITICAL!)
# ============================================================================
def create_train_test_split(expression_df, label_df, test_size=0.2, random_state=42):
    """
    Create stratified train-test split
    
    CRITICAL: This must happen BEFORE:
    - Feature selection
    - Scaling/normalization
    To avoid data leakage!
    """
    print("\n" + "="*100)
    print("STEP 5: TRAIN-TEST SPLIT")
    print("="*100)
    
    # Prepare data
    X = expression_df.T.values  # Transpose to samples x genes
    y = label_df['label'].values
    sample_ids = label_df['sample_id'].values
    
    # Stratified split to maintain class distribution
    X_train, X_test, y_train, y_test, ids_train, ids_test = train_test_split(
        X, y, sample_ids,
        test_size=test_size,
        random_state=random_state,
        stratify=y  # CRITICAL: maintains class balance
    )
    
    print(f"\n✓ Split created with {test_size*100}% test size")
    print(f"\nTraining Set:")
    print(f"  Samples: {len(X_train)}")
    print(f"  Tumor: {sum(y_train)} ({sum(y_train)/len(y_train)*100:.1f}%)")
    print(f"  Normal: {len(y_train)-sum(y_train)} ({(len(y_train)-sum(y_train))/len(y_train)*100:.1f}%)")
    
    print(f"\nTest Set:")
    print(f"  Samples: {len(X_test)}")
    print(f"  Tumor: {sum(y_test)} ({sum(y_test)/len(y_test)*100:.1f}%)")
    print(f"  Normal: {len(y_test)-sum(y_test)} ({(len(y_test)-sum(y_test))/len(y_test)*100:.1f}%)")
    
    return X_train, X_test, y_train, y_test, ids_train, ids_test


# ============================================================================
# PART 6: FEATURE SELECTION (ON TRAINING DATA ONLY!)
# ============================================================================
def select_features(X_train, y_train, X_test, gene_names, n_features=1000):
    """
    Feature selection using ANOVA F-statistic
    
    CRITICAL: Fit on training data only, then transform both train and test
    This prevents data leakage!
    """
    print("\n" + "="*100)
    print("STEP 6: FEATURE SELECTION")
    print("="*100)
    
    print(f"\nSelecting top {n_features} most informative genes...")
    print(f"  Initial features: {X_train.shape[1]:,}")
    
    # CRITICAL: Fit selector on TRAINING data only
    selector = SelectKBest(score_func=f_classif, k=min(n_features, X_train.shape[1]))
    X_train_selected = selector.fit_transform(X_train, y_train)
    
    # Transform test data using SAME selector
    X_test_selected = selector.transform(X_test)
    
    # Get selected gene information
    selected_mask = selector.get_support()
    selected_genes = gene_names[selected_mask]
    feature_scores = selector.scores_[selected_mask]
    
    # Create gene ranking
    gene_ranking = pd.DataFrame({
        'gene': selected_genes,
        'f_score': feature_scores,
        'p_value': selector.pvalues_[selected_mask]
    }).sort_values('f_score', ascending=False)
    
    print(f"  Selected features: {X_train_selected.shape[1]:,}")
    print(f"\nTop 10 Most Discriminative Genes:")
    print(gene_ranking.head(10).to_string(index=False))
    
    # Save gene ranking
    gene_ranking.to_csv('results/selected_genes_ranking.csv', index=False)
    print(f"\n✓ Full gene ranking saved to: results/selected_genes_ranking.csv")
    
    return X_train_selected, X_test_selected, selector, selected_genes, gene_ranking


# ============================================================================
# PART 7: SCALING (ON TRAINING DATA ONLY!)
# ============================================================================
def scale_features(X_train, X_test):
    """
    Z-score normalization (standardization)
    
    CRITICAL: Fit scaler on training data, then transform both sets
    """
    print("\n" + "="*100)
    print("STEP 7: FEATURE SCALING")
    print("="*100)
    
    print("\nApplying Z-score normalization...")
    
    # CRITICAL: Fit on training data only
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)  # Use same scaler
    
    print(f"  Training set scaled: {X_train_scaled.shape}")
    print(f"  Test set scaled: {X_test_scaled.shape}")
    print(f"  Mean of first feature: {X_train_scaled[:, 0].mean():.6f}")
    print(f"  Std of first feature: {X_train_scaled[:, 0].std():.6f}")
    print(f"\n✓ Scaling complete")
    
    return X_train_scaled, X_test_scaled, scaler


# ============================================================================
# PART 8: HANDLE CLASS IMBALANCE (OPTIONAL SMOTE)
# ============================================================================
def apply_smote(X_train, y_train, use_smote=False):
    """
    Apply SMOTE for handling class imbalance
    
    Note: Only apply to training data, never to test data!
    """
    if not use_smote or not SMOTE_AVAILABLE:
        return X_train, y_train
    
    print("\n" + "="*100)
    print("STEP 8: APPLYING SMOTE")
    print("="*100)
    
    print(f"\nBefore SMOTE:")
    unique, counts = np.unique(y_train, return_counts=True)
    for u, c in zip(unique, counts):
        print(f"  Class {u}: {c} samples")
    
    smote = SMOTE(random_state=42)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
    
    print(f"\nAfter SMOTE:")
    unique, counts = np.unique(y_train_balanced, return_counts=True)
    for u, c in zip(unique, counts):
        print(f"  Class {u}: {c} samples")
    
    print(f"\n✓ SMOTE applied")
    
    return X_train_balanced, y_train_balanced


# ============================================================================
# PART 9: MODEL TRAINING
# ============================================================================
def train_random_forest(X_train, y_train):
    """
    Train Random Forest with optimized hyperparameters
    """
    print("\n" + "="*100)
    print("STEP 9A: TRAINING RANDOM FOREST")
    print("="*100)
    
    rf_model = RandomForestClassifier(
        n_estimators=200,           # More trees for stability
        max_depth=15,               # Prevent overfitting
        min_samples_split=10,       # Minimum samples to split
        min_samples_leaf=5,         # Minimum samples in leaf
        max_features='sqrt',        # Features per split
        class_weight='balanced',    # Handle imbalance
        random_state=42,
        n_jobs=-1,                  # Use all cores
        verbose=0
    )
    
    print("\nTraining Random Forest...")
    print(f"  Parameters: n_estimators=200, max_depth=15, class_weight='balanced'")
    
    rf_model.fit(X_train, y_train)
    
    print(f"✓ Random Forest trained successfully!")
    print(f"  Number of trees: {rf_model.n_estimators}")
    print(f"  Number of features used: {rf_model.n_features_in_}")
    
    return rf_model


def train_svm(X_train, y_train):
    """
    Train SVM with RBF kernel
    """
    print("\n" + "="*100)
    print("STEP 9B: TRAINING SVM")
    print("="*100)
    
    svm_model = SVC(
        kernel='rbf',               # RBF kernel for non-linear classification
        C=1.0,                      # Regularization
        gamma='scale',              # Kernel coefficient
        class_weight='balanced',    # Handle imbalance
        probability=True,           # Enable probability estimates
        random_state=42
    )
    
    print("\nTraining SVM...")
    print(f"  Parameters: kernel='rbf', C=1.0, class_weight='balanced'")
    
    svm_model.fit(X_train, y_train)
    
    print(f"✓ SVM trained successfully!")
    print(f"  Support vectors: {svm_model.n_support_}")
    print(f"  Classes: {svm_model.classes_}")
    
    return svm_model


# ============================================================================
# PART 10: MODEL EVALUATION
# ============================================================================
def evaluate_model_comprehensive(model, X_train, X_test, y_train, y_test, model_name):
    """
    Comprehensive model evaluation with multiple metrics
    """
    print("\n" + "="*100)
    print(f"EVALUATING {model_name.upper()}")
    print("="*100)
    
    # Training set predictions
    y_train_pred = model.predict(X_train)
    y_train_proba = model.predict_proba(X_train)[:, 1]
    
    # Test set predictions
    y_test_pred = model.predict(X_test)
    y_test_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    results = {}
    
    for dataset, y_true, y_pred, y_proba in [
        ('Training', y_train, y_train_pred, y_train_proba),
        ('Test', y_test, y_test_pred, y_test_proba)
    ]:
        print(f"\n{dataset} Set Performance:")
        print("-" * 60)
        
        # Classification report
        print(classification_report(y_true, y_pred, 
                                   target_names=['Normal', 'Tumor'],
                                   digits=4))
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        print("Confusion Matrix:")
        print(f"              Predicted")
        print(f"              Normal  Tumor")
        print(f"Actual Normal   {cm[0,0]:5d}  {cm[0,1]:5d}")
        print(f"       Tumor    {cm[1,0]:5d}  {cm[1,1]:5d}")
        
        # Detailed metrics
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        auc = roc_auc_score(y_true, y_proba)
        
        print(f"\nDetailed Metrics:")
        print(f"  Accuracy:  {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall:    {rec:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"  ROC-AUC:   {auc:.4f}")
        
        results[dataset.lower()] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1,
            'roc_auc': auc,
            'confusion_matrix': cm
        }
    
    # Check for overfitting
    train_acc = results['training']['accuracy']
    test_acc = results['test']['accuracy']
    overfit_gap = train_acc - test_acc
    
    print(f"\n{'='*60}")
    print(f"Overfitting Analysis:")
    print(f"  Training Accuracy: {train_acc:.4f}")
    print(f"  Test Accuracy:     {test_acc:.4f}")
    print(f"  Gap:               {overfit_gap:.4f}")
    
    if overfit_gap > 0.1:
        print(f"  ⚠️  WARNING: Possible overfitting detected!")
    elif overfit_gap > 0.05:
        print(f"  ⚠️  CAUTION: Moderate overfitting")
    else:
        print(f"  ✓ Good generalization")
    
    return results, y_test_pred, y_test_proba


# ============================================================================
# PART 11: CROSS-VALIDATION
# ============================================================================
def perform_cross_validation(model, X, y, cv_folds=5):
    """
    Perform stratified k-fold cross-validation
    """
    print("\n" + "="*100)
    print("CROSS-VALIDATION")
    print("="*100)
    
    print(f"\nPerforming {cv_folds}-fold stratified cross-validation...")
    
    # Define scoring metrics
    scoring = {
        'accuracy': 'accuracy',
        'precision': 'precision',
        'recall': 'recall',
        'f1': 'f1',
        'roc_auc': 'roc_auc'
    }
    
    # Stratified K-Fold
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    
    # Perform cross-validation
    cv_results = cross_validate(
        model, X, y,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
        return_train_score=True
    )
    
    # Print results
    print(f"\n{'Metric':<15} {'Mean':<10} {'Std':<10} {'Min':<10} {'Max':<10}")
    print("-" * 55)
    
    for metric in ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']:
        test_scores = cv_results[f'test_{metric}']
        print(f"{metric:<15} {test_scores.mean():8.4f}  {test_scores.std():8.4f}  "
              f"{test_scores.min():8.4f}  {test_scores.max():8.4f}")
    
    return cv_results


# ============================================================================
# PART 12: VISUALIZATION
# ============================================================================
def create_visualizations(X_train, X_test, y_train, y_test, 
                         selected_genes, rf_model, svm_model,
                         rf_proba, svm_proba):
    """
    Create all visualizations
    """
    print("\n" + "="*100)
    print("GENERATING VISUALIZATIONS")
    print("="*100)
    
    # 1. PCA Plot
    print("\n1. Creating PCA visualization...")
    create_pca_plot(X_train, X_test, y_train, y_test)
    
    # 2. Feature Importance
    print("2. Creating feature importance plot...")
    create_feature_importance_plot(rf_model, selected_genes)
    
    # 3. ROC Curves
    print("3. Creating ROC curves...")
    create_roc_curves(y_test, rf_proba, svm_proba)
    
    # 4. Confusion Matrices
    print("4. Creating confusion matrix heatmap...")
    create_confusion_matrix_heatmap(rf_model, svm_model, X_test, y_test)
    
    print("\n✓ All visualizations saved to: visualizations/")


def create_pca_plot(X_train, X_test, y_train, y_test):
    """PCA visualization"""
    # Combine train and test
    X_combined = np.vstack([X_train, X_test])
    y_combined = np.concatenate([y_train, y_test])
    
    # PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_combined)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = {0: 'blue', 1: 'red'}
    labels = {0: 'Normal', 1: 'Tumor'}
    
    for class_val in [0, 1]:
        mask = y_combined == class_val
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
                  c=colors[class_val], label=labels[class_val],
                  alpha=0.6, s=100, edgecolors='black', linewidth=0.5)
    
    ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)', fontsize=12)
    ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)', fontsize=12)
    ax.set_title('PCA: Tumor vs Normal Sample Separation', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations/pca_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_feature_importance_plot(model, gene_names, top_n=25):
    """Feature importance from Random Forest"""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:top_n]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.barh(range(top_n), importances[indices], color='steelblue', edgecolor='black')
    ax.set_yticks(range(top_n))
    ax.set_yticklabels([gene_names[i] for i in indices], fontsize=9)
    ax.set_xlabel('Feature Importance', fontsize=12)
    ax.set_title(f'Top {top_n} Most Important Genes', fontsize=14, fontweight='bold')
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('visualizations/feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_roc_curves(y_test, rf_proba, svm_proba):
    """ROC curves for both models"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Random Forest ROC
    fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_proba)
    auc_rf = roc_auc_score(y_test, rf_proba)
    ax.plot(fpr_rf, tpr_rf, color='darkgreen', lw=2.5, 
            label=f'Random Forest (AUC = {auc_rf:.4f})')
    
    # SVM ROC
    fpr_svm, tpr_svm, _ = roc_curve(y_test, svm_proba)
    auc_svm = roc_auc_score(y_test, svm_proba)
    ax.plot(fpr_svm, tpr_svm, color='darkorange', lw=2.5,
            label=f'SVM (AUC = {auc_svm:.4f})')
    
    # Diagonal line
    ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
    
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate', fontsize=12)
    ax.set_title('ROC Curves Comparison', fontsize=14, fontweight='bold')
    ax.legend(loc="lower right", fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations/roc_curves.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_confusion_matrix_heatmap(rf_model, svm_model, X_test, y_test):
    """Confusion matrices as heatmaps"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Random Forest
    rf_pred = rf_model.predict(X_test)
    cm_rf = confusion_matrix(y_test, rf_pred)
    sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Normal', 'Tumor'],
                yticklabels=['Normal', 'Tumor'],
                ax=axes[0], cbar_kws={'label': 'Count'})
    axes[0].set_title('Random Forest', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Actual', fontsize=11)
    axes[0].set_xlabel('Predicted', fontsize=11)
    
    # SVM
    svm_pred = svm_model.predict(X_test)
    cm_svm = confusion_matrix(y_test, svm_pred)
    sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Oranges',
                xticklabels=['Normal', 'Tumor'],
                yticklabels=['Normal', 'Tumor'],
                ax=axes[1], cbar_kws={'label': 'Count'})
    axes[1].set_title('SVM', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Actual', fontsize=11)
    axes[1].set_xlabel('Predicted', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('visualizations/confusion_matrices.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# PART 13: SAVE MODELS AND RESULTS
# ============================================================================
def save_models_and_artifacts(rf_model, svm_model, scaler, selector, 
                               selected_genes, results_dict):
    """
    Save all models and preprocessing objects
    """
    print("\n" + "="*100)
    print("SAVING MODELS AND ARTIFACTS")
    print("="*100)
    
    # Save models
    joblib.dump(rf_model, 'models/random_forest_model.pkl')
    print("✓ Random Forest model saved: models/random_forest_model.pkl")
    
    joblib.dump(svm_model, 'models/svm_model.pkl')
    print("✓ SVM model saved: models/svm_model.pkl")
    
    # Save preprocessing objects
    joblib.dump(scaler, 'models/scaler.pkl')
    print("✓ Scaler saved: models/scaler.pkl")
    
    joblib.dump(selector, 'models/gene_selector.pkl')
    print("✓ Feature selector saved: models/gene_selector.pkl")
    
    # Save selected genes list
    pd.DataFrame({'gene': selected_genes}).to_csv('models/selected_genes.csv', index=False)
    print("✓ Selected genes list saved: models/selected_genes.csv")
    
    # Save comprehensive results
    results_summary = pd.DataFrame(results_dict).T
    results_summary.to_csv('results/model_performance_summary.csv')
    print("✓ Performance summary saved: results/model_performance_summary.csv")
    
    print("\n✓ All models and artifacts saved successfully!")


# ============================================================================
# MAIN PIPELINE EXECUTION
# ============================================================================
def main():
    """
    Execute complete ML pipeline
    """
    
    # File paths - UPDATED for your actual files
    EXPRESSION_FILE = 'TCGA-LUAD.star_fpkm-uq.tsv'  # Note: hyphen, not underscore
    CLINICAL_FILE = 'TCGA-LUAD.clinical.tsv'  # Note: hyphen, not underscore
    
    # Hyperparameters
    TEST_SIZE = 0.2
    N_FEATURES = 1000
    CV_FOLDS = 5
    USE_SMOTE = False  # Set to True if you want to use SMOTE
    RANDOM_STATE = 42
    
    print(f"\nConfiguration:")
    print(f"  Test size: {TEST_SIZE*100}%")
    print(f"  Number of features to select: {N_FEATURES}")
    print(f"  Cross-validation folds: {CV_FOLDS}")
    print(f"  Use SMOTE: {USE_SMOTE}")
    print(f"  Random state: {RANDOM_STATE}")
    
    # Step 1: Load data
    expression_df = load_gene_expression(EXPRESSION_FILE)
    clinical_df = load_clinical_data(CLINICAL_FILE)
    
    # Step 2: Extract labels
    label_df, expression_filtered = extract_labels_from_barcodes(expression_df)
    
    # Step 3: Quality checks
    qc_results = perform_quality_checks(expression_filtered)
    
    # Step 4: Preprocess
    expression_processed = preprocess_expression_data(
        expression_filtered,
        label_df,
        remove_low_expr=True,
        log_transform=True,
        handle_missing=True
    )
    
    # Step 5: Train-test split (BEFORE feature selection!)
    X_train, X_test, y_train, y_test, ids_train, ids_test = create_train_test_split(
        expression_processed,
        label_df,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE
    )
    
    # Step 6: Feature selection (on training data only)
    gene_names = expression_processed.index.values
    X_train_selected, X_test_selected, selector, selected_genes, gene_ranking = select_features(
        X_train, y_train, X_test, gene_names, n_features=N_FEATURES
    )
    
    # Step 7: Scale features (on training data only)
    X_train_scaled, X_test_scaled, scaler = scale_features(
        X_train_selected, X_test_selected
    )
    
    # Step 8: Apply SMOTE if requested
    X_train_final, y_train_final = apply_smote(X_train_scaled, y_train, use_smote=USE_SMOTE)
    
    # Step 9: Train models
    rf_model = train_random_forest(X_train_final, y_train_final)
    svm_model = train_svm(X_train_final, y_train_final)
    
    # Step 10: Evaluate models
    rf_results, rf_pred, rf_proba = evaluate_model_comprehensive(
        rf_model, X_train_scaled, X_test_scaled, y_train, y_test, 'Random Forest'
    )
    
    svm_results, svm_pred, svm_proba = evaluate_model_comprehensive(
        svm_model, X_train_scaled, X_test_scaled, y_train, y_test, 'SVM'
    )
    
    # Step 11: Cross-validation
    print("\n" + "="*100)
    print("CROSS-VALIDATION - RANDOM FOREST")
    print("="*100)
    rf_cv_results = perform_cross_validation(rf_model, X_train_scaled, y_train, cv_folds=CV_FOLDS)
    
    print("\n" + "="*100)
    print("CROSS-VALIDATION - SVM")
    print("="*100)
    svm_cv_results = perform_cross_validation(svm_model, X_train_scaled, y_train, cv_folds=CV_FOLDS)
    
    # Step 12: Create visualizations
    create_visualizations(
        X_train_scaled, X_test_scaled, y_train, y_test,
        selected_genes, rf_model, svm_model,
        rf_proba, svm_proba
    )
    
    # Step 13: Save everything
    results_dict = {
        'Random_Forest': rf_results['test'],
        'SVM': svm_results['test']
    }
    
    save_models_and_artifacts(
        rf_model, svm_model, scaler, selector,
        selected_genes, results_dict
    )
    
    # Final summary
    print("\n" + "="*100)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*100)
    print("\nFinal Model Comparison (Test Set):")
    print("-" * 80)
    print(f"{'Metric':<15} {'Random Forest':<20} {'SVM':<20}")
    print("-" * 80)
    
    metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
    for metric in metrics:
        rf_val = rf_results['test'][metric]
        svm_val = svm_results['test'][metric]
        better = '✓' if rf_val > svm_val else ''
        worse = '✓' if svm_val > rf_val else ''
        print(f"{metric:<15} {rf_val:8.4f} {better:<11} {svm_val:8.4f} {worse:<11}")
    
    print("\n" + "="*100)
    print("OUTPUT FILES:")
    print("="*100)
    print("\nModels:")
    print("  - models/random_forest_model.pkl")
    print("  - models/svm_model.pkl")
    print("  - models/scaler.pkl")
    print("  - models/gene_selector.pkl")
    print("  - models/selected_genes.csv")
    
    print("\nResults:")
    print("  - results/selected_genes_ranking.csv")
    print("  - results/model_performance_summary.csv")
    
    print("\nVisualizations:")
    print("  - visualizations/pca_plot.png")
    print("  - visualizations/feature_importance.png")
    print("  - visualizations/roc_curves.png")
    print("  - visualizations/confusion_matrices.png")
    
    print("\n" + "="*100)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100)
    
    return {
        'rf_model': rf_model,
        'svm_model': svm_model,
        'rf_results': rf_results,
        'svm_results': svm_results,
        'selected_genes': selected_genes,
        'gene_ranking': gene_ranking
    }


if __name__ == '__main__':
    results = main()