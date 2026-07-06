"""
VitaCity AI — Smoke Test Script
Tests all modules work correctly end-to-end.
Run: python smoke_test.py
"""

import sys
import os
import traceback

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

PASS = "[PASS]"
FAIL = "[FAIL]"
results = []

def test(name, fn):
    try:
        fn()
        print(f"  {PASS} {name}")
        results.append((name, True, None))
    except Exception as e:
        print(f"  {FAIL} {name}: {e}")
        results.append((name, False, str(e)))

print("\n" + "="*55)
print("  VitaCity AI — Smoke Test Suite")
print("="*55)

# ── 1. Data Layer ─────────────────────────────────────────────
print("\n[1] Data Layer")

def test_knowledge_base():
    from data.knowledge_base import (
        get_all_chunks, get_chunks_by_domain, get_chunk_by_id,
        DOMAIN_COLORS, DOMAIN_ICONS, ALL_DOMAINS, KNOWLEDGE_BASE
    )
    chunks = get_all_chunks()
    assert len(chunks) > 20, f"Expected >20 chunks, got {len(chunks)}"
    assert len(ALL_DOMAINS) == 6, f"Expected 6 domains, got {len(ALL_DOMAINS)}"
    assert all("content" in c and "domain" in c and "title" in c for c in chunks)
    mob_chunks = get_chunks_by_domain("Urban Mobility & Transportation")
    assert len(mob_chunks) > 0, f"Expected chunks for Urban Mobility, got {len(mob_chunks)}"
    chunk = get_chunk_by_id("mob_001")
    assert chunk is not None and chunk["id"] == "mob_001"

test("Knowledge base structure", test_knowledge_base)

def test_mock_metrics():
    from data.mock_metrics import (
        get_city_overview, get_domain_scores, get_transport_data,
        get_env_data, get_safety_data, get_health_data,
        get_waste_data, get_civic_data, get_districts,
        get_alerts, get_recent_decisions
    )
    overview = get_city_overview()
    assert "population" in overview and overview["population"] > 0
    scores = get_domain_scores()
    assert len(scores) == 6
    assert all(0 <= v <= 100 for v in scores.values())
    districts = get_districts()
    assert len(districts) == 12
    alerts = get_alerts()
    assert len(alerts) >= 1
    decisions = get_recent_decisions()
    assert len(decisions) >= 1
    # Test all getters
    t_m, t_t = get_transport_data()
    e_m, e_t = get_env_data()
    s_m, s_t = get_safety_data()
    h_m, h_t = get_health_data()
    w_m, w_t = get_waste_data()
    c_m, c_t = get_civic_data()
    assert all("months" in t for t in [t_t, e_t, s_t, h_t, w_t, c_t])

test("Mock metrics data", test_mock_metrics)

# ── 2. Core Engine ────────────────────────────────────────────
print("\n[2] Core Engine")

def test_rag_engine():
    from core.rag_engine import RAGEngine, get_rag_engine
    rag = RAGEngine(top_k=5)
    assert rag.is_ready, "RAG engine should be ready after init"
    assert rag.chunk_count > 0, f"Expected chunks, got {rag.chunk_count}"
    # Test retrieval
    chunks = rag.retrieve("traffic congestion bus rapid transit")
    assert len(chunks) > 0, "Should retrieve at least 1 chunk"
    assert all("similarity_score" in c for c in chunks)
    assert all(c["similarity_score"] >= 0 for c in chunks)
    # Test domain filter
    env_chunks = rag.retrieve("solar renewable energy", domain_filter="Environmental Sustainability")
    # Each chunk should be from env domain
    for c in env_chunks:
        assert "Environmental" in c["domain"] or c["similarity_score"] == 0
    # Test format_context
    context = rag.format_context(chunks)
    assert isinstance(context, str) and len(context) > 0
    # Test retrieve_and_format
    ctx, cks = rag.retrieve_and_format("emergency response time")
    assert isinstance(ctx, str)
    assert isinstance(cks, list)
    # Test domain coverage
    coverage = rag.get_domain_coverage("transportation mobility bus")
    assert isinstance(coverage, dict) and len(coverage) > 0
    # Test singleton
    rag2 = get_rag_engine()
    assert rag2 is not None

test("RAG engine (TF-IDF retrieval)", test_rag_engine)

def test_decision_simulator():
    from core.decision_simulator import simulate_decision, IMPACT_DIMENSIONS
    assert len(IMPACT_DIMENSIONS) == 5
    # Test with a good decision
    result = simulate_decision(
        decision_text="Build new solar panels on all municipal buildings and replace bus fleet with electric buses",
        domain="Environmental Sustainability & Climate Resilience",
        population_affected=100000,
        budget_millions=50.0,
        horizon_years=5,
    )
    assert "overall_score" in result
    assert "impact_scores" in result
    assert len(result["impact_scores"]) == 5
    assert "timeline" in result and len(result["timeline"]) == 5
    assert "risks" in result and len(result["risks"]) > 0
    assert "cost_benefit" in result
    assert "recommendation" in result
    assert all(key in result for key in [
        "decision", "domain", "overall_score", "overall_label",
        "recommendation", "impact_scores", "timeline", "risks",
        "cost_benefit", "population_affected", "people_positively_impacted",
        "budget_millions", "horizon_years", "keywords_detected"
    ])
    # Score bounds check
    for dim, data in result["impact_scores"].items():
        assert -100 <= data["score"] <= 100, f"Score out of bounds for {dim}: {data['score']}"
    # Test with empty input
    err = simulate_decision("")
    assert "error" in err

test("Decision simulator engine", test_decision_simulator)

def test_gemini_client():
    from core.gemini_client import GeminiClient, get_gemini_client
    # Test demo mode (no API key)
    client = GeminiClient()
    # Should be in demo mode if no API key set
    # Test demo responses
    queries = [
        "traffic congestion bus",
        "carbon footprint environment",
        "emergency safety response",
        "healthcare hospital access",
        "waste recycling program",
        "citizen engagement government",
        "what should we do about city planning",
    ]
    for q in queries:
        resp = client._demo_response(q)
        assert "answer" in resp, f"No answer for: {q}"
        assert "confidence" in resp, f"No confidence for: {q}"
        assert 0.0 <= resp["confidence"] <= 1.0, f"Invalid confidence for: {q}"
        assert isinstance(resp.get("key_recommendations", []), list)
        assert isinstance(resp.get("sources_used", []), list)
        assert isinstance(resp.get("follow_up_questions", []), list)
    # Test demo image response
    img_resp = client._demo_image_response()
    assert "issue_detected" in img_resp
    assert "severity" in img_resp
    assert "priority_score" in img_resp
    assert 1 <= img_resp["priority_score"] <= 10
    # Test singleton
    c2 = get_gemini_client()
    assert c2 is not None

test("Gemini client (demo mode)", test_gemini_client)

# ── 3. UI Layer (import-only) ─────────────────────────────────
print("\n[3] UI Layer (import checks)")

def test_theme_import():
    from ui.theme import (
        inject_css, sidebar_logo_html, page_hero_html,
        kpi_card_html, confidence_badge_html, domain_badge_html,
        alert_card_html, source_citation_html, rec_card_html,
        status_indicator_html, CUSTOM_CSS
    )
    assert isinstance(CUSTOM_CSS, str) and len(CUSTOM_CSS) > 1000
    hero = page_hero_html("Test Title", "Test Subtitle", "🏙️")
    assert "Test Title" in hero and "Test Subtitle" in hero
    badge = confidence_badge_html(0.92)
    assert "High Confidence" in badge
    badge2 = confidence_badge_html(0.75)
    assert "Medium Confidence" in badge2
    badge3 = confidence_badge_html(0.55)
    assert "Low Confidence" in badge3
    kpi = kpi_card_html("🚌", "42,000", "Daily Riders", "+5%", True, "#4CC9F0")
    assert "42,000" in kpi and "Daily Riders" in kpi

test("UI theme & HTML helpers", test_theme_import)

def test_components_import():
    import plotly.graph_objects as go
    from ui.components import (
        make_line_chart, make_bar_chart, make_radar_chart,
        make_gauge_chart, make_donut_chart, CHART_BASE, ACCENT_COLORS
    )
    assert isinstance(CHART_BASE, dict)
    assert len(ACCENT_COLORS) >= 6
    # Test chart factories
    line = make_line_chart(
        x=["Jan", "Feb", "Mar"],
        y_series={"Series A": [10, 20, 15], "Series B": [5, 8, 12]},
        title="Test Line Chart",
    )
    assert isinstance(line, go.Figure)
    bar = make_bar_chart(["A", "B", "C"], [10, 20, 30], "Test Bar")
    assert isinstance(bar, go.Figure)
    radar = make_radar_chart(["x", "y", "z"], [80, 60, 70], "Test Radar")
    assert isinstance(radar, go.Figure)
    gauge = make_gauge_chart(75.0, "Test Gauge")
    assert isinstance(gauge, go.Figure)
    donut = make_donut_chart(["A", "B"], [60, 40], "Test Donut")
    assert isinstance(donut, go.Figure)

test("UI components & Plotly chart factories", test_components_import)

def test_page_imports():
    # These should import without error (they define functions, don't run Streamlit)
    import ui.chat_page
    import ui.dashboard_page
    import ui.simulator_page
    import ui.responsible_ai_page
    assert hasattr(ui.chat_page, "render_chat_page")
    assert hasattr(ui.dashboard_page, "render_dashboard_page")
    assert hasattr(ui.simulator_page, "render_simulator_page")
    assert hasattr(ui.responsible_ai_page, "render_responsible_ai_page")

test("Page module imports", test_page_imports)

# ── 4. Integration Test ───────────────────────────────────────
print("\n[4] Integration Test")

def test_rag_plus_demo_chat():
    from core.rag_engine import RAGEngine
    from core.gemini_client import GeminiClient
    rag = RAGEngine(top_k=5)
    client = GeminiClient()
    query = "How can we improve emergency response times in underserved neighborhoods?"
    context, chunks = rag.retrieve_and_format(query)
    assert len(chunks) > 0
    assert len(context) > 0
    response = client._demo_response(query)
    assert len(response.get("answer", "")) > 100
    assert response.get("confidence", 0) > 0

test("RAG + Chat end-to-end pipeline", test_rag_plus_demo_chat)

def test_simulator_integration():
    from core.decision_simulator import simulate_decision
    # Test all preset scenarios
    presets = [
        ("Replace diesel buses with electric buses", "Urban Mobility & Transportation"),
        ("Install solar panels on municipal buildings", "Environmental Sustainability & Climate Resilience"),
        ("Deploy mobile health clinics in healthcare deserts", "Healthcare Access & Wellness"),
        ("Create new neighborhood parks and plant 50000 trees", "Environmental Sustainability & Climate Resilience"),
        ("Deploy smart recycling bins with composting program", "Waste Management & Resource Optimization"),
        ("Launch multilingual civic engagement digital platform", "Citizen Engagement & Public Services"),
    ]
    for text, domain in presets:
        r = simulate_decision(text, domain=domain, population_affected=100000, budget_millions=10.0)
        assert "overall_score" in r, f"No overall_score for: {text[:40]}"
        assert "impact_scores" in r
        assert len(r["timeline"]) == 5

test("Decision simulator preset scenarios", test_simulator_integration)

# -- Results Summary ------------------------------------------
print("\n" + "="*55)
passed = sum(1 for _, ok, _ in results if ok)
failed = sum(1 for _, ok, _ in results if not ok)
print(f"  Results: {passed} passed, {failed} failed out of {len(results)} tests")
print("="*55)

if failed > 0:
    print("\nFailed tests:")
    for name, ok, err in results:
        if not ok:
            print(f"  [FAIL] {name}")
            print(f"     {err}")
    sys.exit(1)
else:
    print("\n  *** ALL TESTS PASSED! VitaCity AI is ready to run. ***")
    print("\n  To start the app:")
    print("    streamlit run app.py")
    print()
