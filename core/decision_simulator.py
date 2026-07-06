"""
VitaCity AI — Decision Simulator Engine
Analyzes proposed city decisions and scores their impact across 5 dimensions.
Generates timeline projections and risk/benefit assessments.
"""

import re
import random
from typing import Dict, List, Tuple


# Impact dimension definitions
IMPACT_DIMENSIONS = {
    "Environmental": {
        "icon": "🌿",
        "color": "#4ADE80",
        "description": "Effect on air quality, carbon emissions, green space, and natural resources",
    },
    "Economic": {
        "icon": "💰",
        "color": "#FBBF24",
        "description": "Effect on city budget, local businesses, employment, and property values",
    },
    "Social Equity": {
        "icon": "⚖️",
        "color": "#A78BFA",
        "description": "Effect on underserved communities, access equality, and community well-being",
    },
    "Health & Safety": {
        "icon": "🏥",
        "color": "#EC4899",
        "description": "Effect on public health outcomes, injury rates, and community safety",
    },
    "Mobility": {
        "icon": "🚌",
        "color": "#4CC9F0",
        "description": "Effect on transportation, accessibility, and commute quality",
    },
}

# Domain keyword → impact signatures
DOMAIN_SIGNATURES = {
    "transit": {
        "Environmental": (+35, "Reduces vehicle emissions and carbon footprint"),
        "Economic": (+20, "Reduces household transportation costs; may require capital investment"),
        "Social Equity": (+30, "Improves access for car-free residents and low-income communities"),
        "Health & Safety": (+15, "Reduces traffic accidents; improves air quality health outcomes"),
        "Mobility": (+45, "Directly improves public transit capacity and reliability"),
    },
    "bus": {
        "Environmental": (+25, "Electric bus fleet significantly reduces local air pollutants"),
        "Economic": (+15, "Operating costs 30% lower than private car per passenger-mile"),
        "Social Equity": (+28, "Key mode of transport for non-drivers and low-income residents"),
        "Health & Safety": (+12, "Reduces road crashes; BRT lanes decrease pedestrian-vehicle conflicts"),
        "Mobility": (+40, "Increases transit capacity and reduces road congestion"),
    },
    "solar": {
        "Environmental": (+50, "Direct reduction in carbon emissions; up to 100% clean electricity"),
        "Economic": (+25, "Payback period 6-8 years; reduces long-term energy costs by 40-60%"),
        "Social Equity": (+10, "Community solar programs extend benefits to renters and low-income households"),
        "Health & Safety": (+20, "Reduces air pollution; fewer asthma and respiratory cases"),
        "Mobility": (0, "Minimal direct effect on transportation"),
    },
    "park": {
        "Environmental": (+30, "Increases tree canopy; reduces urban heat island; improves air quality"),
        "Economic": (+18, "Increases adjacent property values by 8-15%; attracts retail and visitors"),
        "Social Equity": (+35, "Critical amenity for dense, low-income neighborhoods with limited private green space"),
        "Health & Safety": (+40, "Reduces stress; increases physical activity; improves mental health outcomes"),
        "Mobility": (+5, "Can include walking/cycling infrastructure"),
    },
    "housing": {
        "Environmental": (-10, "New construction has embedded carbon; smart design can mitigate"),
        "Economic": (+30, "Addresses affordability; reduces displacement; stabilizes rents"),
        "Social Equity": (+45, "Critical for vulnerable populations; reduces homelessness risk"),
        "Health & Safety": (+25, "Stable housing strongly linked to better health outcomes"),
        "Mobility": (+10, "Mixed-use and transit-oriented developments reduce car dependency"),
    },
    "recycling": {
        "Environmental": (+40, "Reduces landfill methane; conserves raw materials; cuts production emissions"),
        "Economic": (+20, "Reduces landfill disposal costs; generates recyclable commodity revenue"),
        "Social Equity": (+15, "Creates green jobs; cleaner neighborhoods benefit underserved communities"),
        "Health & Safety": (+15, "Reduces toxic waste exposure; cleaner community environment"),
        "Mobility": (+5, "Optimized waste collection reduces truck traffic"),
    },
    "cycling": {
        "Environmental": (+35, "Each km cycled replaces car trip = 0.21 kg CO2 avoided"),
        "Economic": (+20, "Infrastructure cost $200K-1M/km vs. $5-30M for roads; boosts local retail"),
        "Social Equity": (+20, "Low-cost, accessible transport mode for all income levels"),
        "Health & Safety": (+30, "Cyclists have 41% lower mortality; infrastructure protects from vehicle conflicts"),
        "Mobility": (+35, "Increases overall network capacity; reduces car demand"),
    },
    "school": {
        "Environmental": (+5, "Green school buildings, school gardens contribute positively"),
        "Economic": (+30, "Education ROI: $7-12 for every $1 invested; reduces future welfare costs"),
        "Social Equity": (+50, "Critical equity lever; reduces intergenerational poverty"),
        "Health & Safety": (+20, "Safer school environments; nutrition and physical education programs"),
        "Mobility": (+10, "Safe Routes to School programs reduce car drop-offs"),
    },
    "police": {
        "Environmental": (0, "Minimal direct environmental impact"),
        "Economic": (+10, "Crime reduction improves business investment; high cost of expanded policing"),
        "Social Equity": (-15, "Expanded policing has equity concerns; community programs more equitable"),
        "Health & Safety": (+25, "Reduces crime victimization; faster emergency response"),
        "Mobility": (+5, "Traffic enforcement improves road safety"),
    },
    "health": {
        "Environmental": (+5, "Healthier population; healthcare facilities can be sustainability leaders"),
        "Economic": (+30, "Preventive care ROI: $3-8 per $1 invested; reduces productivity loss"),
        "Social Equity": (+40, "Healthcare access is a critical social equity issue"),
        "Health & Safety": (+50, "Direct improvement to population health outcomes"),
        "Mobility": (+5, "Mobile health units and telehealth reduce patient travel burden"),
    },
    "water": {
        "Environmental": (+35, "Water conservation reduces energy for treatment; protects ecosystems"),
        "Economic": (+22, "Reduces water/energy costs; avoids costly infrastructure expansion"),
        "Social Equity": (+20, "Affordable water is essential for all residents"),
        "Health & Safety": (+30, "Clean water is critical for public health"),
        "Mobility": (0, "Minimal direct mobility effect"),
    },
}

# Generic base for unknown decisions
DEFAULT_BASE = {
    "Environmental": (+10, "Moderate positive environmental consideration"),
    "Economic": (+15, "Projected positive economic return"),
    "Social Equity": (+12, "Equitable implementation recommended"),
    "Health & Safety": (+10, "Positive health and safety outcomes expected"),
    "Mobility": (+8, "Some mobility improvements anticipated"),
}


def _normalize_score(raw: int) -> int:
    """Clamp score to -100..+100 range."""
    return max(-100, min(100, raw))


def _detect_keywords(decision_text: str) -> List[str]:
    """Detect domain keywords in the decision text."""
    text_lower = decision_text.lower()
    matched = []
    for keyword in DOMAIN_SIGNATURES:
        if keyword in text_lower:
            matched.append(keyword)
    return matched


def _build_impact_scores(decision_text: str) -> Dict[str, Dict]:
    """
    Build per-dimension impact scores for a decision.
    Returns dict of {dimension: {score, rationale, color, icon}}.
    """
    keywords = _detect_keywords(decision_text)
    impact = {}

    for dim, dim_info in IMPACT_DIMENSIONS.items():
        total_score = 0
        rationale_parts = []

        if keywords:
            for kw in keywords:
                sig = DOMAIN_SIGNATURES.get(kw, {})
                if dim in sig:
                    delta, reason = sig[dim]
                    # Add small variation for realism
                    varied_delta = delta + random.randint(-5, 5)
                    total_score += varied_delta
                    rationale_parts.append(reason)
        else:
            # Use defaults if no keywords matched
            sig = DEFAULT_BASE
            if dim in sig:
                delta, reason = sig[dim]
                total_score = delta + random.randint(-8, 8)
                rationale_parts.append(reason)

        # Average if multiple keywords contributed
        if keywords and len(keywords) > 1:
            total_score = total_score // len(keywords)

        score = _normalize_score(total_score)
        impact[dim] = {
            "score": score,
            "rationale": rationale_parts[0] if rationale_parts else "General impact assessment based on policy analysis.",
            "color": dim_info["color"],
            "icon": dim_info["icon"],
            "label": _score_to_label(score),
        }

    return impact


def _score_to_label(score: int) -> str:
    if score >= 40:
        return "Strong Positive"
    elif score >= 20:
        return "Moderate Positive"
    elif score >= 5:
        return "Slight Positive"
    elif score >= -5:
        return "Neutral"
    elif score >= -20:
        return "Slight Negative"
    elif score >= -40:
        return "Moderate Negative"
    else:
        return "Strong Negative"


def _generate_timeline(impact_scores: Dict, horizon_years: int = 5) -> List[Dict]:
    """Generate cumulative impact timeline year by year."""
    timeline = []
    avg_score = sum(d["score"] for d in impact_scores.values()) / len(impact_scores)

    cumulative = 0
    ramp_factors = [0.15, 0.35, 0.60, 0.80, 1.0]  # Ramp-up over 5 years

    for year in range(1, horizon_years + 1):
        factor = ramp_factors[min(year - 1, 4)]
        year_impact = avg_score * factor
        cumulative += year_impact / horizon_years

        timeline.append({
            "year": f"Year {year}",
            "projected_impact": round(year_impact, 1),
            "cumulative_benefit": round(cumulative * 10, 0),  # Scale to make visible
            "confidence": round(0.95 - (year - 1) * 0.08, 2),  # Confidence decreases with time
        })

    return timeline


def _identify_risks(decision_text: str, impact_scores: Dict) -> List[Dict]:
    """Identify risks based on negative impact scores and decision content."""
    risks = []
    text_lower = decision_text.lower()

    # Check for negative impact dimensions
    for dim, data in impact_scores.items():
        if data["score"] < -10:
            risks.append({
                "risk": f"Negative {dim} Impact",
                "likelihood": "Medium",
                "severity": "High" if data["score"] < -30 else "Medium",
                "mitigation": f"Implement targeted {dim.lower()} mitigation measures and monitoring",
            })

    # Keyword-specific risks
    if "demolish" in text_lower or "remove" in text_lower:
        risks.append({
            "risk": "Community displacement or disruption",
            "likelihood": "High",
            "severity": "High",
            "mitigation": "Develop community relocation support and stakeholder consultation plan",
        })
    if "cost" in text_lower or "million" in text_lower or "budget" in text_lower:
        risks.append({
            "risk": "Budget overrun and cost escalation",
            "likelihood": "Medium",
            "severity": "Medium",
            "mitigation": "Include 20% contingency, stage implementation, and establish independent cost oversight",
        })
    if "new" in text_lower and any(w in text_lower for w in ["build", "construct", "develop", "install"]):
        risks.append({
            "risk": "Construction phase disruption",
            "likelihood": "High",
            "severity": "Low",
            "mitigation": "Develop traffic/service continuity plan and community communication strategy",
        })

    # Add a generic systemic risk
    risks.append({
        "risk": "Stakeholder resistance and adoption delays",
        "likelihood": "Medium",
        "severity": "Medium",
        "mitigation": "Proactive community engagement, pilot program, and iterative feedback cycles",
    })

    return risks[:4]  # Return top 4 risks


def _estimate_cost_benefit(decision_text: str, impact_scores: Dict) -> Dict:
    """Generate a cost-benefit summary based on decision keywords."""
    text_lower = decision_text.lower()

    # Rough cost estimate based on keywords
    if any(w in text_lower for w in ["fleet", "vehicle", "bus"]):
        capex = "High ($20M - $150M)"
        opex = "Medium ($2M - $8M/year)"
        payback = "7-12 years"
    elif any(w in text_lower for w in ["solar", "renewable", "energy"]):
        capex = "High ($5M - $80M)"
        opex = "Low ($200K - $1M/year)"
        payback = "6-10 years"
    elif any(w in text_lower for w in ["park", "green", "garden"]):
        capex = "Medium ($500K - $5M)"
        opex = "Low ($100K - $500K/year)"
        payback = "Qualitative ROI (property values, health)"
    elif any(w in text_lower for w in ["app", "digital", "software", "platform"]):
        capex = "Low ($200K - $2M)"
        opex = "Low ($50K - $500K/year)"
        payback = "2-4 years"
    elif any(w in text_lower for w in ["clinic", "health", "hospital"]):
        capex = "High ($2M - $50M)"
        opex = "Medium ($1M - $10M/year)"
        payback = "ROI via avoided costs: 3-8x"
    else:
        capex = "Medium ($1M - $20M)"
        opex = "Medium ($200K - $2M/year)"
        payback = "4-8 years"

    avg_score = sum(d["score"] for d in impact_scores.values()) / len(impact_scores)
    roi_multiplier = round(1 + avg_score / 30, 1)

    return {
        "capital_investment": capex,
        "operating_cost": opex,
        "payback_period": payback,
        "estimated_roi": f"{roi_multiplier}x - {roi_multiplier + 1.5}x",
        "benefit_categories": [
            "Reduced operational costs",
            "Improved resident well-being",
            "Environmental value creation",
            "Economic development stimulus",
        ],
    }


def simulate_decision(
    decision_text: str,
    domain: str = "All Domains",
    population_affected: int = 50000,
    budget_millions: float = 5.0,
    horizon_years: int = 5,
) -> Dict:
    """
    Main simulation function.

    Args:
        decision_text: Description of the proposed decision/policy.
        domain: Primary domain for the decision.
        population_affected: Estimated population affected.
        budget_millions: Proposed budget in millions.
        horizon_years: Projection horizon in years.

    Returns:
        Comprehensive impact assessment dict.
    """
    if not decision_text or len(decision_text) < 10:
        return {"error": "Please provide a more detailed decision description."}

    impact_scores = _build_impact_scores(decision_text)
    timeline = _generate_timeline(impact_scores, horizon_years)
    risks = _identify_risks(decision_text, impact_scores)
    cost_benefit = _estimate_cost_benefit(decision_text, impact_scores)

    # Overall score: weighted average
    overall = int(sum(d["score"] for d in impact_scores.values()) / len(impact_scores))
    overall_label = _score_to_label(overall)

    # Recommendation
    if overall >= 25:
        recommendation = "✅ **Recommended** — High positive impact across multiple dimensions. Proceed with implementation planning."
        rec_color = "#4ADE80"
    elif overall >= 10:
        recommendation = "🟡 **Conditionally Recommended** — Positive overall impact with some trade-offs. Address identified risks before proceeding."
        rec_color = "#FBBF24"
    elif overall >= 0:
        recommendation = "⚠️ **Proceed with Caution** — Modest positive impact with significant trade-offs. Consider alternative approaches."
        rec_color = "#F97316"
    else:
        recommendation = "🔴 **Not Recommended in Current Form** — Significant negative impacts identified. Major redesign recommended."
        rec_color = "#EF4444"

    people_positively_impacted = int(population_affected * max(0, overall) / 100)

    return {
        "decision": decision_text,
        "domain": domain,
        "overall_score": overall,
        "overall_label": overall_label,
        "recommendation": recommendation,
        "recommendation_color": rec_color,
        "impact_scores": impact_scores,
        "timeline": timeline,
        "risks": risks,
        "cost_benefit": cost_benefit,
        "population_affected": population_affected,
        "people_positively_impacted": people_positively_impacted,
        "budget_millions": budget_millions,
        "horizon_years": horizon_years,
        "keywords_detected": _detect_keywords(decision_text),
    }
