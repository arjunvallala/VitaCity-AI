"""
VitaCity AI — Shared UI Components
Reusable Streamlit components used across multiple pages.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Any

from ui.theme import (
    kpi_card_html,
    confidence_badge_html,
    domain_badge_html,
    alert_card_html,
    source_citation_html,
    rec_card_html,
    status_indicator_html,
)
from data.knowledge_base import DOMAIN_COLORS, DOMAIN_ICONS

# ────────────────────────────────────────────────────────────────
#  Plotly chart base layout (dark-mode)
# ────────────────────────────────────────────────────────────────

CHART_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#8B9EC5", size=12),
    margin=dict(l=16, r=16, t=40, b=16),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(255,255,255,0.08)",
        font=dict(color="#8B9EC5", size=11),
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        showline=False,
        tickfont=dict(color="#8B9EC5", size=11),
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        showline=False,
        tickfont=dict(color="#8B9EC5", size=11),
        zeroline=False,
    ),
)

ACCENT_COLORS = [
    "#4CC9F0", "#A78BFA", "#4ADE80", "#EC4899",
    "#F97316", "#FBBF24", "#38BDF8", "#C084FC",
]


def make_line_chart(
    x: list,
    y_series: Dict[str, list],
    title: str,
    y_label: str = "",
    height: int = 280,
) -> go.Figure:
    """Create a styled multi-series line chart."""
    fig = go.Figure()
    for i, (name, y_vals) in enumerate(y_series.items()):
        color = ACCENT_COLORS[i % len(ACCENT_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y_vals,
                name=name,
                mode="lines+markers",
                line=dict(color=color, width=2.5, shape="spline"),
                marker=dict(size=5, color=color),
                fill="tozeroy",
                fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.06)",
                hovertemplate=f"<b>{name}</b><br>%{{y}}<extra></extra>",
            )
        )
    layout = dict(**CHART_BASE)
    layout["title"] = dict(text=title, font=dict(color="#F0F6FF", size=14, family="Inter"), x=0.01, xanchor="left")
    layout["height"] = height
    layout["yaxis"]["title"] = y_label
    fig.update_layout(**layout)
    return fig


def make_bar_chart(
    categories: list,
    values: list,
    title: str,
    color: str = "#4CC9F0",
    height: int = 280,
    orientation: str = "v",
) -> go.Figure:
    """Create a styled bar chart."""
    if orientation == "h":
        fig = go.Figure(
            go.Bar(x=values, y=categories, orientation="h",
                   marker=dict(color=color, opacity=0.8),
                   hovertemplate="%{y}: %{x}<extra></extra>")
        )
    else:
        fig = go.Figure(
            go.Bar(x=categories, y=values,
                   marker=dict(color=color, opacity=0.8),
                   hovertemplate="%{x}: %{y}<extra></extra>")
        )
    layout = dict(**CHART_BASE)
    layout["title"] = dict(text=title, font=dict(color="#F0F6FF", size=14, family="Inter"), x=0.01, xanchor="left")
    layout["height"] = height
    fig.update_layout(**layout)
    return fig


def make_radar_chart(categories: list, values: list, title: str, height: int = 320) -> go.Figure:
    """Create a radar/spider chart for domain health scores."""
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure(
        go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            fillcolor="rgba(76,201,240,0.08)",
            line=dict(color="#4CC9F0", width=2),
            marker=dict(size=6, color="#4CC9F0"),
            hovertemplate="%{theta}: %{r}<extra></extra>",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#4B5E7A", size=9),
                gridcolor="rgba(255,255,255,0.06)",
                linecolor="rgba(255,255,255,0.06)",
            ),
            angularaxis=dict(
                tickfont=dict(color="#8B9EC5", size=11),
                gridcolor="rgba(255,255,255,0.06)",
                linecolor="rgba(255,255,255,0.06)",
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
        height=height,
        margin=dict(l=40, r=40, t=50, b=40),
        title=dict(text=title, font=dict(color="#F0F6FF", size=14, family="Inter"), x=0.5, xanchor="center"),
    )
    return fig


def make_gauge_chart(value: float, title: str, max_val: float = 100, height: int = 220) -> go.Figure:
    """Create a gauge/indicator chart."""
    # Color based on value percentage
    pct = value / max_val
    if pct >= 0.75:
        bar_color = "#4ADE80"
    elif pct >= 0.50:
        bar_color = "#FBBF24"
    else:
        bar_color = "#F97316"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title=dict(text=title, font=dict(color="#8B9EC5", size=12)),
            gauge=dict(
                axis=dict(range=[0, max_val], tickfont=dict(color="#4B5E7A", size=9)),
                bar=dict(color=bar_color, thickness=0.7),
                bgcolor="rgba(255,255,255,0.04)",
                borderwidth=1,
                bordercolor="rgba(255,255,255,0.08)",
                steps=[
                    dict(range=[0, max_val * 0.5], color="rgba(239,68,68,0.06)"),
                    dict(range=[max_val * 0.5, max_val * 0.75], color="rgba(251,191,36,0.06)"),
                    dict(range=[max_val * 0.75, max_val], color="rgba(74,222,128,0.06)"),
                ],
            ),
            number=dict(font=dict(color="#F0F6FF", size=28, family="Inter"), suffix="/100" if max_val == 100 else ""),
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    return fig


def make_donut_chart(labels: list, values: list, title: str, height: int = 280) -> go.Figure:
    """Create a donut pie chart."""
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=ACCENT_COLORS[:len(labels)]),
            textfont=dict(color="#8B9EC5", size=11),
            hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=16, r=16, t=40, b=16),
        title=dict(text=title, font=dict(color="#F0F6FF", size=14, family="Inter"), x=0.5, xanchor="center"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8B9EC5", size=11),
        ),
    )
    return fig


# ────────────────────────────────────────────────────────────────
#  Streamlit Component Wrappers
# ────────────────────────────────────────────────────────────────

def render_kpi_row(kpis: List[Dict]):
    """
    Render a row of KPI cards.
    Each KPI dict: {icon, value, label, delta, delta_positive, color}
    """
    cols = st.columns(len(kpis))
    for col, kpi in zip(cols, kpis):
        with col:
            st.markdown(
                kpi_card_html(
                    icon=kpi.get("icon", "📊"),
                    value=str(kpi.get("value", "-")),
                    label=kpi.get("label", ""),
                    delta=kpi.get("delta", ""),
                    delta_positive=kpi.get("delta_positive", True),
                    color=kpi.get("color", "#4CC9F0"),
                ),
                unsafe_allow_html=True,
            )


def render_chat_message(role: str, content: str, metadata: Dict = None):
    """Render a chat message bubble with optional metadata."""
    if role == "user":
        st.markdown(
            f'<div class="chat-bubble-user">💬 {content}</div>',
            unsafe_allow_html=True,
        )
    else:
        # AI message
        st.markdown(
            f'<div class="chat-bubble-ai">{content}</div>',
            unsafe_allow_html=True,
        )
        if metadata:
            meta_cols = st.columns([1, 1, 1, 2])
            with meta_cols[0]:
                conf = metadata.get("confidence", 0)
                st.markdown(confidence_badge_html(conf), unsafe_allow_html=True)
            with meta_cols[1]:
                domain = metadata.get("domain", "General")
                icon = DOMAIN_ICONS.get(domain, "🏙️")
                st.markdown(domain_badge_html(domain, icon), unsafe_allow_html=True)
            with meta_cols[2]:
                st.markdown(
                    status_indicator_html("RAG-Augmented", "green"),
                    unsafe_allow_html=True,
                )


def render_sources(chunks: List[Dict]):
    """Render source citation cards."""
    if not chunks:
        return
    with st.expander(f"📚 Sources Used ({len(chunks)} knowledge chunks)", expanded=False):
        for chunk in chunks:
            st.markdown(
                source_citation_html(
                    title=chunk.get("title", "Source"),
                    domain=chunk.get("domain", ""),
                    similarity=chunk.get("similarity_score", 0),
                ),
                unsafe_allow_html=True,
            )


def render_recommendations(recs: List[str]):
    """Render key recommendations."""
    if not recs:
        return
    st.markdown("**🎯 Key Recommendations**")
    for rec in recs:
        st.markdown(rec_card_html(rec), unsafe_allow_html=True)


def render_alerts(alerts: List[Dict]):
    """Render active city alerts."""
    for alert in alerts:
        st.markdown(
            alert_card_html(
                title=alert.get("title", ""),
                description=alert.get("description", ""),
                severity=alert.get("severity", "low"),
                domain=alert.get("domain", ""),
                timestamp=alert.get("timestamp", ""),
            ),
            unsafe_allow_html=True,
        )


def render_domain_health_scores(scores: Dict[str, int]):
    """Render domain health score cards."""
    items = list(scores.items())
    row1 = items[:3]
    row2 = items[3:]

    for row in [row1, row2]:
        cols = st.columns(3)
        for col, (domain, score) in zip(cols, row):
            with col:
                color_map = {
                    "Urban Mobility": "#4CC9F0",
                    "Environment": "#4ADE80",
                    "Public Safety": "#F97316",
                    "Healthcare": "#EC4899",
                    "Waste Mgmt": "#A78BFA",
                    "Civic Engagement": "#FBBF24",
                }
                color = color_map.get(domain, "#4CC9F0")
                delta_color = "#4ADE80" if score >= 70 else "#FBBF24" if score >= 55 else "#EF4444"
                status = "🟢" if score >= 70 else "🟡" if score >= 55 else "🔴"
                st.markdown(
                    f"""
                    <div class="kpi-card" style="border-left: 3px solid {color};">
                      <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-size:12px; color:var(--text-secondary); font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">{domain}</div>
                        <div style="font-size:12px;">{status}</div>
                      </div>
                      <div style="font-size:32px; font-weight:800; color:{color}; margin: 8px 0 4px;">{score}</div>
                      <div style="background:rgba(255,255,255,0.05); border-radius:4px; height:4px; overflow:hidden;">
                        <div style="background:{color}; height:100%; width:{score}%; border-radius:4px; transition: width 0.5s ease;"></div>
                      </div>
                      <div style="font-size:10px; color:var(--text-muted); margin-top:4px;">out of 100</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_impact_bar(
    label: str,
    score: int,
    icon: str,
    color: str,
    rationale: str,
):
    """Render a single impact dimension bar."""
    bar_width = max(0, score)  # Only show positive for bar
    neg_width = max(0, -score)  # Negative portion

    st.markdown(
        f"""
        <div style="margin-bottom: 16px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <div style="font-size:13px; font-weight:600; color:var(--text-primary);">{icon} {label}</div>
            <div style="font-size:13px; font-weight:700; color:{color};">{'+' if score > 0 else ''}{score}</div>
          </div>
          <div style="background:rgba(255,255,255,0.05); border-radius:6px; height:8px; overflow:hidden; position:relative;">
            {'<div style="background:' + color + '; height:100%; width:' + str(bar_width) + '%; border-radius:6px; transition:width 0.6s ease;"></div>'
             if score >= 0 else
             '<div style="background:#EF4444; height:100%; width:' + str(neg_width) + '%; border-radius:6px; float:right; transition:width 0.6s ease;"></div>'}
          </div>
          <div style="font-size:11px; color:var(--text-muted); margin-top:4px;">{rationale}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_district_table(districts: List[Dict]):
    """Render district comparison table as styled DataFrame."""
    df = pd.DataFrame(districts)[
        ["name", "population", "safety_score", "health_score", "env_score", "mobility_score"]
    ].rename(columns={
        "name": "District",
        "population": "Population",
        "safety_score": "Safety 🛡️",
        "health_score": "Health 🏥",
        "env_score": "Environment 🌿",
        "mobility_score": "Mobility 🚌",
    })

    def color_score(val):
        if isinstance(val, (int, float)):
            if val >= 80:
                return "color: #4ADE80; font-weight: 600"
            elif val >= 65:
                return "color: #FBBF24; font-weight: 600"
            else:
                return "color: #F97316; font-weight: 600"
        return ""

    styled = df.style.applymap(
        color_score,
        subset=["Safety 🛡️", "Health 🏥", "Environment 🌿", "Mobility 🚌"],
    ).format({"Population": "{:,}"})

    st.dataframe(styled, use_container_width=True, hide_index=True)


def thinking_placeholder() -> Any:
    """Return a Streamlit empty placeholder for streaming-style display."""
    return st.empty()
