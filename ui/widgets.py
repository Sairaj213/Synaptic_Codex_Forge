import streamlit as st
import pandas as pd
import os

def draw_status_monitor():

    st.subheader("Live Agent Monitor")
    log_container = st.container(height=300, border=True)

    if 'generation_log' not in st.session_state or not st.session_state.generation_log:

        log_container.info("Agent logs will appear here...")

        return

    for log_entry in reversed(st.session_state.generation_log):
        if log_entry.startswith("✅"):
            log_container.success(log_entry)
        elif log_entry.startswith("Error") or log_entry.startswith("❌"):
            log_container.error(log_entry)
        elif log_entry.startswith("---"):
            log_container.markdown(f"**{log_entry}**")
        else:
            log_container.info(log_entry)

def draw_code_viewer():

    st.subheader("Generated Code Viewer")

    generated_code = st.session_state.get('generated_code', {})

    if not generated_code:
        st.info("No code has been generated yet. Run the agent from the 'Run' tab.")
        return

    file_list = list(generated_code.keys())
    selected_file = st.selectbox("Select a file to view:", file_list)

    if selected_file:
        st.code(generated_code[selected_file], language="python")

def draw_project_stats_and_download():

    st.subheader("Project Stats")
    stats = st.session_state.get('project_stats', {})

    if not stats or stats["total_files"] == 0:
        st.info("No stats to display. Run the agent to generate a project.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Files", stats.get("total_files", 0))
    col2.metric("Total Lines of Code", stats.get("total_lines", 0))
    col3.metric("Time Taken (sec)", stats.get("time_taken", 0.0))

    st.subheader("Generated Files")
    files_df = pd.DataFrame(stats.get("files_list", []))
    st.dataframe(files_df, use_container_width=True)
    st.subheader("Download Project")
    zip_path = st.session_state.get('project_zip_path')

    if zip_path and os.path.exists(zip_path):
        with open(zip_path, "rb") as f:
            st.download_button(
                label="Download Project as .zip",
                data=f,
                file_name=os.path.basename(zip_path),
                mime="application/zip",
            )
    else:
        st.warning("No project ZIP file found. Please run the generation pipeline first.")
