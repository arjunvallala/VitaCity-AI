"""
VitaCity AI — Decision Simulator Page
User inputs a proposed decision; AI scores impact across 5 dimensions
and generates timeline projection + risk analysis.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from core.decision_simulator import simulate_decision, IMPACT_DIMENSIONS
from ui.theme import page_hero_html
from ui.components import (
    make_line_chart, make_bar_chart, make_radar_chart,
    render_kpi_row, CHART_BASE, ACCENT_COLORS,
)
from data.knowledge_base import ALL_DOMAINS


# ── Preset Scenarios ──────────────────────────────────────────────────────────
PRESET_DECISIONS = [
    {
        "label": "🚌 Electric Bus Fleet",
        "text": "Replace all 240 diesel buses with electric buses over 3 years, with overnight depot charging infrastructure.",
        "domain": "Urban Mobility & Transportation",
        "population": 187000,
        "budget": 85.0,
    },
    {
        "label": "☀️ Solar Panel Program",
        "text": "Install solar panels on all 840 municipal buildings and 50 public parking structures to achieve 65% renewable electricity.",
        "domain": "Environmental Sustainability & Climate Resilience",
        "population": 512400,
        "budget": 120.0,
    },
    {
        "label": "🏥 Mobile Health Clinics",
        "text": "Deploy 6 mobile health clinics to serve healthcare deserts in Southpark, Eastfield, and Harbor View districts.",
        "domain": "Healthcare Access & Wellness",
        "population": 125000,
        "budget": 4.2,
    },
    {
        "label": "🌿 Urban Park Expansion",
        "text": "Create 12 new neighborhood parks and plant 50,000 trees across underserved districts to improve green space per capita.",
        "domain": "Environmental Sustainability & Climate Resilience",
        "population": 200000,
        "budget": 22.0,
    },
    {
        "label": "♻️ Smart Recycling Scale-Up",
        "text": "Deploy 1,360 additional smart waste bins with IoT fill sensors and expand composting program to mandatory participation.",
        "domain": "Waste Management & Resource Optimization",
        "population": 512400,
        "budget": 8.5,
    },
    {
        "label": "🏛️ Civic Digital Platform",
        "text": "Launch multilingual civic engagement app, AI-powered 311 chatbot, and participatory budgeting portal for all 12 districts.",
        "domain": "Citizen Engagement & Public Services",
        "population": 512400,
        "budget": 3.8,
    },
]


def _init_simulator_state():
    if "sim_result" not in st.session_state:
        st.session_state.sim_result = None
    if "sim_decision_text" not in st.session_state:
        st.session_state.sim_decision_text = ""


def _render_impact_bars(impact_scores: dict):
    """Render vertical impact bars for all 5 dimensions."""
    cols = st.columns(5)
    for col, (dim, data) in zip(cols, impact_scores.items()):
        with col:
            score = data["score"]
            color = data["color"]
            icon = data["icon"]
            label = data["label"]

            # Color based on positivity
            display_color = color if score >= 0 else "#EF4444"
            bar_height = abs(score)

            st.markdown(
                f"""
                <div class="impact-ring">
                  <div style="font-size:22px; margin-bottom:8px;">{icon}</div>
                  <div style="font-size:11px; font-weight:600; color:var(--text-secondary); text-transform:uppercase;
                    letter-spacing:0.04em; margin-bottom:12px;">{dim}</div>
                  <div style="font-size:36px; font-weight:800; color:{display_color}; line-height:1;">
                    {'+' if score > 0 else ''}{score}
                  </div>
                  <div style="font-size:10px; color:var(--text-muted); margin-top:4px;">{label}</div>
                  <div style="margin-top:12px; background:rgba(255,255,255,0.05); border-radius:4px; height:6px; overflow:hidden;">
                    <div style="background:{display_color}; height:100%; width:{bar_height}%;
                      border-radius:4px; transition:width 0.8s ease;"></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_timeline_chart(timeline: list, height: int = 280) -> go.Figure:
    """Render timeline projection chart."""
    years = [t["year"] for t in timeline]
    impacts = [t["projected_impact"] for t in timeline]
    cumulative = [t["cumulative_benefit"] for t in timeline]
    confidence = [t["confidence"] * 100 for t in timeline]

    fig = go.Figure()

    # Cumulative benefit bars
    fig.add_trace(
        go.Bar(
            x=years,
            y=cumulative,
            name="Cumulative Benefit Index",
            marker=dict(color="#4ADE80", opacity=0.7),
            hovertemplate="%{x}: %{y:.0f} pts<extra></extra>",
            yaxis="y",
        )
    )

    # Confidence line
    fig.add_trace(
        go.Scatter(
            x=years,
            y=confidence,
            name="Forecast Confidence %",
            mode="lines+markers",
            line=dict(color="#4CC9F0", width=2.5, dash="dot"),
            marker=dict(size=7, color="#4CC9F0"),
            hovertemplate="%{x}: %{y:.0f}%<extra></extra>",
            yaxis="y2",
        )
    )

    layout = dict(**CHART_BASE)
    layout["title"] = dict(
        text="Impact Timeline Projection",
        font=dict(color="#F0F6FF", size=14, family="Inter"),
        x=0.01, xanchor="left",
    )
    layout["height"] = height
    layout["barmode"] = "group"
    layout["yaxis"]["title"] = "Benefit Index"
    layout["yaxis2"] = dict(
        title="Confidence %",
        overlaying="y",
        side="right",
        tickfont=dict(color="#4CC9F0", size=10),
        gridcolor="rgba(0,0,0,0)",
        zeroline=False,
        showline=False,
        range=[0, 110],
    )
    layout["legend"] = dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8B9EC5", size=11),
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    )
    fig.update_layout(**layout)
    return fig


def _render_risk_table(risks: list):
    """Render risk assessment table."""
    rows = []
    for r in risks:
        severity_colors = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}
        likelihood_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        rows.append({
            "Risk": r["risk"],
            "Likelihood": f"{likelihood_colors.get(r['likelihood'], '🟡')} {r['likelihood']}",
            "Severity": f"{severity_colors.get(r['severity'], '🟡')} {r['severity']}",
            "Mitigation Strategy": r["mitigation"],
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_simulator_page():
    """Main Decision Simulator page renderer."""
    _init_simulator_state()

    # Page Header
    st.markdown(
        page_hero_html(
            title="Decision Simulator",
            subtitle="Model the Impact of City Decisions Before They're Made",
            icon="🎯",
        ),
        unsafe_allow_html=True,
    )

    # ── Layout: Input | Results ────────────────────────────────────────────
    input_col, result_col = st.columns([1, 2])

    with input_col:
        st.markdown(
            '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">⚡ Quick Presets</div>',
            unsafe_allow_html=True,
        )

        for preset in PRESET_DECISIONS:
            if st.button(preset["label"], key=f"preset_{preset['label']}", use_container_width=True):
                st.session_state.sim_decision_text = preset["text"]
                # Auto-run simulation
                st.session_state.sim_result = simulate_decision(
                    decision_text=preset["text"],
                    domain=preset["domain"],
                    population_affected=preset["population"],
                    budget_millions=preset["budget"],
                    horizon_years=5,
                )
                st.rerun()

        st.markdown("---")
        st.markdown(
            '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">⚙️ Custom Decision</div>',
            unsafe_allow_html=True,
        )

        decision_text = st.text_area(
            "Describe your proposed decision",
            value=st.session_state.sim_decision_text,
            placeholder="e.g. Build 5 new cycling superhighways connecting all major transit hubs to the city center by 2027...",
            height=130,
            key="sim_decision_input",
        )

        selected_domain = st.selectbox(
            "Primary Domain",
            ["All Domains"] + ALL_DOMAINS,
            key="sim_domain_select",
        )

        pop_col, budget_col = st.columns(2)
        with pop_col:
            population = st.number_input(
                "Population Affected",
                min_value=1000,
                max_value=1000000,
                value=100000,
                step=5000,
                key="sim_population",
            )
        with budget_col:
            budget = st.number_input(
                "Budget ($M)",
                min_value=0.1,
                max_value=500.0,
                value=10.0,
                step=0.5,
                key="sim_budget",
            )

        horizon = st.slider(
            "Projection Horizon (Years)",
            min_value=1,
            max_value=10,
            value=5,
            key="sim_horizon",
        )

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        if st.button("🚀 Simulate Impact", key="sim_run_btn", type="primary", use_container_width=True):
            if len(decision_text.strip()) < 10:
                st.warning("⚠️ Please enter a more detailed decision description (at least 10 characters).")
            else:
                with st.spinner("🔄 Running impact simulation..."):
                    import time
                    time.sleep(0.4)
                    result = simulate_decision(
                        decision_text=decision_text.strip(),
                        domain=selected_domain,
                        population_affected=int(population),
                        budget_millions=float(budget),
                        horizon_years=int(horizon),
                    )
                st.session_state.sim_result = result
                st.session_state.sim_decision_text = decision_text.strip()
                st.rerun()

    # ── Results Panel ───────────────────────────────────────────────────────
    with result_col:
        result = st.session_state.sim_result

        if result is None:
            # Empty state
            st.markdown(
                """
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                  padding:80px 20px; color:var(--text-muted); text-align:center;">
                  <div style="font-size:60px; margin-bottom:20px;">🎯</div>
                  <div style="font-size:18px; font-weight:600; color:var(--text-secondary); margin-bottom:10px;">
                    Ready to Simulate
                  </div>
                  <div style="font-size:14px; line-height:1.6; max-width:400px;">
                    Select a preset decision or enter your own policy proposal.
                    The simulator will score it across 5 impact dimensions,
                    generate a timeline, and identify key risks.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        if "error" in result:
            st.error(result["error"])
            return

        # ── Overall Score ──────────────────────────────────────────────────
        overall = result["overall_score"]
        overall_color = (
            "#4ADE80" if overall >= 25 else
            "#FBBF24" if overall >= 10 else
            "#F97316" if overall >= 0 else
            "#EF4444"
        )

        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, rgba(76,201,240,0.05), rgba(167,139,250,0.05));
              border: 1px solid rgba(76,201,240,0.15); border-radius: 16px; padding: 24px 28px; margin-bottom: 20px;">
              <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
                <div style="text-align:center; min-width:100px;">
                  <div style="font-size:52px; font-weight:900; color:{overall_color}; line-height:1;">
                    {'+' if overall > 0 else ''}{overall}
                  </div>
                  <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em;">
                    Overall Score
                  </div>
                </div>
                <div style="flex:1;">
                  <div style="font-size:13px; font-weight:600; color:var(--text-primary); margin-bottom:8px;">
                    Decision: "{result['decision'][:120]}{'...' if len(result['decision']) > 120 else ''}"
                  </div>
                  <div style="font-size:13px; line-height:1.5;">{result['recommendation']}</div>
                  <div style="margin-top:10px; display:flex; gap:12px; flex-wrap:wrap; font-size:12px; color:var(--text-muted);">
                    <span>👥 {result['population_affected']:,} residents affected</span>
                    <span>💰 ${result['budget_millions']}M investment</span>
                    <span>📅 {result['horizon_years']}-year horizon</span>
                    <span>😊 {result['people_positively_impacted']:,} positively impacted</span>
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── 5-Dimension Impact Scores ──────────────────────────────────────
        st.markdown(
            '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">📊 Impact Across 5 Dimensions</div>',
            unsafe_allow_html=True,
        )
        _render_impact_bars(result["impact_scores"])

        # ── Impact Detail Expander ─────────────────────────────────────────
        with st.expander("📝 Dimension Analysis Details", expanded=False):
            for dim, data in result["impact_scores"].items():
                st.markdown(
                    f"""
                    <div style="display:flex; align-items:flex-start; gap:10px; padding:10px 0;
                      border-bottom:1px solid var(--border-color);">
                      <div style="font-size:18px;">{data['icon']}</div>
                      <div style="flex:1;">
                        <div style="font-size:13px; font-weight:600; color:var(--text-primary);">{dim}</div>
                        <div style="font-size:12px; color:var(--text-muted); margin-top:2px;">{data['rationale']}</div>
                      </div>
                      <div style="font-size:20px; font-weight:800;
                        color:{'#4ADE80' if data['score'] >= 0 else '#EF4444'}; min-width:50px; text-align:right;">
                        {'+' if data['score'] > 0 else ''}{data['score']}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        # ── Timeline Chart ─────────────────────────────────────────────────
        timeline_fig = _render_timeline_chart(result["timeline"])
        st.plotly_chart(timeline_fig, use_container_width=True, config={"displayModeBar": False})

        # ── Risk & Cost-Benefit ────────────────────────────────────────────
        risk_col, cb_col = st.columns([3, 2])

        with risk_col:
            st.markdown(
                '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">⚠️ Risk Assessment</div>',
                unsafe_allow_html=True,
            )
            _render_risk_table(result["risks"])

        with cb_col:
            st.markdown(
                '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">💰 Cost-Benefit Summary</div>',
                unsafe_allow_html=True,
            )
            cb = result["cost_benefit"]
            st.markdown(
                f"""
                <div class="kpi-card" style="padding:16px 18px;">
                  <div style="margin-bottom:10px;">
                    <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; margin-bottom:3px;">Capital Investment</div>
                    <div style="font-size:13px; font-weight:600; color:var(--text-primary);">{cb['capital_investment']}</div>
                  </div>
                  <div style="margin-bottom:10px;">
                    <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; margin-bottom:3px;">Operating Cost</div>
                    <div style="font-size:13px; font-weight:600; color:var(--text-primary);">{cb['operating_cost']}</div>
                  </div>
                  <div style="margin-bottom:10px;">
                    <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; margin-bottom:3px;">Payback Period</div>
                    <div style="font-size:13px; font-weight:600; color:#4ADE80;">{cb['payback_period']}</div>
                  </div>
                  <div>
                    <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase; margin-bottom:3px;">Estimated ROI</div>
                    <div style="font-size:13px; font-weight:600; color:#4CC9F0;">{cb['estimated_roi']}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Keywords detected
        keywords = result.get("keywords_detected", [])
        if keywords:
            st.markdown(
                f'<div style="margin-top:12px; font-size:12px; color:var(--text-muted);">🏷️ Keywords detected: '
                + " ".join(f'<span style="background:rgba(76,201,240,0.1); color:#4CC9F0; padding:2px 8px; border-radius:10px; margin:0 2px;">{kw}</span>' for kw in keywords)
                + "</div>",
                unsafe_allow_html=True,
            )
