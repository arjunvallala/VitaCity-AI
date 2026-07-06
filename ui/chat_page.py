"""
VitaCity AI — Chat Page
Smart conversational AI interface with RAG, multimodal support, and scenario buttons.
"""

import time
import streamlit as st
from PIL import Image

from core.gemini_client import get_gemini_client
from core.rag_engine import get_rag_engine
from data.knowledge_base import DOMAIN_COLORS, DOMAIN_ICONS, ALL_DOMAINS
from ui.theme import page_hero_html, confidence_badge_html, domain_badge_html
from ui.components import render_chat_message, render_sources, render_recommendations


# ── Quick Scenario Buttons ────────────────────────────────────────────────────

SCENARIOS = [
    {
        "icon": "🚌",
        "label": "Traffic Congestion",
        "query": "What are the top 3 causes of traffic congestion in our district and what are the most cost-effective solutions?",
        "domain": "Urban Mobility & Transportation",
    },
    {
        "icon": "🌿",
        "label": "Carbon Reduction",
        "query": "How can we reduce our city's carbon footprint by 20% in 5 years? Give me a phased implementation plan with cost estimates.",
        "domain": "Environmental Sustainability & Climate Resilience",
    },
    {
        "icon": "🚨",
        "label": "Emergency Response",
        "query": "Which neighborhoods have the lowest emergency response times and what targeted investments will improve them most?",
        "domain": "Public Safety & Emergency Preparedness",
    },
    {
        "icon": "🏥",
        "label": "Healthcare Access",
        "query": "Where are the healthcare deserts in our city and what programs best address gaps in primary care access?",
        "domain": "Healthcare Access & Wellness",
    },
    {
        "icon": "♻️",
        "label": "Waste Reduction ROI",
        "query": "What waste reduction programs have the highest return on investment and how do we scale them citywide?",
        "domain": "Waste Management & Resource Optimization",
    },
    {
        "icon": "🏛️",
        "label": "Citizen Engagement",
        "query": "How do we increase citizen participation in local governance from 16% to 35% within 24 months?",
        "domain": "Citizen Engagement & Public Services",
    },
]


def _init_session():
    """Initialize chat session state."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_sources" not in st.session_state:
        st.session_state.chat_sources = {}
    if "chat_metadata" not in st.session_state:
        st.session_state.chat_metadata = {}
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = ""
    if "auto_send" not in st.session_state:
        st.session_state.auto_send = False
    if "chat_domain_filter" not in st.session_state:
        st.session_state.chat_domain_filter = "All Domains"
    if "image_context" not in st.session_state:
        st.session_state.image_context = None
    if "_last_uploaded_filename" not in st.session_state:
        st.session_state["_last_uploaded_filename"] = None


def _send_query(user_message: str, domain_filter: str, uploaded_image=None):
    """Process user message through RAG + Gemini and update history."""
    if not user_message.strip():
        return

    client = get_gemini_client()
    rag = get_rag_engine()

    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_message,
    })

    # Handle image upload
    if uploaded_image is not None:
        with st.spinner("🔍 Analyzing image with VitaCity AI Vision..."):
            time.sleep(0.3)
            image_result = client.analyze_image(uploaded_image, context=user_message)

            # Format image analysis as markdown
            severity_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(
                image_result.get("severity", "Medium"), "🟡"
            )
            score = image_result.get("priority_score", 5)
            answer_md = f"""
## 🖼️ Urban Issue Analysis Report

**Issue Detected:** {image_result.get('issue_detected', 'Urban infrastructure issue')}
**Severity:** {severity_emoji} {image_result.get('severity', 'Medium')} | **Priority Score:** {score}/10

---

### 📋 Description
{image_result.get('description', 'Infrastructure issue detected requiring city attention.')}

### ⚡ Immediate Actions Required
{chr(10).join(f"- {a}" for a in image_result.get('immediate_actions', []))}

### 🏢 Responsible Department
{image_result.get('responsible_department', 'Public Works')}

### 💰 Cost Estimate
{image_result.get('cost_estimate', 'To be determined after site inspection')}

### ⏱️ Expected Timeline
{image_result.get('timeline', '1-4 weeks depending on severity')}
"""
            ai_response = {
                "answer": answer_md,
                "confidence": image_result.get("confidence", 0.82),
                "domain": "Public Safety & Emergency Preparedness",
                "key_recommendations": image_result.get("immediate_actions", [])[:3],
                "sources_used": ["Urban Infrastructure Assessment", "Public Works Standards"],
                "predicted_impact": f"Priority {score}/10 issue. Prompt remediation prevents escalating costs and safety risks.",
                "follow_up_questions": [
                    "Are there other similar issues in this neighborhood?",
                    "When was the last infrastructure inspection in this area?",
                ],
            }
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer_md,
            })
            idx = len(st.session_state.chat_history) - 1
            st.session_state.chat_metadata[idx] = {
                "confidence": ai_response["confidence"],
                "domain": ai_response["domain"],
            }
            st.session_state.chat_sources[idx] = []
            st.session_state.image_context = None
            return

    # RAG retrieval
    with st.spinner("🧠 Retrieving knowledge context..."):
        rag_context, retrieved_chunks = rag.retrieve_and_format(
            query=user_message,
            domain_filter=domain_filter if domain_filter != "All Domains" else None,
            top_k=5,
        )

    # Gemini inference
    with st.spinner("✨ Generating AI insights..."):
        time.sleep(0.2)
        history_for_context = [
            msg for msg in st.session_state.chat_history[:-1]  # exclude the user message we just added
            if msg["role"] in ("user", "assistant")
        ][-8:]  # keep last 8 for context

        result = client.chat(
            user_message=user_message,
            rag_context=rag_context,
            chat_history=history_for_context,
        )

    answer = result.get("answer", "I was unable to generate a response. Please try again.")

    # Append AI message
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer,
    })
    ai_idx = len(st.session_state.chat_history) - 1

    # Store metadata and sources
    st.session_state.chat_metadata[ai_idx] = {
        "confidence": result.get("confidence", 0.80),
        "domain": result.get("domain", "General"),
        "predicted_impact": result.get("predicted_impact", ""),
        "follow_up_questions": result.get("follow_up_questions", []),
        "key_recommendations": result.get("key_recommendations", []),
    }
    st.session_state.chat_sources[ai_idx] = retrieved_chunks


def render_chat_page():
    """Main chat page renderer."""
    _init_session()

    # Pre-select domain filter before widget instantiation if pending scenario click
    if "next_domain_filter" in st.session_state:
        st.session_state.chat_domain_filter = st.session_state.next_domain_filter
        del st.session_state.next_domain_filter

    # Page header
    st.markdown(
        page_hero_html(
            title="VitaCity AI Chat",
            subtitle="Conversational Decision Intelligence · Powered by Gemini + RAG",
            icon="🤖",
        ),
        unsafe_allow_html=True,
    )

    # ── Layout: Main chat | Right sidebar ─────────────────────────────────────
    chat_col, sidebar_col = st.columns([3, 1])

    with sidebar_col:
        _render_chat_sidebar()

    with chat_col:
        # Domain filter
        domain_filter = st.selectbox(
            "Filter by Domain",
            ["All Domains"] + ALL_DOMAINS,
            key="chat_domain_filter",
            label_visibility="collapsed",
            help="Restrict RAG retrieval to a specific urban domain",
        )

        # ── Quick Scenarios ────────────────────────────────────────────────
        st.markdown(
            '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">⚡ Quick Scenarios</div>',
            unsafe_allow_html=True,
        )

        scenario_cols = st.columns(3)
        for i, scenario in enumerate(SCENARIOS):
            with scenario_cols[i % 3]:
                btn_label = f"{scenario['icon']} {scenario['label']}"
                if st.button(btn_label, key=f"scenario_{i}", use_container_width=True):
                    # Clear previous chat history to avoid confusing scrolling issues
                    st.session_state.chat_history = []
                    st.session_state.chat_sources = {}
                    st.session_state.chat_metadata = {}
                    st.session_state.pending_query = scenario["query"]
                    st.session_state.auto_send = True
                    # Sync the domain filter dropdown with the scenario's domain via next_domain_filter key
                    st.session_state.next_domain_filter = scenario["domain"]
                    st.rerun()

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

        # ── Chat History ────────────────────────────────────────────────────
        if not st.session_state.chat_history:
            st.markdown(
                """
                <div style="text-align:center; padding:60px 20px; color:var(--text-muted);">
                  <div style="font-size:48px; margin-bottom:16px;">🏙️</div>
                  <div style="font-size:16px; font-weight:600; color:var(--text-secondary); margin-bottom:8px;">
                    Welcome to VitaCity AI
                  </div>
                  <div style="font-size:13px; line-height:1.6;">
                    Ask any question about urban mobility, environment, safety, healthcare,
                    waste management, or citizen services. Use a scenario button above to
                    see a live demo.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            chat_container = st.container()
            with chat_container:
                for idx, message in enumerate(st.session_state.chat_history):
                    role = message["role"]
                    content = message["content"]
                    metadata = st.session_state.chat_metadata.get(idx)
                    sources = st.session_state.chat_sources.get(idx, [])

                    render_chat_message(role, content, metadata if role == "assistant" else None)

                    if role == "assistant" and metadata:
                        # Key recommendations
                        recs = metadata.get("key_recommendations", [])
                        if recs:
                            render_recommendations(recs)

                        # Sources
                        if sources:
                            render_sources(sources)

                        # Impact & Follow-up
                        impact = metadata.get("predicted_impact", "")
                        follow_ups = metadata.get("follow_up_questions", [])
                        if impact or follow_ups:
                            with st.expander("🔮 Impact Prediction & Follow-up Questions", expanded=False):
                                if impact:
                                    st.markdown(
                                        f'<div style="background:rgba(76,201,240,0.06); border:1px solid rgba(76,201,240,0.15); '
                                        f'border-radius:8px; padding:12px 16px; font-size:13px; color:var(--text-primary);">'
                                        f'📈 <strong>Predicted Impact:</strong> {impact}</div>',
                                        unsafe_allow_html=True,
                                    )
                                if follow_ups:
                                    st.markdown(
                                        '<div style="margin-top:10px; font-size:12px; color:var(--text-muted);">💡 Related Questions:</div>',
                                        unsafe_allow_html=True,
                                    )
                                    for fq in follow_ups:
                                        if st.button(f"→ {fq}", key=f"followup_{idx}_{hash(fq)}", use_container_width=True):
                                            st.session_state.pending_query = fq
                                            st.session_state.auto_send = True
                                            st.rerun()

                        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

        # ── Image Upload ────────────────────────────────────────────────────
        with st.expander("📸 Upload Image for Urban Issue Analysis", expanded=False):
            st.markdown(
                '<div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">'
                'Upload a photo of a pothole, waste dump, flood area, or other urban issue for AI analysis.</div>',
                unsafe_allow_html=True,
            )
            uploaded_file = st.file_uploader(
                "Drop image here",
                type=["jpg", "jpeg", "png", "webp"],
                key="image_upload",
                label_visibility="collapsed",
            )
            if uploaded_file is not None:
                # Only update image_context when a NEW file is selected
                if st.session_state.get("_last_uploaded_filename") != uploaded_file.name:
                    st.session_state["_last_uploaded_filename"] = uploaded_file.name
                    img = Image.open(uploaded_file)
                    st.session_state.image_context = img
                img_to_show = st.session_state.get("image_context")
                if img_to_show is not None:
                    st.image(img_to_show, caption="Uploaded image — will be analysed with your next message", use_container_width=True)
            else:
                # No file selected — clear stale image_context so it can't bleed into text queries
                st.session_state.image_context = None
                st.session_state["_last_uploaded_filename"] = None

        # ── Input Row ────────────────────────────────────────────────────────
        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        # Handle pending query from scenario buttons / follow-ups
        default_val = st.session_state.get("pending_query", "")
        auto_send = st.session_state.get("auto_send", False)
        if default_val:
            st.session_state.pending_query = ""
        if auto_send:
            st.session_state.auto_send = False

        # ── Auto-send: triggered by scenario buttons and follow-up clicks ──
        # NOTE: never pass image_context for button-triggered queries
        if auto_send and default_val.strip():
            _send_query(default_val.strip(), domain_filter, uploaded_image=None)
            st.rerun()

        input_col, btn_col, clear_col = st.columns([8, 1, 1])

        with input_col:
            user_input = st.text_input(
                "Ask VitaCity AI...",
                value=default_val,
                placeholder="e.g. How can we reduce traffic congestion in the Riverside district?",
                key="chat_input",
                label_visibility="collapsed",
            )

        with btn_col:
            send_clicked = st.button("Send", key="send_btn", type="primary", use_container_width=True)

        with clear_col:
            if st.button("🗑️", key="clear_btn", use_container_width=True, help="Clear conversation"):
                st.session_state.chat_history = []
                st.session_state.chat_sources = {}
                st.session_state.chat_metadata = {}
                st.session_state.image_context = None
                st.rerun()

        # Process on manual Send button click
        if send_clicked and user_input.strip():
            image = st.session_state.get("image_context")
            _send_query(user_input.strip(), domain_filter, uploaded_image=image)
            st.session_state.image_context = None  # clear after use
            st.rerun()


def _render_chat_sidebar():
    """Render the right sidebar for the chat page."""
    st.markdown(
        '<div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">🔧 AI Settings</div>',
        unsafe_allow_html=True,
    )

    client = get_gemini_client()
    rag = get_rag_engine()

    # API Status
    api_status = "🟢 Connected" if client.is_configured else "🟡 Demo Mode"
    api_color = "#4ADE80" if client.is_configured else "#FBBF24"
    st.markdown(
        f'<div style="font-size:12px; color:{api_color}; font-weight:600; margin-bottom:4px;">{api_status}</div>',
        unsafe_allow_html=True,
    )

    model_name = "gemini-2.0-flash" if client.is_configured else "Demo Mode"
    st.markdown(
        f'<div style="font-size:11px; color:var(--text-muted);">Model: {model_name}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

    # RAG Stats
    st.markdown(
        f"""
        <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:10px; padding:12px 14px; margin-bottom:12px;">
          <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">RAG Engine</div>
          <div style="font-size:18px; font-weight:700; color:#4ADE80;">{rag.chunk_count}</div>
          <div style="font-size:11px; color:var(--text-muted);">Knowledge Chunks</div>
          <div style="margin-top:6px; font-size:11px; color:var(--text-muted);">6 Urban Domains · TF-IDF</div>
          <div style="font-size:11px; color:#4ADE80; margin-top:2px;">{'✓ Index Ready' if rag.is_ready else '⚠ Index Failed'}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Session stats
    total_msgs = len(st.session_state.get("chat_history", []))
    ai_msgs = sum(1 for m in st.session_state.get("chat_history", []) if m["role"] == "assistant")

    st.markdown(
        f"""
        <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:10px; padding:12px 14px;">
          <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">Session Stats</div>
          <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="font-size:12px; color:var(--text-secondary);">Messages</span>
            <span style="font-size:12px; font-weight:600; color:var(--text-primary);">{total_msgs}</span>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="font-size:12px; color:var(--text-secondary);">AI Responses</span>
            <span style="font-size:12px; font-weight:600; color:#4CC9F0;">{ai_msgs}</span>
          </div>
          <div style="display:flex; justify-content:space-between;">
            <span style="font-size:12px; color:var(--text-secondary);">Domains Active</span>
            <span style="font-size:12px; font-weight:600; color:#A78BFA;">6</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Demo mode notice
    if not client.is_configured:
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.info(
            "**Demo Mode Active**\n\n"
            "Add your `GEMINI_API_KEY` to `.env` for live Gemini responses. "
            "Demo mode shows curated, realistic examples.",
            icon="ℹ️",
        )
