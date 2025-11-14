import streamlit as st
from ui.widgets import draw_status_monitor, draw_code_viewer, draw_project_stats_and_download

def draw_tabs():

    tab1, tab2, tab3 = st.tabs([
        "📝 Plan & Monitor",
        "VIEW: Code & Files",
        "📈 Stats & Download"
    ])

    with tab1:
        st.header("Project Plan & Generation Status")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Project Plan")
            plan_container = st.container(height=300, border=True)
            plan = st.session_state.get('project_plan')

            if plan:
                plan_container.json(plan)
            else:
                plan_container.info("The project plan will appear here after generation.")

        with col2:
            draw_status_monitor()

    with tab2:
        st.header("Review Generated Code")
        draw_code_viewer()

    with tab3:
        st.header("Project Statistics & Download")
        draw_project_stats_and_download()
