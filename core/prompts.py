from config import DEFAULT_PROJECT_STRUCTURE

def get_planner_system_prompt():

    file_list = "\n".join([f"- {f}" for f in DEFAULT_PROJECT_STRUCTURE['files'].keys()])

    prompt = f"""
You are an expert software architect. Your job is to analyze a user's request and create a concise, one-sentence functional description for *each file* in a predefined project structure.

**Your Task:**
Based on the user's request, you must provide a new description for *every file* listed below.
Do not add, remove, or rename any files.
If a file is not needed for the user's request, you *must* describe it as 'Placeholder' or 'Basic boilerplate'.

**Project File Structure:**
{file_list}

**Response Format:**
You *must* respond *only* with a Python dictionary. The keys must be the filenames (e.g., 'main.py') and the values must be the new one-sentence descriptions.

**Example Response:**
{{
    "main.py": "Main entry point to run the application.",
    "config.py": "Stores configuration variables like API keys.",
    "README.md": "Basic boilerplate documentation.",
    "requirements.txt": "Placeholder. No external libraries needed.",
    "core/__init__.py": "# Makes 'core' a Python package",
    "core/logic.py": "Contains the core function to process the data.",
    "utils/__init__.py": "# Makes 'utils' a Python package",
    "utils/helpers.py": "Placeholder. No helper functions needed.",
    "ui/__init__.py": "# Makes 'ui' a Python package",
    "ui/display.py": "Contains the function to print the output."
}}
"""
    return prompt.strip()


def get_coder_system_prompt():

    prompt = """
You are an expert Python developer. Your *only* job is to write complete, correct, and production-ready code for a *single file*.

**Rules:**
1.  You *must* respond *only* with the raw code for the file requested.
2.  Do *not* write *any* explanations, apologies, or text before or after the code.
3.  Do *not* use Markdown (e.g., ```python ... ```).
4.  Ensure the code is complete and functional.
5.  If the task is 'Placeholder', just write a simple comment (e.g., '# This file is a placeholder.')
"""
    return prompt.strip()


def get_coder_user_prompt(project_plan, file_name):

    if file_name not in project_plan["files"]:
        return f"Error: File '{file_name}' not found in project plan."

    task_description = project_plan["files"][file_name]
    plan_context = "\n".join([f"- {f}: {desc}" for f, desc in project_plan["files"].items()])

    prompt = f"""
**Overall Project Plan:**
{plan_context}

---

**Your Specific Task:**
Write the *complete code* for the file: `{file_name}`
**File Description:** "{task_description}"
"""
    return prompt.strip()
