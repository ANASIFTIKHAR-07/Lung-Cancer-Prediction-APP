"""
Simple ZIP creator for sharing your ML models
"""

import zipfile
import os
from datetime import datetime

def create_zip(zip_name='LUAD_Complete_Package.zip', include_data=False):
    """
    Create a ZIP file with everything in the current directory
    
    Args:
        zip_name: Name of the output ZIP file
        include_data: If True, includes large data files (clinical, expression)
    """
    print("="*80)
    print("CREATING COMPLETE ZIP FILE")
    print("="*80)
    
    # Get everything in current directory
    print("\nScanning current directory...")
    all_items = os.listdir('.')
    
    # Exclude certain files
    exclude = [
        zip_name,  # Don't zip the zip file itself!
        '.git',    # Don't include git folder
        '__pycache__',  # Don't include Python cache
        '.DS_Store',  # Mac files
        'Thumbs.db',  # Windows thumbnails
    ]
    
    # Optional: exclude large data files to make ZIP smaller
    if not include_data:
        exclude.extend([
            'TCGA-LUAD.star_fpkm-uq.tsv',  # Large expression file
            'TCGA-LUAD.clinical.tsv',       # Clinical file
        ])
        print("\n⚠️  Excluding large data files to reduce ZIP size")
        print("   (Your friend probably doesn't need the raw data)")
    
    # Create ZIP
    print(f"\nCreating: {zip_name}")
    print("-" * 80)
    
    file_count = 0
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for item in all_items:
            # Skip excluded items
            if item in exclude:
                print(f"  ⊘ Skipping: {item}")
                continue
            
            if os.path.isfile(item):
                # It's a file
                zipf.write(item)
                file_count += 1
                size = os.path.getsize(item) / 1024  # KB
                print(f"  ✓ Added file: {item} ({size:.1f} KB)")
            
            elif os.path.isdir(item):
                # It's a folder - add all files in it
                folder_files = 0
                for root, dirs, files in os.walk(item):
                    # Skip hidden/cache folders
                    dirs[:] = [d for d in dirs if d not in exclude]
                    
                    for file in files:
                        filepath = os.path.join(root, file)
                        zipf.write(filepath)
                        folder_files += 1
                        file_count += 1
                
                print(f"  ✓ Added folder: {item}/ ({folder_files} files)")
    
    # Summary
    zip_size = os.path.getsize(zip_name) / 1024 / 1024  # MB
    
    print("\n" + "="*80)
    print("ZIP FILE CREATED SUCCESSFULLY!")
    print("="*80)
    print(f"\nFile: {zip_name}")
    print(f"Size: {zip_size:.2f} MB")
    print(f"Total files: {file_count}")
    print(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n📦 Contents:")
    print("  ✓ models/ - Trained ML models (.pkl files)")
    print("  ✓ results/ - Performance metrics (CSV)")
    print("  ✓ visualizations/ - Plots (PNG)")
    print("  ✓ luad_ml_pipeline.py - Complete ML code")
    print("  ✓ requirements.txt - Dependencies")
    print("  ✓ All other files in directory")
    
    if not include_data:
        print("\n  ⚠️  Raw data files NOT included (to keep ZIP small)")
        print("     If you need to include data files, run:")
        print("     create_zip('LUAD_With_Data.zip', include_data=True)")
    
    print("\n📤 Ready to share via:")
    print("  - Google Drive (recommended)")
    print("  - OneDrive") 
    print("  - Dropbox")
    print("  - Email (if < 25MB)")
    print("  - GitHub (if < 100MB)")
    
    print("\n" + "="*80)

def list_directory_contents():
    """Show what will be zipped"""
    print("\n" + "="*80)
    print("CURRENT DIRECTORY CONTENTS")
    print("="*80)
    
    for item in os.listdir('.'):
        if os.path.isfile(item):
            size = os.path.getsize(item) / 1024 / 1024  # MB
            print(f"  📄 {item} ({size:.2f} MB)")
        elif os.path.isdir(item):
            # Count files in directory
            file_count = sum([len(files) for _, _, files in os.walk(item)])
            print(f"  📁 {item}/ ({file_count} files)")
    
    print("="*80)

if __name__ == '__main__':
    # Show what's in the directory
    list_directory_contents()
    
    print("\n" + "="*80)
    print("CHOOSE WHAT TO ZIP:")
    print("="*80)
    print("\nOption 1: Complete package WITHOUT large data files (recommended)")
    print("  Size: ~5-15 MB")
    print("  Includes: models, results, code, visualizations")
    print("  Excludes: TCGA data files (277 MB)")
    
    print("\nOption 2: Everything INCLUDING data files")
    print("  Size: ~280-300 MB")
    print("  Includes: Everything!")
    
    # Create the recommended package
    print("\n" + "="*80)
    print("Creating Option 1 (recommended)...")
    print("="*80)
    create_zip('LUAD_Complete_Package.zip', include_data=False)
    
    # Uncomment below if you want to include data files too
    # print("\nAlso creating Option 2 (with data)...")
    # create_zip('LUAD_With_Data.zip', include_data=True)
    
    print("\n✅ Done! You can now share the ZIP file(s).")
    print("\n💡 TIP: If your friend needs the data files, share them separately")
    print("   via Google Drive (they're too large for email).")