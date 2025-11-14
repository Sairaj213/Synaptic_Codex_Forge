import os

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
PROJECT_OUTPUT_DIR = "generated_projects"
DEFAULT_PROJECT_STRUCTURE = {
    "folders": [
        "assets",
        "core",
        "utils",
        "ui"
    ],
    "files": {
        "main.py": "Placeholder for main application entry point.",
        "config.py": "Placeholder for project configuration.",
        "README.md": "Placeholder for project documentation.",
        "requirements.txt": "Placeholder for project dependencies.",
        "core/__init__.py": "# Makes 'core' a Python package",
        "core/logic.py": "Placeholder for core business logic.",
        "utils/__init__.py": "# Makes 'utils' a Python package",
        "utils/helpers.py": "Placeholder for utility functions.",
        "ui/__init__.py": "# Makes 'ui' a Python package",
        "ui/display.py": "Placeholder for UI or display logic."
    }
}

DEFAULT_LLM_PARAMS = {
    "temperature": 0.7,
    "max_new_tokens": 4096,
    "debug_mode": True
}
