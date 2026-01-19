"""
===============================================================================
AUTOMATIC GENE ANNOTATION TOOL
===============================================================================
Converts Ensembl Gene IDs to Human-Readable Gene Names and Functions

This script takes your top discriminative genes (Ensembl IDs like ENSG00000224215)
and automatically fetches:
- Gene Symbol (e.g., SFTPA1, TP53)
- Gene Name (full description)
- Chromosome location
- Gene type (protein_coding, lncRNA, etc.)
- Associated diseases/functions

Methods:
1. Using mygene.info API (RECOMMENDED - No installation needed)
2. Using biomaRt (Alternative - requires R integration)
3. Manual lookup guide
===============================================================================
"""

import pandas as pd
import requests
import json
import time
from typing import List, Dict

# ============================================================================
# METHOD 1: AUTOMATIC ANNOTATION USING MYGENE.INFO API (EASIEST!)
# ============================================================================

def annotate_genes_mygene(ensembl_ids: List[str]) -> pd.DataFrame:
    """
    Annotate Ensembl gene IDs using MyGene.info API
    
    This is FREE, no API key needed, and very reliable!
    """
    print("="*70)
    print("ANNOTATING GENES USING MYGENE.INFO API")
    print("="*70)
    
    # Clean Ensembl IDs (remove version numbers)
    clean_ids = [gene_id.split('.')[0] for gene_id in ensembl_ids]
    
    results = []
    
    # Query in batches of 100 (API limit)
    batch_size = 100
    for i in range(0, len(clean_ids), batch_size):
        batch = clean_ids[i:i+batch_size]
        
        print(f"\nProcessing batch {i//batch_size + 1} ({len(batch)} genes)...")
        
        # Query MyGene.info API
        url = "http://mygene.info/v3/gene"
        params = {
            'ids': ','.join(batch),
            'fields': 'symbol,name,summary,type_of_gene,genomic_pos,alias',
            'species': 'human'
        }
        
        try:
            response = requests.post(url, data=params)
            data = response.json()
            
            # Process results
            for item in data:
                if isinstance(item, dict) and 'notfound' not in item:
                    results.append({
                        'ensembl_id': item.get('query', 'Unknown'),
                        'gene_symbol': item.get('symbol', 'Unknown'),
                        'gene_name': item.get('name', 'No description'),
                        'gene_type': item.get('type_of_gene', 'Unknown'),
                        'summary': item.get('summary', 'No summary available')[:200] + '...' if item.get('summary') else 'N/A',
                        'chromosome': item.get('genomic_pos', {}).get('chr', 'Unknown') if isinstance(item.get('genomic_pos'), dict) else 'Unknown'
                    })
                else:
                    results.append({
                        'ensembl_id': item.get('query', 'Unknown'),
                        'gene_symbol': 'Not Found',
                        'gene_name': 'Gene not found in database',
                        'gene_type': 'Unknown',
                        'summary': 'N/A',
                        'chromosome': 'Unknown'
                    })
            
            # Be nice to the API
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error in batch {i//batch_size + 1}: {str(e)}")
            continue
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    print(f"\n✓ Annotated {len(df)} genes successfully!")
    
    return df

# ============================================================================
# METHOD 2: USING ENSEMBL REST API (ALTERNATIVE)
# ============================================================================

def annotate_genes_ensembl(ensembl_ids: List[str]) -> pd.DataFrame:
    """
    Annotate genes using Ensembl REST API
    More detailed but slower
    """
    print("="*70)
    print("ANNOTATING GENES USING ENSEMBL REST API")
    print("="*70)
    
    server = "https://rest.ensembl.org"
    results = []
    
    for idx, gene_id in enumerate(ensembl_ids, 1):
        # Clean ID (remove version)
        clean_id = gene_id.split('.')[0]
        
        print(f"Processing {idx}/{len(ensembl_ids)}: {clean_id}...", end=' ')
        
        try:
            # Query Ensembl
            ext = f"/lookup/id/{clean_id}?expand=1"
            r = requests.get(server + ext, headers={"Content-Type": "application/json"})
            
            if r.ok:
                data = r.json()
                
                results.append({
                    'ensembl_id': gene_id,
                    'gene_symbol': data.get('display_name', 'Unknown'),
                    'gene_name': data.get('description', 'No description'),
                    'gene_type': data.get('biotype', 'Unknown'),
                    'chromosome': data.get('seq_region_name', 'Unknown'),
                    'start': data.get('start', 'N/A'),
                    'end': data.get('end', 'N/A'),
                    'strand': data.get('strand', 'N/A')
                })
                print("✓")
            else:
                results.append({
                    'ensembl_id': gene_id,
                    'gene_symbol': 'Not Found',
                    'gene_name': 'Gene not found',
                    'gene_type': 'Unknown',
                    'chromosome': 'Unknown',
                    'start': 'N/A',
                    'end': 'N/A',
                    'strand': 'N/A'
                })
                print("✗")
            
            # Be nice to Ensembl servers
            time.sleep(0.35)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            continue
    
    df = pd.DataFrame(results)
    print(f"\n✓ Annotated {len(df)} genes!")
    
    return df

# ============================================================================
# MAIN EXECUTION - ANNOTATE YOUR TOP GENES
# ============================================================================

if __name__ == "__main__":
    
    # Your top genes from the analysis
    top_genes = [
        "ENSG00000224215.1",
        "ENSG00000180440.4",
        "ENSG00000261863.1",
        "ENSG00000150625.16",
        "ENSG00000108576.10",
        "ENSG00000158764.7",
        "ENSG00000140600.17",
        "ENSG00000161649.13",
        "ENSG00000102683.8",
        "ENSG00000154342.6",
        "ENSG00000169218.14",
        "ENSG00000197465.14",
        "ENSG00000135604.10",
        "ENSG00000159307.19",
        "ENSG00000246430.7",
        "ENSG00000235387.5",
        "ENSG00000182010.11",
        "ENSG00000134115.13",
        "ENSG00000168952.15",
        "ENSG00000234281.5"
    ]
    
    # Load your feature importance data if you saved it
    # feature_scores = pd.read_csv('feature_importance.csv')
    # top_genes = feature_scores['gene'].head(20).tolist()
    
    print("\n" + "="*70)
    print("GENE ANNOTATION PIPELINE")
    print("="*70)
    print(f"Annotating {len(top_genes)} top discriminative genes...")
    
    # METHOD 1: Use MyGene.info (RECOMMENDED)
    print("\n[METHOD 1] Using MyGene.info API...")
    annotated_df = annotate_genes_mygene(top_genes)
    
    # Display results
    print("\n" + "="*70)
    print("ANNOTATION RESULTS - TOP 20 GENES")
    print("="*70)
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    
    print("\n", annotated_df.to_string(index=False))
    
    # Save results
    annotated_df.to_csv('annotated_top_genes.csv', index=False)
    print("\n✓ Results saved to: annotated_top_genes.csv")
    
    # Create a nice summary table
    print("\n" + "="*70)
    print("QUICK SUMMARY - GENE SYMBOLS")
    print("="*70)
    
    summary = annotated_df[['ensembl_id', 'gene_symbol', 'gene_type', 'chromosome']]
    print("\n", summary.to_string(index=False))
    
    # Analyze gene types
    print("\n" + "="*70)
    print("GENE TYPE DISTRIBUTION")
    print("="*70)
    gene_type_counts = annotated_df['gene_type'].value_counts()
    print(gene_type_counts)
    
    # Create a detailed report
    print("\n" + "="*70)
    print("CREATING DETAILED REPORT...")
    print("="*70)
    
    with open('gene_annotation_report.txt', 'w') as f:
        f.write("="*70 + "\n")
        f.write("TOP 20 DISCRIMINATIVE GENES FOR LUAD CLASSIFICATION\n")
        f.write("="*70 + "\n\n")
        
        for idx, row in annotated_df.iterrows():
            f.write(f"\n{idx + 1}. {row['gene_symbol']} ({row['ensembl_id']})\n")
            f.write(f"   Type: {row['gene_type']}\n")
            f.write(f"   Location: Chromosome {row['chromosome']}\n")
            f.write(f"   Name: {row['gene_name']}\n")
            if row['summary'] != 'N/A':
                f.write(f"   Summary: {row['summary']}\n")
            f.write("-"*70 + "\n")
    
    print("✓ Detailed report saved to: gene_annotation_report.txt")
    
    # ========================================================================
    # BONUS: Search for cancer-related genes
    # ========================================================================
    print("\n" + "="*70)
    print("IDENTIFYING CANCER-RELATED GENES")
    print("="*70)
    
    cancer_keywords = ['cancer', 'tumor', 'carcinoma', 'oncogene', 'malignant', 
                       'metastasis', 'proliferation', 'apoptosis']
    
    cancer_related = []
    for idx, row in annotated_df.iterrows():
        gene_info = f"{row['gene_name']} {row['summary']}".lower()
        if any(keyword in gene_info for keyword in cancer_keywords):
            cancer_related.append({
                'gene_symbol': row['gene_symbol'],
                'ensembl_id': row['ensembl_id'],
                'relevance': 'Cancer-related'
            })
    
    if cancer_related:
        print(f"\n✓ Found {len(cancer_related)} genes with direct cancer relevance:")
        for gene in cancer_related:
            print(f"  - {gene['gene_symbol']} ({gene['ensembl_id']})")
    else:
        print("\nNote: Summary data may not be available for all genes.")
        print("Check the full annotation file for details.")
    
    print("\n" + "="*70)
    print("ANNOTATION COMPLETE!")
    print("="*70)
    print("\nFiles created:")
    print("  1. annotated_top_genes.csv - Complete annotation data")
    print("  2. gene_annotation_report.txt - Human-readable report")
    print("\nUse these in your project report and presentation!")
    print("="*70)

# ============================================================================
# ALTERNATIVE: If you want to annotate from saved feature importance file
# ============================================================================

def annotate_from_feature_file(feature_file: str, top_n: int = 20):
    """
    Load feature importance file and annotate top N genes
    """
    print(f"Loading features from {feature_file}...")
    
    # Assuming your feature file has columns: gene, f_score, p_value
    features = pd.read_csv(feature_file, sep='\t')
    
    # Get top N genes
    top_genes = features.head(top_n)['gene'].tolist()
    
    print(f"Annotating top {top_n} genes...")
    
    # Annotate
    annotated = annotate_genes_mygene(top_genes)
    
    # Merge with feature scores
    features_with_names = features.head(top_n).merge(
        annotated,
        left_on='gene',
        right_on='ensembl_id',
        how='left'
    )
    
    return features_with_names

# Example usage:
# annotated_features = annotate_from_feature_file('top_features.tsv', top_n=50)
# annotated_features.to_csv('features_with_gene_names.csv', index=False)