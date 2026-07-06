"""
VitaCity AI — Dashboard Page
Rich interactive dashboard with KPIs, Plotly charts, district data, and live alerts.
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from data.mock_metrics import (
    get_city_overview, get_domain_scores,
    get_transport_data, get_env_data, get_safety_data,
    get_health_data, get_waste_data, get_civic_data,
    get_districts, get_alerts, get_recent_decisions,
)
from ui.theme import page_hero_html, alert_card_html, kpi_card_html
from ui.components import (
    render_kpi_row, render_alerts, render_domain_health_scores,
    render_district_table, make_line_chart, make_bar_chart,
    make_radar_chart, make_gauge_chart, make_donut_chart,
    CHART_BASE, ACCENT_COLORS,
)


def render_dashboard_page():
    """Main dashboard page renderer."""

    # Load all data
    overview = get_city_overview()
    domain_scores = get_domain_scores()
    transport_m, transport_t = get_transport_data()
    env_m, env_t = get_env_data()
    safety_m, safety_t = get_safety_data()
    health_m, health_t = get_health_data()
    waste_m, waste_t = get_waste_data()
    civic_m, civic_t = get_civic_data()
    districts = get_districts()
    alerts = get_alerts()
    recent_decisions = get_recent_decisions()

    # ── Page Header ─────────────────────────────────────────────────────────
    st.markdown(
        page_hero_html(
            title="City Intelligence Dashboard",
            subtitle="Real-time Urban Analytics · Metro Vitacity · Population 512,400",
            icon="📊",
        ),
        unsafe_allow_html=True,
    )

    # ── City-Wide KPIs ────────────────────────────────────────────────────────
    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">🌆 City Overview</div>',
        unsafe_allow_html=True,
    )

    render_kpi_row([
        {"icon": "👥", "value": "512,400",        "label": "Population",           "delta": "+1.8% YoY",   "delta_positive": True,  "color": "#4CC9F0"},
        {"icon": "🤖", "value": f"{overview['ai_insights_today']:,}", "label": "AI Insights Today", "delta": "+12% vs last week", "delta_positive": True, "color": "#A78BFA"},
        {"icon": "🗺️", "value": f"{overview['districts']}",          "label": "Districts Monitored", "delta": "100% coverage",    "delta_positive": True, "color": "#4ADE80"},
        {"icon": "⚠️", "value": str(overview['active_alerts']),      "label": "Active Alerts",        "delta": "–1 resolved today","delta_positive": True, "color": "#F97316"},
        {"icon": "🎯", "value": f"{overview['decisions_simulated']:,}", "label": "Decisions Simulated", "delta": "+340 this month", "delta_positive": True, "color": "#EC4899"},
        {"icon": "⭐", "value": f"{overview['citizen_satisfaction']}/10", "label": "Citizen Satisfaction", "delta": "+0.3 pts",  "delta_positive": True, "color": "#FBBF24"},
    ])

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # ── Domain Health Scores ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">🏆 Domain Health Scores</div>',
        unsafe_allow_html=True,
    )
    render_domain_health_scores(domain_scores)

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # ── Active Alerts + Radar ────────────────────────────────────────────────
    st.markdown("---")
    alert_col, radar_col = st.columns([1, 1])

    with alert_col:
        st.markdown(
            '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:10px;">🚨 Active City Alerts</div>',
            unsafe_allow_html=True,
        )
        render_alerts(alerts)

    with radar_col:
        fig_radar = make_radar_chart(
            categories=list(domain_scores.keys()),
            values=list(domain_scores.values()),
            title="Domain Health Radar",
            height=320,
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

    # ── Charts Tabs ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">📈 Trend Analytics</div>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["🚌 Mobility", "🌿 Environment", "🚨 Safety", "🏥 Healthcare", "♻️ Waste", "🏛️ Civic"])

    # Mobility Tab
    with tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            fig = make_line_chart(
                x=transport_t["months"],
                y_series={"Daily Ridership (000s)": [v / 1000 for v in transport_t["transit_ridership"]]},
                title="Transit Ridership Trend",
                y_label="Thousands",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with col2:
            fig = make_line_chart(
                x=transport_t["months"],
                y_series={
                    "Avg Speed (km/h)": transport_t["avg_speed"],
                    "Incidents": transport_t["incidents"],
                },
                title="Traffic Speed vs. Incidents",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        m_cols = st.columns(4)
        mobility_kpis = [
            ("🚌", f"{transport_m['public_transit_ridership_daily']:,}", "Daily Riders", "#4CC9F0"),
            ("⏱️", f"{transport_m['transit_on_time_pct']}%", "On-Time Rate", "#4ADE80"),
            ("⚡", str(transport_m['ev_charging_stations']), "EV Stations", "#A78BFA"),
            ("🚲", f"{transport_m['cycling_infrastructure_km']} km", "Cycling Network", "#FBBF24"),
        ]
        for col, (icon, val, label, color) in zip(m_cols, mobility_kpis):
            with col:
                st.markdown(kpi_card_html(icon, val, label, color=color), unsafe_allow_html=True)

    # Environment Tab
    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            fig = make_line_chart(
                x=env_t["months"],
                y_series={
                    "AQI": env_t["aqi"],
                    "CO₂ (kt/month)": env_t["co2_kt"],
                },
                title="Air Quality & Carbon Emissions",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with col2:
            fig = make_line_chart(
                x=env_t["months"],
                y_series={"Renewable Energy %": env_t["renewable_pct"]},
                title="Renewable Energy Share",
                y_label="%",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        e_cols = st.columns(4)
        env_kpis = [
            ("🌬️", f"AQI {env_m['aqi_current']}", "Air Quality (Good)", "#4ADE80"),
            ("🌡️", f"{env_m['pm25_ugm3']} μg/m³", "PM2.5", "#FBBF24"),
            ("☀️", f"{env_m['renewable_energy_pct']}%", "Renewable Energy", "#4CC9F0"),
            ("🌳", f"{env_m['tree_canopy_pct']}%", "Tree Canopy Coverage", "#4ADE80"),
        ]
        for col, (icon, val, label, color) in zip(e_cols, env_kpis):
            with col:
                st.markdown(kpi_card_html(icon, val, label, color=color), unsafe_allow_html=True)

    # Safety Tab
    with tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            fig = make_line_chart(
                x=safety_t["months"],
                y_series={"Crime Rate /1,000": safety_t["crime_rate"]},
                title="Crime Rate Trend",
                y_label="per 1,000 residents",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with col2:
            fig = make_line_chart(
                x=safety_t["months"],
                y_series={
                    "Fire Response (min)": safety_t["fire_response"],
                    "EMS Response (min)": safety_t["ems_response"],
                },
                title="Emergency Response Times",
                y_label="Minutes",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        s_cols = st.columns(4)
        safety_kpis = [
            ("🚔", f"{safety_m['crime_rate_per_1000']}/1k", "Crime Rate", "#F97316"),
            ("🚒", f"{safety_m['fire_response_avg_min']} min", "Fire Response Avg", "#4ADE80"),
            ("🚑", f"{safety_m['ems_response_avg_min']} min", "EMS Response Avg", "#4CC9F0"),
            ("📹", f"{safety_m['cctv_cameras']:,}", "CCTV Cameras", "#A78BFA"),
        ]
        for col, (icon, val, label, color) in zip(s_cols, safety_kpis):
            with col:
                st.markdown(kpi_card_html(icon, val, label, color=color), unsafe_allow_html=True)

    # Healthcare Tab
    with tabs[3]:
        col1, col2 = st.columns(2)
        with col1:
            fig = make_line_chart(
                x=health_t["months"],
                y_series={"ER Wait Time (min)": health_t["er_wait"]},
                title="ER Average Wait Time",
                y_label="Minutes",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with col2:
            fig = make_line_chart(
                x=health_t["months"],
                y_series={"Telehealth Visits": health_t["telehealth"]},
                title="Telehealth Adoption",
                y_label="Monthly Visits",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        h_cols = st.columns(4)
        health_kpis = [
            ("👨‍⚕️", f"{health_m['pcp_per_10k_residents']}/10k", "PCPs per Resident", "#EC4899"),
            ("🏥", f"{health_m['avg_er_wait_min']} min", "Avg ER Wait", "#F97316"),
            ("💉", f"{health_m['vaccination_rate_pct']}%", "Vaccination Rate", "#4ADE80"),
            ("📱", f"{health_m['telehealth_visits_monthly']:,}", "Telehealth/Month", "#4CC9F0"),
        ]
        for col, (icon, val, label, color) in zip(h_cols, health_kpis):
            with col:
                st.markdown(kpi_card_html(icon, val, label, color=color), unsafe_allow_html=True)

    # Waste Tab
    with tabs[4]:
        col1, col2 = st.columns(2)
        with col1:
            fig = make_line_chart(
                x=waste_t["months"],
                y_series={
                    "Landfill Diversion %": waste_t["landfill_diversion"],
                    "Recycling Rate %": waste_t["recycling_rate"],
                },
                title="Waste Diversion Progress",
                y_label="%",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with col2:
            # Waste composition donut
            fig = make_donut_chart(
                labels=["Recyclables", "Organics/Compost", "Landfill", "Hazardous", "E-Waste"],
                values=[44, 27, 22, 4, 3],
                title="Waste Stream Composition",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        w_cols = st.columns(4)
        waste_kpis = [
            ("♻️", f"{waste_m['landfill_diversion_pct']}%", "Landfill Diversion", "#4ADE80"),
            ("🗑️", f"{waste_m['recycling_rate_pct']}%", "Recycling Rate", "#4CC9F0"),
            ("🌱", f"{waste_m['composting_rate_pct']}%", "Composting Rate", "#FBBF24"),
            ("📡", f"{waste_m['smart_bins_deployed']:,}", "Smart Bins Deployed", "#A78BFA"),
        ]
        for col, (icon, val, label, color) in zip(w_cols, waste_kpis):
            with col:
                st.markdown(kpi_card_html(icon, val, label, color=color), unsafe_allow_html=True)

    # Civic Tab
    with tabs[5]:
        col1, col2 = st.columns(2)
        with col1:
            fig = make_line_chart(
                x=civic_t["months"],
                y_series={"Civic App Users (000s)": [v for v in civic_t["app_users"]]},
                title="Civic Platform Adoption",
                y_label="Thousands",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with col2:
            fig = make_line_chart(
                x=civic_t["months"],
                y_series={"311 Resolution Days": civic_t["resolution_days"]},
                title="311 Avg Resolution Time",
                y_label="Days",
                height=260,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
        c_cols = st.columns(4)
        civic_kpis = [
            ("📱", f"{civic_m['civic_app_users']:,}", "Civic App Users", "#FBBF24"),
            ("📋", f"{civic_m['311_requests_monthly']:,}", "Monthly 311 Requests", "#4CC9F0"),
            ("⚡", f"{civic_m['avg_311_resolution_days']} days", "Avg Resolution Time", "#4ADE80"),
            ("🗳️", f"{civic_m['participatory_budget_participants']:,}", "Budget Participants", "#A78BFA"),
        ]
        for col, (icon, val, label, color) in zip(c_cols, civic_kpis):
            with col:
                st.markdown(kpi_card_html(icon, val, label, color=color), unsafe_allow_html=True)

    # ── District Comparison ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">🗺️ District Performance Comparison</div>',
        unsafe_allow_html=True,
    )
    render_district_table(districts)

    # ── District bar chart ───────────────────────────────────────────────────
    metric_options = {
        "Safety Score": "safety_score",
        "Health Score": "health_score",
        "Environment Score": "env_score",
        "Mobility Score": "mobility_score",
    }
    selected_metric_label = st.selectbox("Compare districts by:", list(metric_options.keys()), key="district_metric")
    selected_field = metric_options[selected_metric_label]

    sorted_districts = sorted(districts, key=lambda d: d[selected_field], reverse=True)
    district_names = [d["name"] for d in sorted_districts]
    district_values = [d[selected_field] for d in sorted_districts]

    colors_bar = []
    for v in district_values:
        if v >= 80:
            colors_bar.append("#4ADE80")
        elif v >= 65:
            colors_bar.append("#FBBF24")
        else:
            colors_bar.append("#F97316")

    fig_districts = go.Figure(
        go.Bar(
            x=district_names,
            y=district_values,
            marker=dict(color=colors_bar, opacity=0.85),
            hovertemplate="%{x}: %{y}/100<extra></extra>",
        )
    )
    layout = dict(**CHART_BASE)
    layout["title"] = dict(text=f"{selected_metric_label} by District", font=dict(color="#F0F6FF", size=14, family="Inter"), x=0.01, xanchor="left")
    layout["height"] = 280
    layout["yaxis"]["range"] = [0, 100]
    layout["yaxis"]["title"] = "Score (0-100)"
    fig_districts.update_layout(**layout)
    st.plotly_chart(fig_districts, use_container_width=True, config={"displayModeBar": False})

    # ── Recent AI Decisions Log ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">🕐 Recent AI Decision Queries</div>',
        unsafe_allow_html=True,
    )

    for dec in recent_decisions:
        impact_color = "#4ADE80" if dec["impact"] == "High" else "#FBBF24" if dec["impact"] == "Medium" else "#8B9EC5"
        conf_pct = int(dec["confidence"] * 100)
        st.markdown(
            f"""
            <div class="kpi-card" style="margin-bottom:6px; padding:12px 16px;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:13px; color:var(--text-primary); font-weight:500;">"{dec['query']}"</div>
                <div style="font-size:11px; color:var(--text-muted); white-space:nowrap; margin-left:12px;">{dec['time']}</div>
              </div>
              <div style="margin-top:6px; display:flex; gap:8px; align-items:center;">
                <span style="font-size:11px; background:rgba(76,201,240,0.1); color:#4CC9F0; padding:2px 8px; border-radius:12px;">{dec['domain']}</span>
                <span style="font-size:11px; color:#4ADE80;">●</span>
                <span style="font-size:11px; color:var(--text-muted);">Confidence: {conf_pct}%</span>
                <span style="font-size:11px; color:{impact_color}; font-weight:600;">Impact: {dec['impact']}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
