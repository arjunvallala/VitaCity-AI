"""
VitaCity AI — Mock Metrics Data
Realistic, detailed mock data for dashboard KPIs and Plotly charts.
All data is synthesized to represent a mid-sized city of ~500,000 residents.
"""

import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
#  CITY OVERVIEW KPIs
# ─────────────────────────────────────────────
CITY_OVERVIEW = {
    "name": "Metro Vitacity",
    "population": 512_400,
    "area_km2": 342,
    "districts": 12,
    "ai_insights_today": 847,
    "active_alerts": 3,
    "decisions_simulated": 2_341,
    "citizen_satisfaction": 7.4,   # out of 10
}

# ─────────────────────────────────────────────
#  DOMAIN HEALTH SCORES (0–100)
# ─────────────────────────────────────────────
DOMAIN_HEALTH_SCORES = {
    "Urban Mobility": 68,
    "Environment": 74,
    "Public Safety": 81,
    "Healthcare": 72,
    "Waste Mgmt": 79,
    "Civic Engagement": 65,
}

# ─────────────────────────────────────────────
#  TRANSPORTATION METRICS
# ─────────────────────────────────────────────
TRANSPORT_METRICS = {
    "avg_commute_min": 34,
    "public_transit_ridership_daily": 187_000,
    "transit_on_time_pct": 84.2,
    "ev_charging_stations": 342,
    "cycling_infrastructure_km": 218,
    "avg_traffic_speed_kmh": 28.4,
    "road_incidents_this_month": 127,
    "congestion_index": 0.62,      # 0=free flow, 1=gridlock
}

TRANSPORT_TREND = {
    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "transit_ridership": [158, 162, 171, 176, 183, 187, 191, 189, 185, 182, 178, 175],
    "avg_speed": [31, 30, 29, 28, 27, 28, 28, 29, 28, 27, 28, 29],
    "incidents": [145, 138, 131, 129, 132, 127, 125, 128, 130, 133, 129, 131],
}

# ─────────────────────────────────────────────
#  ENVIRONMENTAL METRICS
# ─────────────────────────────────────────────
ENV_METRICS = {
    "aqi_current": 47,             # Good: 0-50, Moderate: 51-100
    "aqi_label": "Good",
    "pm25_ugm3": 8.2,
    "co2_kt_annual": 1_842,        # kilotonnes
    "renewable_energy_pct": 38,
    "tree_canopy_pct": 24,
    "green_space_per_capita_m2": 18.4,
    "solar_capacity_mw": 142,
    "flood_risk_zones_pct": 8.3,
}

ENV_TREND = {
    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "aqi": [62, 58, 54, 51, 48, 47, 44, 46, 49, 52, 56, 60],
    "co2_kt": [172, 165, 161, 154, 148, 145, 141, 143, 150, 156, 162, 168],
    "renewable_pct": [31, 32, 34, 35, 37, 38, 40, 39, 38, 37, 36, 34],
}

# ─────────────────────────────────────────────
#  PUBLIC SAFETY METRICS
# ─────────────────────────────────────────────
SAFETY_METRICS = {
    "crime_rate_per_1000": 18.4,
    "violent_crime_per_1000": 4.2,
    "fire_response_avg_min": 5.8,
    "ems_response_avg_min": 7.2,
    "911_calls_monthly": 14_820,
    "community_policing_programs": 24,
    "cctv_cameras": 1_842,
    "emergency_shelters": 8,
}

SAFETY_TREND = {
    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "crime_rate": [21.2, 20.8, 20.1, 19.6, 19.0, 18.4, 18.1, 18.3, 18.6, 18.8, 19.0, 18.7],
    "fire_response": [6.4, 6.3, 6.1, 6.0, 5.9, 5.8, 5.7, 5.8, 5.9, 6.0, 5.9, 5.8],
    "ems_response": [8.1, 7.9, 7.8, 7.6, 7.4, 7.2, 7.1, 7.2, 7.3, 7.3, 7.2, 7.1],
}

# ─────────────────────────────────────────────
#  HEALTHCARE METRICS
# ─────────────────────────────────────────────
HEALTH_METRICS = {
    "pcp_per_10k_residents": 2.8,
    "avg_er_wait_min": 48,
    "telehealth_visits_monthly": 12_400,
    "vaccination_rate_pct": 78.3,
    "mental_health_access_pct": 42,
    "diabetes_prevalence_pct": 9.8,
    "obesity_rate_pct": 31.2,
    "healthy_food_access_pct": 68,
}

HEALTH_TREND = {
    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "er_wait": [62, 59, 56, 53, 51, 48, 47, 46, 48, 50, 52, 54],
    "telehealth": [8200, 8800, 9400, 10100, 11200, 12400, 13100, 12900, 12600, 12300, 12000, 11800],
    "vaccination_pct": [72, 73, 74, 75, 76, 78, 78, 78, 78, 78, 78, 78],
}

# ─────────────────────────────────────────────
#  WASTE MANAGEMENT METRICS
# ─────────────────────────────────────────────
WASTE_METRICS = {
    "landfill_diversion_pct": 71,
    "recycling_rate_pct": 44,
    "composting_rate_pct": 27,
    "waste_per_capita_kg_yr": 412,
    "smart_bins_deployed": 2_840,
    "collection_efficiency_pct": 88,
    "food_waste_diverted_tonnes_yr": 8_200,
    "ewaste_collected_tonnes_yr": 340,
}

WASTE_TREND = {
    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "landfill_diversion": [62, 63, 65, 67, 69, 71, 72, 72, 71, 71, 71, 71],
    "recycling_rate": [38, 39, 40, 41, 43, 44, 45, 45, 44, 44, 44, 44],
    "waste_per_capita": [438, 432, 428, 422, 416, 412, 408, 410, 413, 415, 414, 412],
}

# ─────────────────────────────────────────────
#  CITIZEN ENGAGEMENT METRICS
# ─────────────────────────────────────────────
CIVIC_METRICS = {
    "civic_app_users": 84_200,
    "311_requests_monthly": 28_400,
    "avg_311_resolution_days": 4.2,
    "open_data_datasets": 186,
    "participatory_budget_participants": 12_800,
    "public_meetings_attended_avg": 340,
    "digital_services_pct": 72,
    "citizen_satisfaction_score": 7.4,
}

CIVIC_TREND = {
    "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "app_users": [61, 63, 66, 69, 73, 78, 81, 83, 84, 84, 84, 84],
    "requests_311": [24200, 25100, 25800, 26500, 27200, 28400, 29100, 28900, 28600, 28300, 28100, 28000],
    "resolution_days": [6.8, 6.4, 6.0, 5.6, 5.1, 4.2, 3.9, 4.0, 4.1, 4.2, 4.2, 4.3],
}

# ─────────────────────────────────────────────
#  DISTRICT-LEVEL DATA (12 districts)
# ─────────────────────────────────────────────
DISTRICTS = [
    {"name": "Northgate",     "population": 48200,  "safety_score": 84, "health_score": 76, "env_score": 71, "mobility_score": 72, "lat": 40.785, "lon": -73.968},
    {"name": "Riverside",     "population": 52100,  "safety_score": 78, "health_score": 71, "env_score": 82, "mobility_score": 68, "lat": 40.768, "lon": -73.980},
    {"name": "Central Hub",   "population": 61300,  "safety_score": 70, "health_score": 68, "env_score": 65, "mobility_score": 85, "lat": 40.754, "lon": -73.954},
    {"name": "Eastfield",     "population": 39800,  "safety_score": 75, "health_score": 73, "env_score": 74, "mobility_score": 64, "lat": 40.742, "lon": -73.935},
    {"name": "Westmoor",      "population": 44600,  "safety_score": 82, "health_score": 79, "env_score": 78, "mobility_score": 70, "lat": 40.762, "lon": -74.001},
    {"name": "Southpark",     "population": 37200,  "safety_score": 69, "health_score": 65, "env_score": 71, "mobility_score": 62, "lat": 40.728, "lon": -73.962},
    {"name": "Innovation Dist","population": 28400, "safety_score": 88, "health_score": 84, "env_score": 79, "mobility_score": 91, "lat": 40.748, "lon": -73.942},
    {"name": "Lakeside",      "population": 41800,  "safety_score": 86, "health_score": 80, "env_score": 87, "mobility_score": 74, "lat": 40.775, "lon": -73.946},
    {"name": "Midtown",       "population": 55400,  "safety_score": 73, "health_score": 70, "env_score": 63, "mobility_score": 88, "lat": 40.751, "lon": -73.975},
    {"name": "Green Valley",  "population": 35100,  "safety_score": 80, "health_score": 77, "env_score": 91, "mobility_score": 61, "lat": 40.790, "lon": -73.920},
    {"name": "Harbor View",   "population": 43200,  "safety_score": 76, "health_score": 74, "env_score": 76, "mobility_score": 77, "lat": 40.720, "lon": -73.980},
    {"name": "University Zone","population": 25300, "safety_score": 79, "health_score": 82, "env_score": 80, "mobility_score": 83, "lat": 40.760, "lon": -73.925},
]

# ─────────────────────────────────────────────
#  ACTIVE ALERTS (real-time feed simulation)
# ─────────────────────────────────────────────
ACTIVE_ALERTS = [
    {
        "id": "ALT001",
        "severity": "high",
        "domain": "Public Safety",
        "title": "Elevated Air Quality Alert — Central Hub District",
        "description": "PM2.5 readings at 68 μg/m³ (Unhealthy for Sensitive Groups). Construction dust from Highway 7 expansion.",
        "timestamp": "2026-07-06 10:23",
        "action": "Restrict outdoor exercise for sensitive populations. Deploy water sprayers at construction site.",
    },
    {
        "id": "ALT002",
        "severity": "medium",
        "domain": "Transportation",
        "title": "Transit Disruption — Riverside BRT Corridor",
        "description": "Bus delays of 12-18 minutes due to water main break on Oak Avenue. 14 routes affected.",
        "timestamp": "2026-07-06 14:07",
        "action": "Activate shuttle supplementation and update real-time passenger information systems.",
    },
    {
        "id": "ALT003",
        "severity": "low",
        "domain": "Waste Management",
        "title": "Recycling Contamination Spike — Northgate",
        "description": "Contamination rate reached 22% (threshold: 15%) in Northgate collection area this week.",
        "timestamp": "2026-07-06 09:45",
        "action": "Deploy community education team. Review bin labeling in affected blocks.",
    },
]

# ─────────────────────────────────────────────
#  RECENT AI DECISIONS LOG
# ─────────────────────────────────────────────
RECENT_DECISIONS = [
    {"query": "Should we expand bike lanes on Main Street?",       "domain": "Mobility",     "confidence": 0.91, "impact": "High",   "time": "2h ago"},
    {"query": "Where to place new EV charging stations?",          "domain": "Environment",  "confidence": 0.88, "impact": "Medium", "time": "3h ago"},
    {"query": "Optimizing waste collection routes for Q3",         "domain": "Waste",        "confidence": 0.93, "impact": "High",   "time": "5h ago"},
    {"query": "Community health screening locations for flu season","domain": "Healthcare",   "confidence": 0.86, "impact": "Medium", "time": "7h ago"},
    {"query": "Emergency shelter capacity for winter surge",        "domain": "Safety",       "confidence": 0.90, "impact": "High",   "time": "9h ago"},
    {"query": "Participatory budget allocation for parks",          "domain": "Civic",        "confidence": 0.84, "impact": "Medium", "time": "12h ago"},
]

def get_city_overview():
    return CITY_OVERVIEW

def get_domain_scores():
    return DOMAIN_HEALTH_SCORES

def get_transport_data():
    return TRANSPORT_METRICS, TRANSPORT_TREND

def get_env_data():
    return ENV_METRICS, ENV_TREND

def get_safety_data():
    return SAFETY_METRICS, SAFETY_TREND

def get_health_data():
    return HEALTH_METRICS, HEALTH_TREND

def get_waste_data():
    return WASTE_METRICS, WASTE_TREND

def get_civic_data():
    return CIVIC_METRICS, CIVIC_TREND

def get_districts():
    return DISTRICTS

def get_alerts():
    return ACTIVE_ALERTS

def get_recent_decisions():
    return RECENT_DECISIONS
