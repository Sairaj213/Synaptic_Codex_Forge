import streamlit as st
from utils.session_state import initialize_state
from ui.sidebar import draw_sidebar
from ui.tabs_layout import draw_tabs
from core.model import load_model
from core.agent import run_generation_pipeline

st.set_page_config(
    page_title="Synaptic Codex Forge",
    page_icon="🤖",
    layout="wide"
)
initialize_state()
project_name, llm_params = draw_sidebar()

st.title("🤖 Synaptic Codex Forge")
st.markdown("Powered by `mistralai/Mistral-7B-Instruct-v0.3`")

model_loaded = False
with st.spinner("Loading Mistral-7B model... This may take a moment."):
    model, tokenizer = load_model()

if model is None or tokenizer is None:
    st.error("Model failed to load. Please check your setup and network connection.")
else:
    st.success("Model loaded successfully!")
    model_loaded = True

st.header("What do you want to build?")
user_request = st.text_area(
    "Describe your project in detail:",
    height=150,
    placeholder="e.g., 'A Python app that uses Flask to serve a single 'Hello World' API endpoint...'"
)

if model_loaded:
    if st.button("🚀 Generate Project", type="primary", use_container_width=True):
        if not user_request:
            st.warning("Please describe your project first.")
        elif not project_name:
            st.warning("Please enter a project name in the sidebar.")
        else:
            st.subheader("Live Agent Monitor")
            log_placeholder = st.container(height=400, border=True)
            run_generation_pipeline(
                user_request,
                project_name,
                model,
                tokenizer,
                llm_params,
                log_placeholder  
            )
            st.rerun()
    st.divider()
draw_tabs()
