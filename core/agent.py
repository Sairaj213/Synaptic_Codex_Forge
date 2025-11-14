import os
import time
import ast
import re
import streamlit as st
from core.model import generate_text
from core.prompts import get_planner_system_prompt, get_coder_system_prompt, get_coder_user_prompt
from utils.file_manager import create_project_structure, save_code_to_file, zip_project_folder
from config import DEFAULT_PROJECT_STRUCTURE

def log_message(message, type="info", placeholder=None):

    st.session_state.generation_log.append(message)

    if placeholder:
        log_func = getattr(placeholder, type, placeholder.info)
        log_func(message)

def run_planner(user_request, model, tokenizer, llm_params, log_placeholder):

    log_message("Calling 'Planner' agent...", placeholder=log_placeholder)
    system_prompt = get_planner_system_prompt()

    response = generate_text(system_prompt, user_request, model, tokenizer, llm_params)

    if "Error" in response:
        log_message(response, "error", placeholder=log_placeholder)
        return None

    try:
        start_index = response.find('{')
        end_index = response.rfind('}')

        if start_index == -1 or end_index == -1:
            raise ValueError("Could not find a dictionary in the model's response.")

        plan_str = response[start_index : end_index + 1]
        plan_str = plan_str.replace("Placeholder", "'Placeholder'").replace("Basic boilerplate", "'Basic boilerplate'")
        project_plan = ast.literal_eval(plan_str)

        if not isinstance(project_plan, dict):
            raise ValueError("Planner did not return a valid dictionary structure.")

        full_plan = {
            "folders": DEFAULT_PROJECT_STRUCTURE["folders"],
            "files": project_plan
        }

        st.session_state.project_plan = full_plan
        log_message("✅ Project plan generated successfully.", "success", placeholder=log_placeholder)
        return full_plan

    except Exception as e:
        log_message(f"Error parsing planner response: {e}\nResponse was: {response}", "error", placeholder=log_placeholder)
        return None

def clean_code_output(raw_code):
    start_fence = raw_code.find("```")
    if start_fence == -1:
        return raw_code.strip()
    first_newline = raw_code.find('\n', start_fence)
    if first_newline == -1:
        code_start = start_fence + 3
    else:
        code_start = first_newline + 1
    last_fence = raw_code.rfind("```")
    if last_fence == -1 or last_fence <= code_start:
        return raw_code[code_start:].strip()
    return raw_code[code_start : last_fence].strip()


def run_coder_and_saver(project_path, project_plan, model, tokenizer, llm_params, log_placeholder):

    log_message("Calling 'Coder' agent for each file...", placeholder=log_placeholder)

    total_lines = 0
    generated_files_list = []
    files_to_generate = project_plan.get("files", {})
    if not files_to_generate:
        log_message("No files found in the project plan.", "warning", placeholder=log_placeholder)
        return

    st.session_state.generated_code = {}

    for file_name, task_description in files_to_generate.items():
        log_message(f"Generating code for: {file_name}...", placeholder=log_placeholder)

        system_prompt = get_coder_system_prompt()
        user_prompt = get_coder_user_prompt(project_plan, file_name)
        raw_output = generate_text(system_prompt, user_prompt, model, tokenizer, llm_params)
        generated_code = clean_code_output(raw_output)

        if "Error" in raw_output:
            log_message(f"Error generating code for {file_name}: {raw_output}", "error", placeholder=log_placeholder)
            continue

        if not generated_code and "Placeholder" not in task_description:
            log_message(f"Error generating code for {file_name}: Model returned empty string.", "error", placeholder=log_placeholder)
            continue

        full_file_path = os.path.join(project_path, file_name)
        success, message = save_code_to_file(full_file_path, generated_code)

        if success:
            lines = len(generated_code.split('\n'))
            total_lines += lines
            generated_files_list.append({"File": file_name, "Status": "✅ Generated", "Lines": lines})
            log_message(f"✅ Saved {file_name} ({lines} lines).", "success", placeholder=log_placeholder)
            st.session_state.generated_code[file_name] = generated_code
        else:
            log_message(message, "error", placeholder=log_placeholder)
            generated_files_list.append({"File": file_name, "Status": "❌ Error", "Lines": 0})

    return total_lines, generated_files_list


def run_generation_pipeline(user_request, project_name, model, tokenizer, llm_params, log_placeholder):

    start_time = time.time()
    st.session_state.generation_log = []
    st.session_state.project_plan = None
    st.session_state.project_zip_path = None
    st.session_state.generated_code = {}
    st.session_state.project_stats = {"total_files": 0, "total_lines": 0, "time_taken": 0.0, "files_list": []}
    project_plan = run_planner(user_request, model, tokenizer, llm_params, log_placeholder)
    if project_plan is None:
        return

    log_message("Creating project directory structure...", placeholder=log_placeholder)
    project_path, logs = create_project_structure(project_name, project_plan)
    for log in logs:
        st.session_state.generation_log.append(log) 
        log_message(log, "info", placeholder=log_placeholder) 
    log_message(f"✅ Project structure created at: {project_path}", "success", placeholder=log_placeholder)
    total_lines, files_list = run_coder_and_saver(project_path, project_plan, model, tokenizer, llm_params, log_placeholder)
    log_message("Zipping project folder for download...", placeholder=log_placeholder)
    zip_path, message = zip_project_folder(project_path, project_name)
    if zip_path:
        st.session_state.project_zip_path = zip_path
        log_message(f"✅ Project zipped successfully!", "success", placeholder=log_placeholder)
    else:
        log_message(message, "error", placeholder=log_placeholder)

    end_time = time.time()
    time_taken = end_time - start_time
    st.session_state.project_stats = {
        "total_files": len(files_list),
        "total_lines": total_lines,
        "time_taken": round(time_taken, 2),
        "files_list": files_list
    }
    log_message(f"--- Pipeline Finished in {time_taken:.2f} seconds ---", "success", placeholder=log_placeholder)
    log_placeholder.balloons()
