"""
VitaCity AI — Responsible AI Page
Explainability, data sources, model transparency, bias mitigation, and confidence methodology.
"""

import streamlit as st
import plotly.graph_objects as go

from ui.theme import page_hero_html
from ui.components import make_bar_chart, make_donut_chart, CHART_BASE
from core.rag_engine import get_rag_engine
from data.knowledge_base import DOMAIN_COLORS, DOMAIN_ICONS, ALL_DOMAINS


def _render_how_it_works():
    """Render the RAG architecture explanation."""
    st.markdown(
        """
        <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:16px; padding:24px 28px; margin-bottom:20px;">
          <div style="font-size:14px; font-weight:700; color:var(--text-primary); margin-bottom:16px;">🔄 How VitaCity AI Works</div>

          <div style="display:flex; gap:0; align-items:stretch; flex-wrap:wrap;">

            <div style="flex:1; min-width:140px; padding:16px; background:rgba(76,201,240,0.06);
              border:1px solid rgba(76,201,240,0.2); border-radius:12px; margin:4px; text-align:center;">
              <div style="font-size:28px; margin-bottom:8px;">💬</div>
              <div style="font-size:12px; font-weight:700; color:#4CC9F0; margin-bottom:6px;">1. USER QUERY</div>
              <div style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                Natural language question from citizen, planner, or official
              </div>
            </div>

            <div style="display:flex; align-items:center; padding:0 4px; color:var(--text-muted); font-size:20px;">→</div>

            <div style="flex:1; min-width:140px; padding:16px; background:rgba(167,139,250,0.06);
              border:1px solid rgba(167,139,250,0.2); border-radius:12px; margin:4px; text-align:center;">
              <div style="font-size:28px; margin-bottom:8px;">🔍</div>
              <div style="font-size:12px; font-weight:700; color:#A78BFA; margin-bottom:6px;">2. RAG RETRIEVAL</div>
              <div style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                TF-IDF search finds top-5 relevant knowledge chunks from 35+ curated sources
              </div>
            </div>

            <div style="display:flex; align-items:center; padding:0 4px; color:var(--text-muted); font-size:20px;">→</div>

            <div style="flex:1; min-width:140px; padding:16px; background:rgba(74,222,128,0.06);
              border:1px solid rgba(74,222,128,0.2); border-radius:12px; margin:4px; text-align:center;">
              <div style="font-size:28px; margin-bottom:8px;">🧠</div>
              <div style="font-size:12px; font-weight:700; color:#4ADE80; margin-bottom:6px;">3. GEMINI LLM</div>
              <div style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                Gemini 2.0 Flash synthesizes context + knowledge into structured city intelligence
              </div>
            </div>

            <div style="display:flex; align-items:center; padding:0 4px; color:var(--text-muted); font-size:20px;">→</div>

            <div style="flex:1; min-width:140px; padding:16px; background:rgba(251,191,36,0.06);
              border:1px solid rgba(251,191,36,0.2); border-radius:12px; margin:4px; text-align:center;">
              <div style="font-size:28px; margin-bottom:8px;">📊</div>
              <div style="font-size:12px; font-weight:700; color:#FBBF24; margin-bottom:6px;">4. STRUCTURED OUTPUT</div>
              <div style="font-size:11px; color:var(--text-muted); line-height:1.5;">
                Answer + confidence score + citations + recommendations + predicted impact
              </div>
            </div>

          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_knowledge_base_stats():
    """Show knowledge base breakdown."""
    rag = get_rag_engine()

    from data.knowledge_base import KNOWLEDGE_BASE

    # Count by domain
    domain_counts = {}
    for chunk in KNOWLEDGE_BASE:
        d = chunk["domain"]
        domain_counts[d] = domain_counts.get(d, 0) + 1

    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">📚 Knowledge Base Composition</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        fig = make_donut_chart(
            labels=[d.split(" &")[0].split(" (")[0][:25] for d in domain_counts.keys()],
            values=list(domain_counts.values()),
            title="Chunks by Domain",
            height=280,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        for domain, count in domain_counts.items():
            icon = DOMAIN_ICONS.get(domain, "📄")
            color = DOMAIN_COLORS.get(domain, "#4CC9F0")
            short_name = domain.split(" &")[0][:28]
            pct = int(count / len(KNOWLEDGE_BASE) * 100)
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                  <div style="width:24px; text-align:center; font-size:16px;">{icon}</div>
                  <div style="flex:1;">
                    <div style="font-size:12px; color:var(--text-primary); font-weight:500;">{short_name}</div>
                    <div style="background:rgba(255,255,255,0.05); border-radius:4px; height:4px; margin-top:4px; overflow:hidden;">
                      <div style="background:{color}; height:100%; width:{pct * 3}%; border-radius:4px;"></div>
                    </div>
                  </div>
                  <div style="font-size:12px; font-weight:700; color:{color}; min-width:24px; text-align:right;">{count}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div style="background:rgba(76,201,240,0.06); border:1px solid rgba(76,201,240,0.15);
              border-radius:10px; padding:14px 16px; margin-top:12px;">
              <div style="font-size:24px; font-weight:800; color:#4CC9F0;">{len(KNOWLEDGE_BASE)}</div>
              <div style="font-size:12px; color:var(--text-muted);">Total Knowledge Chunks</div>
              <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">
                TF-IDF indexed · {len(domain_counts)} domains · Bigram features
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_confidence_methodology():
    """Explain how confidence scores are calculated."""
    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">🎯 Confidence Score Methodology</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:12px; padding:20px;">
              <div style="font-size:13px; font-weight:700; color:var(--text-primary); margin-bottom:12px;">
                📐 Confidence Calculation
              </div>

              <div style="font-size:12px; color:var(--text-secondary); line-height:1.8;">
                Confidence scores reflect three combined factors:
              </div>

              <div style="margin-top:12px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                  <span style="font-size:12px; color:var(--text-secondary);">RAG Retrieval Relevance</span>
                  <span style="font-size:12px; font-weight:600; color:#4CC9F0;">40%</span>
                </div>
                <div style="background:rgba(255,255,255,0.05); border-radius:4px; height:4px; margin-bottom:12px;">
                  <div style="background:#4CC9F0; height:100%; width:40%; border-radius:4px;"></div>
                </div>

                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                  <span style="font-size:12px; color:var(--text-secondary);">Knowledge Base Coverage</span>
                  <span style="font-size:12px; font-weight:600; color:#A78BFA;">35%</span>
                </div>
                <div style="background:rgba(255,255,255,0.05); border-radius:4px; height:4px; margin-bottom:12px;">
                  <div style="background:#A78BFA; height:100%; width:35%; border-radius:4px;"></div>
                </div>

                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                  <span style="font-size:12px; color:var(--text-secondary);">Source Quality Score</span>
                  <span style="font-size:12px; font-weight:600; color:#4ADE80;">25%</span>
                </div>
                <div style="background:rgba(255,255,255,0.05); border-radius:4px; height:4px;">
                  <div style="background:#4ADE80; height:100%; width:25%; border-radius:4px;"></div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:12px; padding:20px;">
              <div style="font-size:13px; font-weight:700; color:var(--text-primary); margin-bottom:12px;">
                📊 Confidence Thresholds
              </div>

              <div style="margin-bottom:12px;">
                <div style="display:flex; align-items:center; gap:10px; padding:10px 12px;
                  background:rgba(74,222,128,0.08); border:1px solid rgba(74,222,128,0.2);
                  border-radius:8px; margin-bottom:8px;">
                  <div style="width:10px; height:10px; background:#4ADE80; border-radius:50%;"></div>
                  <div>
                    <div style="font-size:12px; font-weight:600; color:#4ADE80;">High Confidence ≥ 85%</div>
                    <div style="font-size:11px; color:var(--text-muted);">Strong evidence base, multiple aligned sources</div>
                  </div>
                </div>

                <div style="display:flex; align-items:center; gap:10px; padding:10px 12px;
                  background:rgba(251,191,36,0.08); border:1px solid rgba(251,191,36,0.2);
                  border-radius:8px; margin-bottom:8px;">
                  <div style="width:10px; height:10px; background:#FBBF24; border-radius:50%;"></div>
                  <div>
                    <div style="font-size:12px; font-weight:600; color:#FBBF24;">Medium Confidence 70–84%</div>
                    <div style="font-size:11px; color:var(--text-muted);">Good coverage, some uncertainty or novelty</div>
                  </div>
                </div>

                <div style="display:flex; align-items:center; gap:10px; padding:10px 12px;
                  background:rgba(249,115,22,0.08); border:1px solid rgba(249,115,22,0.2);
                  border-radius:8px;">
                  <div style="width:10px; height:10px; background:#F97316; border-radius:50%;"></div>
                  <div>
                    <div style="font-size:12px; font-weight:600; color:#F97316;">Low Confidence &lt; 70%</div>
                    <div style="font-size:11px; color:var(--text-muted);">Limited sources, speculative, verify externally</div>
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_model_card():
    """Render model transparency card."""
    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">🤖 Model Transparency Card</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="kpi-card" style="border-top:2px solid #4CC9F0;">
              <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; margin-bottom:8px;">Language Model</div>
              <div style="font-size:16px; font-weight:700; color:var(--text-primary);">Gemini 2.0 Flash</div>
              <div style="font-size:11px; color:var(--text-muted); margin-top:6px;">Google DeepMind</div>
              <div style="font-size:11px; color:var(--text-muted);">Multimodal · Low latency</div>
              <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">Max tokens: 2,048</div>
              <div style="font-size:11px; color:var(--text-muted);">Temperature: 0.4</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="kpi-card" style="border-top:2px solid #A78BFA;">
              <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; margin-bottom:8px;">Retrieval Engine</div>
              <div style="font-size:16px; font-weight:700; color:var(--text-primary);">TF-IDF + Cosine</div>
              <div style="font-size:11px; color:var(--text-muted); margin-top:6px;">scikit-learn</div>
              <div style="font-size:11px; color:var(--text-muted);">Bigram features</div>
              <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">In-memory index</div>
              <div style="font-size:11px; color:var(--text-muted);">Top-K: 5 chunks</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="kpi-card" style="border-top:2px solid #4ADE80;">
              <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; margin-bottom:8px;">Safety Settings</div>
              <div style="font-size:16px; font-weight:700; color:var(--text-primary);">BLOCK_MEDIUM+</div>
              <div style="font-size:11px; color:var(--text-muted); margin-top:6px;">Harassment blocked</div>
              <div style="font-size:11px; color:var(--text-muted);">Hate speech blocked</div>
              <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">Dangerous content blocked</div>
              <div style="font-size:11px; color:#4ADE80;">✓ Safe for public use</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_bias_mitigation():
    """Render bias mitigation and ethical AI notes."""
    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">⚖️ Bias Mitigation & Ethical AI</div>',
        unsafe_allow_html=True,
    )

    bias_items = [
        {
            "icon": "🌍",
            "title": "Geographic Equity",
            "desc": "RAG corpus includes data from both high-income and underserved communities. Recommendations are always checked for equity implications.",
        },
        {
            "icon": "📊",
            "title": "Data Provenance",
            "desc": "All knowledge chunks cite real-world programs (Bogotá BRT, Oslo Vision Zero, Singapore water management) with documented outcomes.",
        },
        {
            "icon": "🔍",
            "title": "Hallucination Mitigation",
            "desc": "RAG grounding anchors responses to verified knowledge. Confidence scores flag areas of lower certainty for human expert review.",
        },
        {
            "icon": "🔒",
            "title": "Privacy by Design",
            "desc": "No personal data is collected or used. All metrics are population-level aggregates. Image analysis is processed in-session only.",
        },
        {
            "icon": "👥",
            "title": "Human-in-the-Loop",
            "desc": "VitaCity AI provides decision support, not decision-making. All outputs should be reviewed by qualified city professionals.",
        },
        {
            "icon": "🔄",
            "title": "Continuous Improvement",
            "desc": "Knowledge base is versioned and updated quarterly. Model performance is monitored for drift using a held-out evaluation set.",
        },
    ]

    cols = st.columns(2)
    for i, item in enumerate(bias_items):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="kpi-card" style="margin-bottom:8px; padding:14px 16px;">
                  <div style="display:flex; gap:10px; align-items:flex-start;">
                    <div style="font-size:20px;">{item['icon']}</div>
                    <div>
                      <div style="font-size:13px; font-weight:600; color:var(--text-primary);">{item['title']}</div>
                      <div style="font-size:12px; color:var(--text-muted); margin-top:4px; line-height:1.5;">{item['desc']}</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_data_sources():
    """Render data sources and citations."""
    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">📖 Knowledge Sources & References</div>',
        unsafe_allow_html=True,
    )

    sources = [
        ("🚌", "Transportation",
         "NFPA 1710, ITDP BRT Standard, NACTO Urban Street Design Guide, US DOT Smart Mobility Challenge, Bogotá TransMilenio Impact Studies"),
        ("🌿", "Environment",
         "IPCC AR6 Report, C40 Cities Climate Action, WHO Air Quality Guidelines 2021, UN-Habitat Urban Climate Resilience Framework"),
        ("🚨", "Public Safety",
         "FBI Uniform Crime Reporting, NFPA Emergency Response Standards, FEMA Community Resilience Framework, Oslo Vision Zero Annual Reports"),
        ("🏥", "Healthcare",
         "WHO Primary Health Care Indicators, CDC Chronic Disease Prevention, HRSA Health Professional Shortage Area Data, KFF Health System Tracker"),
        ("♻️", "Waste Management",
         "USEPA Waste Diversion Data, Zero Waste International Alliance, Ellen MacArthur Foundation Circular Economy Reports, Basel Convention Guidelines"),
        ("🏛️", "Civic Engagement",
         "OECD Digital Government Framework, Participatory Budgeting Project Global Database, GovLab Open Data Impact, UN e-Government Survey 2022"),
    ]

    for icon, domain, refs in sources:
        with st.expander(f"{icon} {domain} Sources", expanded=False):
            st.markdown(
                f'<div style="font-size:12px; color:var(--text-secondary); line-height:1.8;">{refs}</div>',
                unsafe_allow_html=True,
            )


def _render_limitations():
    """Render known limitations."""
    st.markdown(
        """
        <div style="background:rgba(249,115,22,0.06); border:1px solid rgba(249,115,22,0.2);
          border-radius:12px; padding:20px 24px; margin-top:8px;">
          <div style="font-size:13px; font-weight:700; color:#F97316; margin-bottom:12px;">
            ⚠️ Known Limitations
          </div>
          <ul style="font-size:12px; color:var(--text-secondary); line-height:2; margin:0; padding-left:18px;">
            <li>Knowledge base covers urban contexts primarily from North America and Western Europe; results may differ for Global South cities.</li>
            <li>Mock city data (Metro Vitacity) is synthetic. Quantitative projections should be recalibrated with your city's actual data.</li>
            <li>Decision Simulator impact scores are heuristic estimates, not econometric models. Engage domain experts for major policy decisions.</li>
            <li>LLM responses may occasionally contain plausible-sounding but inaccurate statistics. Always verify critical numbers with primary sources.</li>
            <li>Image analysis is best-effort. Critical infrastructure assessments require in-person inspection by qualified engineers.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_responsible_ai_page():
    """Main Responsible AI page renderer."""

    st.markdown(
        page_hero_html(
            title="Responsible AI Framework",
            subtitle="Transparency, Explainability & Ethical AI in Urban Decision Support",
            icon="⚖️",
        ),
        unsafe_allow_html=True,
    )

    _render_how_it_works()

    st.markdown("---")
    _render_knowledge_base_stats()

    st.markdown("---")
    _render_confidence_methodology()

    st.markdown("---")
    _render_model_card()

    st.markdown("---")
    _render_bias_mitigation()

    st.markdown("---")
    _render_data_sources()

    st.markdown("---")
    _render_limitations()

    # Google Cloud Best Practices badge
    st.markdown(
        """
        <div style="background:rgba(76,201,240,0.05); border:1px solid rgba(76,201,240,0.15);
          border-radius:12px; padding:16px 20px; margin-top:16px; display:flex; align-items:center; gap:16px;">
          <div style="font-size:28px;">☁️</div>
          <div>
            <div style="font-size:13px; font-weight:700; color:var(--text-primary);">Google Cloud Best Practices</div>
            <div style="font-size:12px; color:var(--text-muted); margin-top:4px;">
              VitaCity AI follows Google Cloud's Responsible AI Principles: Socially Beneficial · Fair · Accountable ·
              Private · Safe · Scientifically Rigorous · Accessible
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
