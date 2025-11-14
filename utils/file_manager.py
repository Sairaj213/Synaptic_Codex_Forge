import os
import shutil
import zipfile
import streamlit as st
from config import PROJECT_OUTPUT_DIR

def create_project_structure(project_name, structure_plan):

    project_path = os.path.join(PROJECT_OUTPUT_DIR, project_name)

    if os.path.exists(project_path):
        shutil.rmtree(project_path)

    os.makedirs(project_path, exist_ok=True)

    log = []

    if "folders" in structure_plan:
        for folder in structure_plan["folders"]:
            folder_path = os.path.join(project_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            log.append(f"Created folder: {folder_path}")

    if "files" in structure_plan:
        for file_path, description in structure_plan["files"].items():
            full_file_path = os.path.join(project_path, file_path)
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
            with open(full_file_path, 'w') as f:
                if description.startswith("Placeholder"):
                    f.write(f"# {description}\n")
                else:
                     f.write("") 
            log.append(f"Created empty file: {full_file_path}")

    return project_path, log

def save_code_to_file(file_path, code):

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        return True, f"Successfully saved code to {file_path}"
    except Exception as e:
        return False, f"Error saving file {file_path}: {e}"

def zip_project_folder(project_path, project_name):

    zip_file_name = f"{project_name}.zip"
    zip_file_path = os.path.join(PROJECT_OUTPUT_DIR, zip_file_name)

    try:
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, project_path)
                    zipf.write(full_path, relative_path)

        return zip_file_path, f"Project zipped successfully: {zip_file_path}"
    except Exception as e:
        return None, f"Error zipping project: {e}"
