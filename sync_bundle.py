import os
import shutil
import subprocess
import yaml

# Define paths
operator_bundle_path = 'rhods-operator/path/to/bundle/files'
rbc_bundle_path = 'rbc/bundle'
rbc_dockerfile_path = 'rbc/Dockerfile'
csv_path = 'rhods-operator/path/to/csv'
metadata_path = 'rhods-operator/path/to/metadata'
crds_path = 'rhods-operator/path/to/crds'

# Helper functions
def remove_unwanted_fields(file_path):
    with open(file_path, 'r') as f:
        content = yaml.safe_load(f)
    
    # Remove channels, default channel, replaces, and skip ranges
    content.pop('channels', None)
    content.pop('defaultChannel', None)
    content.pop('replaces', None)
    content.pop('skipRanges', None)
    
    with open(file_path, 'w') as f:
        yaml.safe_dump(content, f)

def sync_files():
    # Sync CSV, metadata, CRDs, and Dockerfile
    if os.path.exists(operator_bundle_path):
        shutil.copytree(operator_bundle_path, rbc_bundle_path, dirs_exist_ok=True)
    if os.path.exists(csv_path):
        shutil.copy(csv_path, os.path.join(rbc_bundle_path, 'csv'))
    if os.path.exists(metadata_path):
        shutil.copy(metadata_path, os.path.join(rbc_bundle_path, 'metadata'))
    if os.path.exists(crds_path):
        shutil.copytree(crds_path, os.path.join(rbc_bundle_path, 'crds'), dirs_exist_ok=True)
    if os.path.exists(operator_bundle_path):
        shutil.copy(os.path.join(operator_bundle_path, 'Dockerfile'), rbc_dockerfile_path)
    
    # Remove unwanted fields from CSV files if necessary
    for root, _, files in os.walk(rbc_bundle_path):
        for file in files:
            if file.endswith('.yaml'):
                remove_unwanted_fields(os.path.join(root, file))

if __name__ == "__main__":
    sync_files()
