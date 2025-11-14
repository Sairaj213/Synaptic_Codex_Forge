import streamlit as st

def initialize_state():

    if 'project_plan' not in st.session_state:
        st.session_state.project_plan = None

    if 'generation_log' not in st.session_state:
        st.session_state.generation_log = []

    if 'project_zip_path' not in st.session_state:
        st.session_state.project_zip_path = None

    if 'generated_code' not in st.session_state:
        st.session_state.generated_code = {}

    if 'project_stats' not in st.session_state:
        st.session_state.project_stats = {
            "total_files": 0,
            "total_lines": 0,
            "time_taken": 0.0,
            "files_list": []
        }
