import streamlit as st
from config import DEFAULT_LLM_PARAMS, MODEL_ID

def draw_sidebar():

    st.sidebar.title("⚙️ Control Panel")
    st.sidebar.markdown("Configure the agent and LLM parameters.")
    st.sidebar.header("Project Settings")
    project_name = st.sidebar.text_input(
        "Project Name",
        value="my_awesome_project",
        help="The name of the folder for your generated project."
    )

    st.sidebar.header("LLM Parameters")
    st.sidebar.text_input("Model", value=MODEL_ID, disabled=True)

    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=DEFAULT_LLM_PARAMS["temperature"],
        step=0.05,
        help="Controls randomness. Lower is more deterministic, higher is more creative."
    )

    max_new_tokens = st.sidebar.slider(
        "Max New Tokens",
        min_value=512,
        max_value=8192,
        value=DEFAULT_LLM_PARAMS["max_new_tokens"],
        step=256,
        help="Maximum number of tokens the model can generate for each file."
    )

    st.sidebar.header("Agent Controls")
    debug_mode = st.sidebar.checkbox(
        "Debug Mode",
        value=DEFAULT_LLM_PARAMS["debug_mode"],
        help="Show extra debug information in the logs."
    )

    st.sidebar.header("Utility")
    if st.sidebar.button("Clear Session Cache"):
        st.session_state.clear()
        st.rerun()

    llm_params = {
        "temperature": temperature,
        "max_new_tokens": max_new_tokens,
        "debug_mode": debug_mode
    }

    return project_name, llm_params
