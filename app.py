"""
VitaCity AI — Main Application Entry Point
Streamlit app with sidebar navigation and page routing.

Run locally:
    streamlit run app.py

Deploy to Cloud Run:
    gcloud builds submit --config cloudbuild.yaml
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv

# ── Load environment variables ─────────────────────────────────────────────────
load_dotenv()

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="VitaCity AI — Decision Intelligence Platform",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/vitacityai",
        "Report a bug": None,
        "About": "VitaCity AI — Powered by Gemini + RAG | Built for Google Cloud Hackathon 2026",
    },
)

# ── Inject CSS theme ───────────────────────────────────────────────────────────
from ui.theme import inject_css, sidebar_logo_html
inject_css()

# ── Page imports ───────────────────────────────────────────────────────────────
from ui.chat_page import render_chat_page
from ui.dashboard_page import render_dashboard_page
from ui.simulator_page import render_simulator_page
from ui.responsible_ai_page import render_responsible_ai_page


# ── Navigation configuration ───────────────────────────────────────────────────
NAV_PAGES = {
    "🤖  AI Chat Assistant": "chat",
    "📊  City Dashboard": "dashboard",
    "🎯  Decision Simulator": "simulator",
    "⚖️  Responsible AI": "responsible_ai",
}


def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        # Logo
        st.markdown(sidebar_logo_html(), unsafe_allow_html=True)

        # Navigation
        st.markdown(
            '<div style="font-size:10px; color:var(--text-muted); text-transform:uppercase; '
            'letter-spacing:0.1em; padding:0 8px; margin-bottom:6px;">Navigation</div>',
            unsafe_allow_html=True,
        )

        selected_page = st.radio(
            "Navigation",
            list(NAV_PAGES.keys()),
            key="nav_radio",
            label_visibility="collapsed",
        )

        # System Status
        st.markdown(
            """
            <div style="position:absolute; bottom:0; left:0; right:0; padding:16px;
              border-top:1px solid var(--border-color); background:var(--bg-secondary);">
            """,
            unsafe_allow_html=True,
        )

        from core.gemini_client import get_gemini_client
        from core.rag_engine import get_rag_engine

        client = get_gemini_client()
        rag = get_rag_engine()

        api_ok = client.is_configured
        rag_ok = rag.is_ready

        api_color = "#4ADE80" if api_ok else "#FBBF24"
        api_label = "Gemini API: Live" if api_ok else "Gemini API: Demo"
        rag_color = "#4ADE80" if rag_ok else "#EF4444"

        st.markdown(
            f"""
            <div style="font-size:10px; color:var(--text-muted); text-transform:uppercase;
              letter-spacing:0.08em; margin-bottom:8px;">System Status</div>
            <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
              <div style="width:6px; height:6px; background:{api_color}; border-radius:50%;
                animation: pulse-dot 2s infinite;"></div>
              <div style="font-size:11px; color:{api_color};">{api_label}</div>
            </div>
            <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
              <div style="width:6px; height:6px; background:{rag_color}; border-radius:50%;
                animation: pulse-dot 2s infinite;"></div>
              <div style="font-size:11px; color:{rag_color};">RAG Engine: {'Ready' if rag_ok else 'Error'}</div>
            </div>
            <div style="display:flex; align-items:center; gap:6px; margin-bottom:12px;">
              <div style="width:6px; height:6px; background:#4ADE80; border-radius:50%;
                animation: pulse-dot 2s infinite;"></div>
              <div style="font-size:11px; color:#4ADE80;">Metro Vitacity: Online</div>
            </div>
            <div style="font-size:10px; color:var(--text-muted);">
              Powered by Google Gemini ·<br>Built on Google Cloud
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        return selected_page


def main():
    """Main application entry point."""

    # Render sidebar and get selected page
    selected_page = render_sidebar()
    page_key = NAV_PAGES.get(selected_page, "chat")

    # Route to selected page
    if page_key == "chat":
        render_chat_page()
    elif page_key == "dashboard":
        render_dashboard_page()
    elif page_key == "simulator":
        render_simulator_page()
    elif page_key == "responsible_ai":
        render_responsible_ai_page()
    else:
        render_chat_page()


if __name__ == "__main__":
    main()
