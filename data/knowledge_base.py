"""
VitaCity AI — Knowledge Base
Rich, domain-specific knowledge chunks for RAG retrieval across 6 urban domains.
"""

KNOWLEDGE_BASE = [

    # ─────────────────────────────────────────────
    #  DOMAIN 1: Urban Mobility & Transportation
    # ─────────────────────────────────────────────
    {
        "id": "mob_001",
        "domain": "Urban Mobility & Transportation",
        "title": "Traffic Congestion Root Causes",
        "content": (
            "Urban traffic congestion is primarily caused by: (1) Inadequate road capacity relative to vehicle density, "
            "(2) Poor signal timing and lack of adaptive traffic control systems, (3) Over-reliance on private vehicles due to "
            "insufficient public transit options, (4) Inefficient land-use planning concentrating employment in single zones, "
            "(5) Incomplete pedestrian and cycling infrastructure pushing more residents to cars. Cities that have reduced "
            "congestion by 30-40% have done so through a combination of congestion pricing, real-time adaptive signals, "
            "dedicated bus rapid transit (BRT) lanes, and park-and-ride facilities at transit nodes."
        ),
        "tags": ["traffic", "congestion", "signals", "transit", "roads"],
        "confidence_base": 0.92,
    },
    {
        "id": "mob_002",
        "domain": "Urban Mobility & Transportation",
        "title": "Bus Rapid Transit Implementation",
        "content": (
            "Bus Rapid Transit (BRT) systems offer 80% of the capacity of light rail at 20% of the cost. Successful BRT "
            "implementations (Bogotá TransMilenio, Curitiba Rede Integrada) share key features: dedicated lanes physically "
            "separated from traffic, off-board fare collection, level boarding platforms, real-time passenger information "
            "systems, and high-frequency service (every 3-5 minutes during peak hours). A properly implemented BRT corridor "
            "can carry 30,000-45,000 passengers per hour per direction. Cities should prioritize corridors with existing "
            "bus ridership above 3,000 passengers/hour as BRT candidates."
        ),
        "tags": ["BRT", "bus", "transit", "public transport", "corridor"],
        "confidence_base": 0.90,
    },
    {
        "id": "mob_003",
        "domain": "Urban Mobility & Transportation",
        "title": "Micro-Mobility and Last-Mile Solutions",
        "content": (
            "Micro-mobility (e-scooters, e-bikes, cargo bikes) addresses the critical 'last mile' gap between transit "
            "stations and final destinations. Cities with successful micro-mobility programs maintain: geofenced operating "
            "zones, mandatory helmet programs, designated parking corrals, integration with transit apps for seamless "
            "journey planning, and rebalancing operations to prevent scooter clustering. Average trip distance is 1.8 km "
            "with an average speed of 15 km/h. Micro-mobility programs have been shown to reduce short car trips by "
            "17-23% in dense urban areas when combined with robust cycling infrastructure."
        ),
        "tags": ["scooter", "e-bike", "last mile", "micro-mobility", "cycling"],
        "confidence_base": 0.87,
    },
    {
        "id": "mob_004",
        "domain": "Urban Mobility & Transportation",
        "title": "Smart Parking Systems",
        "content": (
            "Cruising for parking accounts for 30% of urban traffic in congested downtowns. Smart parking systems using "
            "IoT sensors, dynamic pricing, and mobile reservation apps reduce parking search time by up to 43%. Key "
            "technologies: magnetic sensors embedded in parking spots, overhead cameras with computer vision, license "
            "plate recognition for enforcement, and demand-responsive pricing ($0.50-$5.00/hour based on occupancy). "
            "San Francisco's SFpark program reduced cruising-related traffic by 30% and increased parking revenue by 19%. "
            "Recommendation: Deploy sensors in lots exceeding 85% average occupancy first."
        ),
        "tags": ["parking", "smart parking", "IoT", "downtown", "traffic"],
        "confidence_base": 0.88,
    },
    {
        "id": "mob_005",
        "domain": "Urban Mobility & Transportation",
        "title": "Electric Vehicle Infrastructure Planning",
        "content": (
            "For a city targeting 40% EV adoption by 2030, charging infrastructure must scale accordingly. The recommended "
            "ratio is 1 public charger per 10 EVs. Infrastructure should include: Level 2 AC chargers (7-22 kW) for "
            "residential neighborhoods and workplaces (4-8 hour charging), DC fast chargers (50-350 kW) at highway "
            "corridors and shopping centers (20-45 minute charging), and ultra-fast chargers (350+ kW) at fleet depots. "
            "Grid upgrades are essential: a dense urban district may require 50-200 MW additional capacity. EV charging "
            "combined with vehicle-to-grid (V2G) technology can reduce peak grid demand by 15%."
        ),
        "tags": ["EV", "electric vehicle", "charging", "infrastructure", "grid"],
        "confidence_base": 0.89,
    },
    {
        "id": "mob_006",
        "domain": "Urban Mobility & Transportation",
        "title": "Pedestrian Safety and Vision Zero",
        "content": (
            "Vision Zero — a policy commitment to eliminate all traffic fatalities — has been adopted by 40+ major cities. "
            "Key interventions: (1) Reducing speed limits to 30 km/h in residential areas (cuts pedestrian fatality risk "
            "by 70% vs 50 km/h), (2) Raised crosswalks and pedestrian refuges at high-risk intersections, (3) Leading "
            "Pedestrian Intervals (LPI) giving walkers a 7-second head start, (4) Data-driven targeting of high-injury "
            "networks (typically 5% of streets account for 65% of severe injuries). Oslo achieved zero pedestrian "
            "fatalities in 2019 using this comprehensive approach."
        ),
        "tags": ["pedestrian", "safety", "vision zero", "crosswalk", "speed"],
        "confidence_base": 0.91,
    },

    # ─────────────────────────────────────────────
    #  DOMAIN 2: Environmental Sustainability
    # ─────────────────────────────────────────────
    {
        "id": "env_001",
        "domain": "Environmental Sustainability & Climate Resilience",
        "title": "Urban Carbon Footprint Reduction Strategies",
        "content": (
            "A city's carbon footprint is distributed across: buildings 35%, transportation 28%, industry 22%, waste 8%, "
            "and other 7%. Achieving a 20% reduction in 5 years requires concurrent action: (1) Building efficiency: "
            "retrofitting older commercial buildings with LED lighting, smart HVAC, and insulation can cut building "
            "emissions by 30-40%. (2) Renewable energy: switching municipal operations to 100% renewable electricity "
            "saves approximately 0.8 tCO2 per MWh. (3) Transportation: each 10% shift from cars to public transit "
            "reduces transport emissions by 6-8%. (4) Urban forestry: 100 trees sequester ~1 tCO2/year. A 20% city-wide "
            "reduction requires coordinated policy, incentives, and roughly $15-50M in capital investment for mid-sized cities."
        ),
        "tags": ["carbon", "emissions", "climate", "green", "sustainability", "footprint"],
        "confidence_base": 0.90,
    },
    {
        "id": "env_002",
        "domain": "Environmental Sustainability & Climate Resilience",
        "title": "Urban Heat Island Effect Mitigation",
        "content": (
            "Urban Heat Islands (UHI) can make cities 2-5°C warmer than surrounding rural areas, increasing cooling energy "
            "demand by 10-20% and worsening air quality. Mitigation strategies: (1) Green roofs reduce rooftop temperatures "
            "by 30-40°C and building cooling loads by 15-25%. (2) Cool pavements (reflective asphalt/concrete) reflect "
            "50-80% more solar radiation vs standard asphalt. (3) Urban tree canopy target of 30%+ coverage reduces ambient "
            "temperature by 2-8°C in shaded areas. (4) Strategic placement of water features (fountains, misting stations) "
            "provide evaporative cooling. Cities like Singapore (30% green coverage mandate) and Melbourne (Urban Forest "
            "Strategy) have measurably reduced UHI impacts."
        ),
        "tags": ["heat island", "UHI", "green roof", "urban forest", "temperature", "cooling"],
        "confidence_base": 0.88,
    },
    {
        "id": "env_003",
        "domain": "Environmental Sustainability & Climate Resilience",
        "title": "Air Quality Monitoring and Management",
        "content": (
            "Urban air quality is measured using the Air Quality Index (AQI) across key pollutants: PM2.5, PM10, NO2, O3, "
            "CO, and SO2. WHO guidelines recommend PM2.5 annual mean of 5 μg/m³ (2021 revised standard). Cities achieving "
            "good air quality: (1) Deploy dense sensor networks (1 sensor per 0.5 km²) for hyper-local monitoring. "
            "(2) Implement Low Emission Zones (LEZ) restricting high-polluting vehicles in city centers. (3) Transition "
            "diesel bus fleets to electric/hydrogen. (4) Create green buffer zones along major roadways. Real-time air "
            "quality data fed to citizen apps increases public awareness and behavior change by 23%."
        ),
        "tags": ["air quality", "AQI", "PM2.5", "pollution", "emissions", "monitoring"],
        "confidence_base": 0.91,
    },
    {
        "id": "env_004",
        "domain": "Environmental Sustainability & Climate Resilience",
        "title": "Flood Resilience and Stormwater Management",
        "content": (
            "Climate change is increasing extreme rainfall events by 20-30% in frequency and intensity. Flood resilience "
            "strategies: (1) Sponge city concepts — permeable pavements, bioswales, retention ponds absorb up to 70% of "
            "runoff on-site. (2) Nature-based solutions: restored wetlands can store 1.5 million liters per hectare. "
            "(3) Smart stormwater systems with IoT-controlled valves adapt in real-time to rainfall forecasts. (4) "
            "Floodplain mapping and zoning restrictions prevent development in 100-year flood zones. Dutch 'Room for the "
            "River' program reduced peak flows by 10-15% and protected 4 million residents. Investment in flood resilience "
            "returns $6 for every $1 spent in avoided damages."
        ),
        "tags": ["flood", "stormwater", "resilience", "sponge city", "wetlands", "climate"],
        "confidence_base": 0.89,
    },
    {
        "id": "env_005",
        "domain": "Environmental Sustainability & Climate Resilience",
        "title": "Renewable Energy Transition for Municipalities",
        "content": (
            "Municipal renewable energy transition pathway: (1) Solar PV on all suitable public rooftops (schools, "
            "municipal buildings) — average 100 kWp per building, payback period 6-8 years. (2) Community solar gardens "
            "allow residents without suitable rooftops to participate. (3) Wind energy (small urban turbines or "
            "partnership with utility-scale wind farms) can supply 40-60% of municipal electricity. (4) Battery energy "
            "storage systems (BESS) with 4-hour duration provide grid stability. (5) Green hydrogen from excess renewable "
            "power for heavy transport and industrial use. Cities achieving 100% renewable electricity: Copenhagen, "
            "Burlington VT, Georgetown TX."
        ),
        "tags": ["solar", "renewable", "energy", "wind", "battery", "green hydrogen"],
        "confidence_base": 0.87,
    },
    {
        "id": "env_006",
        "domain": "Environmental Sustainability & Climate Resilience",
        "title": "Urban Biodiversity and Green Infrastructure",
        "content": (
            "Urban biodiversity supports ecosystem services worth $2-9 trillion globally. Key programs: (1) Wildlife "
            "corridors connecting parks allow species movement through cities. (2) Native plant landscaping in public "
            "spaces reduces irrigation needs by 60% and supports pollinators. (3) Urban wetland restoration improves "
            "water filtration and provides habitat. (4) Green building mandates requiring living walls and biodiverse "
            "roof gardens. Singapore's 'City in a Garden' vision has increased green coverage from 36% to 47% since "
            "2000. Biodiversity indices (BVI) can be used to measure progress and set targets."
        ),
        "tags": ["biodiversity", "green infrastructure", "wildlife", "parks", "ecosystem"],
        "confidence_base": 0.85,
    },

    # ─────────────────────────────────────────────
    #  DOMAIN 3: Public Safety & Emergency Preparedness
    # ─────────────────────────────────────────────
    {
        "id": "safe_001",
        "domain": "Public Safety & Emergency Preparedness",
        "title": "Emergency Response Time Optimization",
        "content": (
            "Average emergency response time is a critical life-safety metric. Best practices: (1) Fire stations should "
            "be located within 4-minute travel time to cover 90% of a service area (NFPA 1710 standard). (2) EMS units "
            "benefit from dynamic pre-positioning using predictive demand models — reducing response time by 12-18%. "
            "(3) Priority signal preemption systems clear traffic signals ahead of emergency vehicles. (4) Community "
            "First Responder (CFR) programs train volunteers to provide immediate care while paramedics are en route. "
            "Neighborhoods with response times > 8 minutes should be flagged as high-priority for station investment or "
            "CFR program expansion."
        ),
        "tags": ["emergency", "response time", "fire", "EMS", "ambulance", "safety"],
        "confidence_base": 0.91,
    },
    {
        "id": "safe_002",
        "domain": "Public Safety & Emergency Preparedness",
        "title": "Crime Prevention Through Environmental Design (CPTED)",
        "content": (
            "Crime Prevention Through Environmental Design (CPTED) uses physical environment modifications to deter "
            "criminal activity: (1) Natural surveillance — maximize visibility through lighting (minimum 10 lux for "
            "pedestrian areas), transparent storefronts, and eliminating blind spots. (2) Territorial reinforcement — "
            "clear public/private boundaries using landscaping, paving changes, and signage. (3) Access control — "
            "strategic placement of entrances, fencing, and bollards. (4) Activity support — active ground-floor uses "
            "and street programming increase 'eyes on the street.' CPTED implementations have reduced crime rates by "
            "15-40% in target areas without displacing crime to neighboring zones."
        ),
        "tags": ["crime", "CPTED", "safety", "lighting", "surveillance", "design"],
        "confidence_base": 0.87,
    },
    {
        "id": "safe_003",
        "domain": "Public Safety & Emergency Preparedness",
        "title": "Disaster Early Warning Systems",
        "content": (
            "Multi-hazard early warning systems (MHEWS) save lives and reduce economic losses by 30-fold. Components: "
            "(1) Risk knowledge: comprehensive hazard mapping using GIS and historical data. (2) Monitoring: real-time "
            "sensor networks (seismic, weather, flood gauges, wildfire cameras). (3) Warning dissemination: multi-channel "
            "alerts (SMS, sirens, TV/radio EAS, social media) reaching 95%+ of population within 5 minutes. (4) Response "
            "capability: pre-positioned supplies, trained community disaster response teams. The UN Sendai Framework "
            "targets 100% population coverage by MHEWS by 2030."
        ),
        "tags": ["disaster", "early warning", "flood", "earthquake", "siren", "alert"],
        "confidence_base": 0.90,
    },
    {
        "id": "safe_004",
        "domain": "Public Safety & Emergency Preparedness",
        "title": "Community Policing and Trust Building",
        "content": (
            "Community policing strategies that build trust while maintaining safety: (1) Foot patrol officers assigned "
            "to specific neighborhoods for 12+ months build relationships and local knowledge. (2) Regular community "
            "meetings and co-design of safety priorities with residents. (3) Transparent data sharing — publishing "
            "crime statistics, response times, and use-of-force data builds accountability. (4) Diversion programs for "
            "non-violent offenders (mental health response, addiction support) reduce recidivism by 30%. (5) Youth "
            "engagement programs providing mentorship and economic opportunity address root causes. Cities with strong "
            "community policing programs show 20-35% reductions in violent crime over 5-year periods."
        ),
        "tags": ["policing", "community", "crime", "trust", "youth", "safety"],
        "confidence_base": 0.86,
    },
    {
        "id": "safe_005",
        "domain": "Public Safety & Emergency Preparedness",
        "title": "Cybersecurity for Smart City Infrastructure",
        "content": (
            "As cities deploy IoT and digital infrastructure, cybersecurity becomes critical. Key vulnerabilities: "
            "SCADA systems controlling water/power, traffic management systems, surveillance networks, and citizen data "
            "platforms. Best practices: (1) Zero-trust architecture — authenticate every device and user continuously. "
            "(2) Network segmentation isolating critical infrastructure from general IT networks. (3) Regular penetration "
            "testing (quarterly) and vulnerability assessments. (4) Incident response plans with <4 hour detection, "
            "<24 hour containment targets. (5) Staff training — 85% of breaches involve human error. Cities should "
            "budget 10-15% of IT spend on cybersecurity."
        ),
        "tags": ["cybersecurity", "smart city", "IoT", "infrastructure", "data", "security"],
        "confidence_base": 0.88,
    },

    # ─────────────────────────────────────────────
    #  DOMAIN 4: Healthcare Access & Wellness
    # ─────────────────────────────────────────────
    {
        "id": "health_001",
        "domain": "Healthcare Access & Wellness",
        "title": "Primary Healthcare Access Gaps",
        "content": (
            "Healthcare deserts — areas with inadequate primary care access — affect 150+ million Americans. Indicators: "
            "Primary Care Physician (PCP) ratio below 1:3,500 population, >30-minute travel time to nearest clinic, "
            "or >3-week wait for routine appointment. Solutions: (1) Federally Qualified Health Centers (FQHCs) provide "
            "sliding-scale care regardless of ability to pay. (2) Mobile health clinics serve rural/underserved areas "
            "at 60% lower cost than fixed facilities. (3) Telehealth expansion has increased access for 24% of previously "
            "unserved patients. (4) Nurse Practitioner scope-of-practice expansion increases provider supply by 20-30%. "
            "Mapping healthcare access overlaid with social determinants reveals compounding vulnerability."
        ),
        "tags": ["healthcare", "access", "primary care", "clinic", "telehealth", "equity"],
        "confidence_base": 0.90,
    },
    {
        "id": "health_002",
        "domain": "Healthcare Access & Wellness",
        "title": "Mental Health and Community Wellness Programs",
        "content": (
            "Mental health conditions affect 1 in 4 adults and cost cities $200-400 per capita annually in lost "
            "productivity and crisis services. Community wellness strategies: (1) Integrate mental health screening "
            "into primary care (collaborative care model increases treatment by 50%). (2) Peer support programs — "
            "individuals in recovery providing mentorship — reduce hospitalization by 23%. (3) Crisis Stabilization "
            "Units (CSUs) divert 70-80% of mental health crisis calls from ERs. (4) Green spaces and parks improve "
            "mental health outcomes; 10 minutes in nature reduces cortisol by 20%. (5) Community mental health "
            "navigators connecting residents to services reduce barriers for marginalized populations."
        ),
        "tags": ["mental health", "wellness", "crisis", "community", "parks", "support"],
        "confidence_base": 0.88,
    },
    {
        "id": "health_003",
        "domain": "Healthcare Access & Wellness",
        "title": "Chronic Disease Prevention and Management",
        "content": (
            "Chronic diseases (diabetes, hypertension, heart disease, obesity) account for 75% of healthcare costs. "
            "Prevention strategies with strong evidence: (1) Community health worker programs reduce ER visits by 30% "
            "for high-risk patients ($1 invested returns $3-8). (2) Food access programs — community gardens, "
            "farmers markets in food deserts — increase fruit/vegetable consumption by 25%. (3) Walkable neighborhood "
            "design increases physical activity by 35-45% (people in walkable areas walk 89 more minutes/week). "
            "(4) Diabetes Prevention Program (DPP) reduces Type 2 diabetes incidence by 58%. A city chronic disease "
            "prevention budget of $20-50 per capita annually can save $200-500 per capita in avoidable healthcare costs."
        ),
        "tags": ["chronic disease", "diabetes", "prevention", "obesity", "food", "walkable"],
        "confidence_base": 0.89,
    },
    {
        "id": "health_004",
        "domain": "Healthcare Access & Wellness",
        "title": "Maternal and Child Health Outcomes",
        "content": (
            "Maternal mortality in the US (23.8 per 100,000) is 3-4x higher than comparable wealthy nations. Infant "
            "mortality varies 3-fold between urban neighborhoods based on income and race. Key interventions: (1) "
            "Doula and midwifery services reduce C-section rates by 39% and preterm birth by 30%. (2) Home visiting "
            "programs (Nurse-Family Partnership) improve birth outcomes and reduce child abuse by 50%. (3) Breastfeeding "
            "support — lactation consultants and workplace lactation rooms — achieve 6-month breastfeeding rates of "
            "60%+ (national average: 57%). (4) Food support (WIC program) reduces low birth weight by 25%. "
            "Addressing maternal/child health inequity requires coordinated multi-sector approaches."
        ),
        "tags": ["maternal", "child health", "infant mortality", "pregnancy", "equity", "WIC"],
        "confidence_base": 0.87,
    },
    {
        "id": "health_005",
        "domain": "Healthcare Access & Wellness",
        "title": "Digital Health and Telemedicine",
        "content": (
            "Telemedicine has expanded dramatically: 65-fold increase in utilization during COVID-19, with 38% sustained "
            "utilization. Benefits: (1) Reduces travel time and cost (average $45 saved per visit). (2) Increases access "
            "for elderly, disabled, and rural patients. (3) Enables remote monitoring of chronic conditions (wearables, "
            "connected devices) reducing hospital readmissions by 25%. (4) AI-assisted triage tools can handle 30% of "
            "routine queries without physician involvement. Equity considerations: 15% of low-income households lack "
            "broadband; digital literacy programs and device lending essential for equitable telehealth."
        ),
        "tags": ["telemedicine", "digital health", "remote", "wearable", "AI", "broadband"],
        "confidence_base": 0.88,
    },

    # ─────────────────────────────────────────────
    #  DOMAIN 5: Waste Management & Resource Optimization
    # ─────────────────────────────────────────────
    {
        "id": "waste_001",
        "domain": "Waste Management & Resource Optimization",
        "title": "Zero Waste Strategy and Circular Economy",
        "content": (
            "Zero Waste strategies target 90%+ landfill diversion through waste reduction, reuse, and recycling. "
            "Key pillars: (1) Extended Producer Responsibility (EPR) — manufacturers responsible for end-of-life "
            "product management — has increased recycling rates by 40-60% in European cities. (2) Organics diversion: "
            "composting food and yard waste (typically 40% of municipal waste stream) produces compost worth "
            "$30-60/tonne and reduces methane emissions. (3) Pay-As-You-Throw (PAYT) pricing increases recycling "
            "participation by 25-35%. (4) Repair cafes and reuse centers divert 500-2,000 tonnes/year per city. "
            "San Francisco achieves 80% landfill diversion. Top performers: Ljubljana, Slovenia at 68%."
        ),
        "tags": ["waste", "recycling", "zero waste", "circular economy", "compost", "landfill"],
        "confidence_base": 0.90,
    },
    {
        "id": "waste_002",
        "domain": "Waste Management & Resource Optimization",
        "title": "Smart Waste Collection Systems",
        "content": (
            "Traditional fixed-schedule waste collection wastes 30-40% of vehicle capacity. Smart systems: (1) IoT "
            "fill-level sensors in bins trigger collection only when 70-80% full, reducing collection trips by 50-80%. "
            "(2) AI-powered route optimization saves 20-30% in fuel costs. (3) Underground pneumatic waste systems "
            "(used in Stockholm, Barcelona) eliminate truck collection in dense areas entirely. (4) RFID-tagged bins "
            "enable accurate waste composition tracking and contamination identification. Smart waste systems have ROI "
            "periods of 3-5 years and reduce collection costs by $40-80 per household per year."
        ),
        "tags": ["smart waste", "IoT sensors", "collection", "route optimization", "RFID"],
        "confidence_base": 0.88,
    },
    {
        "id": "waste_003",
        "domain": "Waste Management & Resource Optimization",
        "title": "Food Waste Reduction Programs",
        "content": (
            "Food waste represents 30-40% of the food supply and 8% of global greenhouse gas emissions. City-level "
            "interventions: (1) Surplus food redistribution networks connecting restaurants/grocery stores with food "
            "banks (apps like Too Good To Go, Olio) — each tonne of food rescued saves 2.5 tCO2e. (2) Date label "
            "reform (replacing 'best before' with 'use by' only for safety-critical items) reduces household waste "
            "by 20%. (3) School and workplace composting education reduces organic waste by 30-40%. (4) Anaerobic "
            "digestion of food waste generates biogas (100 kWh per tonne) and digestate fertilizer. Cities with "
            "comprehensive food waste programs achieve 50-60% reduction in organics to landfill."
        ),
        "tags": ["food waste", "composting", "biogas", "redistribution", "organic", "greenhouse gas"],
        "confidence_base": 0.89,
    },
    {
        "id": "waste_004",
        "domain": "Waste Management & Resource Optimization",
        "title": "Water Conservation and Efficiency",
        "content": (
            "Urban water systems lose 20-30% of supply through leakage. Conservation strategies: (1) Smart meter "
            "rollout with real-time consumption feedback reduces household water use by 15-20%. (2) Leak detection "
            "using acoustic sensors and AI analysis identifies and prioritizes pipe repairs, reducing losses by "
            "25-40%. (3) Greywater recycling systems reuse 50-70 liters per household per day for irrigation. "
            "(4) Water-sensitive urban design (WSUD) integrates water management into urban planning. (5) Tiered "
            "pricing structures with low baseline rates and high excess rates reduce peak demand by 15%. "
            "Singapore achieves 142 liters per capita per day — among the world's most efficient."
        ),
        "tags": ["water", "conservation", "smart meter", "leakage", "efficiency", "recycling"],
        "confidence_base": 0.88,
    },
    {
        "id": "waste_005",
        "domain": "Waste Management & Resource Optimization",
        "title": "E-Waste and Hazardous Waste Management",
        "content": (
            "E-waste is the fastest-growing waste stream globally (53.6 million tonnes in 2019). Proper management: "
            "(1) Manufacturer take-back programs (required in EU WEEE Directive) achieve 45% collection rates. "
            "(2) Community e-waste collection events with certified recyclers ensure proper processing. (3) Refurbishment "
            "and repair programs extend device lifecycles — refurbished electronics use 80% less energy to produce than "
            "new devices. (4) Precious metal recovery: 1 tonne of e-waste contains 60x more gold than 1 tonne of ore. "
            "Hazardous household waste (paint, batteries, chemicals) requires separate collection infrastructure with "
            "at least 1 facility per 100,000 residents."
        ),
        "tags": ["e-waste", "electronics", "hazardous", "recycling", "refurbishment", "batteries"],
        "confidence_base": 0.86,
    },

    # ─────────────────────────────────────────────
    #  DOMAIN 6: Citizen Engagement & Public Services
    # ─────────────────────────────────────────────
    {
        "id": "civic_001",
        "domain": "Citizen Engagement & Public Services",
        "title": "Digital Government Services Transformation",
        "content": (
            "Digital government maturity is measured on a 5-level scale: (1) Informational, (2) Interactive, "
            "(3) Transactional, (4) Integrated, (5) Intelligent/Proactive. Most cities are at level 2-3. Moving to "
            "level 4-5 provides: 40-60% cost reduction in service delivery, 78% citizen satisfaction improvement, "
            "and 24/7 service availability. Key services to digitize: permit applications, business licensing, "
            "utility payments, service requests, and public feedback. Estonia's X-Road platform delivers 99% of "
            "government services online, saving citizens 1,400 years of working time annually."
        ),
        "tags": ["digital government", "e-government", "services", "citizen", "online", "Estonia"],
        "confidence_base": 0.90,
    },
    {
        "id": "civic_002",
        "domain": "Citizen Engagement & Public Services",
        "title": "Participatory Budgeting",
        "content": (
            "Participatory Budgeting (PB) gives citizens direct voice in public spending decisions. Models: (1) "
            "District PB — each district receives a fixed allocation ($500K-$5M) for residents to allocate. (2) "
            "Thematic PB — focused on specific domains (parks, schools, roads). (3) Digital PB — online platforms "
            "enable broader participation. Outcomes: PB programs increase civic participation by 25-30%, direct "
            "resources to underserved communities, and improve project quality through community input. New York City's "
            "PB program (since 2012) has engaged 500,000+ residents and funded 1,000+ projects. Implementation "
            "requires robust community outreach to reach non-English speakers and low-income residents."
        ),
        "tags": ["participatory budgeting", "civic", "community", "spending", "democracy", "engagement"],
        "confidence_base": 0.88,
    },
    {
        "id": "civic_003",
        "domain": "Citizen Engagement & Public Services",
        "title": "311 Service Request Systems and Analytics",
        "content": (
            "311 non-emergency service request systems handle 2-15 million requests annually in large cities. "
            "Modern 311 platforms: (1) Multi-channel intake: phone, app, web, social media, and AI chatbot. (2) "
            "GIS-integrated routing to correct department. (3) Predictive maintenance: ML models analyzing 311 data "
            "predict infrastructure failures 30-90 days before they occur. (4) Performance dashboards tracking "
            "response time SLAs by department and neighborhood. (5) Sentiment analysis of feedback for service "
            "quality monitoring. Cities with mature 311 analytics reduce average resolution time by 35% and "
            "identify systemic issues before they escalate."
        ),
        "tags": ["311", "service request", "reporting", "citizen", "maintenance", "analytics"],
        "confidence_base": 0.89,
    },
    {
        "id": "civic_004",
        "domain": "Citizen Engagement & Public Services",
        "title": "Inclusive Urban Planning and Community Voice",
        "content": (
            "Inclusive planning ensures all community members shape decisions that affect them. Methods: (1) Community "
            "engagement events in local languages with childcare and evening/weekend scheduling increase participation "
            "by 3-5x vs. standard public hearings. (2) Digital engagement platforms (Pol.is, Decidim) enable "
            "asynchronous input from 10-50x more residents than in-person events. (3) Equity impact assessments "
            "evaluate how proposed plans affect different demographic groups. (4) Resident advisory boards with "
            "paid stipends for low-income members ensure representation. (5) Results tracking: publishing how "
            "community input shaped final decisions builds trust and increases future participation."
        ),
        "tags": ["planning", "community", "engagement", "equity", "participation", "urban"],
        "confidence_base": 0.87,
    },
    {
        "id": "civic_005",
        "domain": "Citizen Engagement & Public Services",
        "title": "Open Data and Government Transparency",
        "content": (
            "Open government data programs publish datasets for public use, enabling civic innovation. Best practices: "
            "(1) Open data portals with machine-readable formats (JSON, CSV, API access) make data usable by developers. "
            "(2) High-value datasets to prioritize: budget and spending, property records, crime statistics, transit, "
            "and environmental quality. (3) Civic hackathons engage developers and community innovators. (4) Data "
            "quality standards ensure published data is accurate and current. Cities with mature open data programs "
            "generate $10-15 per resident in estimated economic value annually through third-party innovation. "
            "Privacy-by-design ensures open data does not expose personal information."
        ),
        "tags": ["open data", "transparency", "government", "API", "civic tech", "innovation"],
        "confidence_base": 0.88,
    },
    {
        "id": "civic_006",
        "domain": "Citizen Engagement & Public Services",
        "title": "Social Services Integration and Navigation",
        "content": (
            "Fragmented social services create barriers for people who need multiple supports simultaneously. "
            "Integrated service delivery: (1) 'No wrong door' model — any point of contact can access and refer "
            "to the full service ecosystem. (2) Benefits screening tools (e.g., Benefits.gov, Aunt Bertha) identify "
            "all programs a family qualifies for — average family misses $5,000-$14,000 in benefits annually. "
            "(3) Case management systems share information (with consent) across housing, health, employment, and "
            "child welfare agencies. (4) Accountable care communities use data to identify and intervene with "
            "highest-need residents proactively. Integrated approaches reduce total cost of care by 15-25%."
        ),
        "tags": ["social services", "benefits", "integration", "housing", "navigation", "equity"],
        "confidence_base": 0.87,
    },

    # ─────────────────────────────────────────────
    #  BONUS: Cross-Domain & Smart City
    # ─────────────────────────────────────────────
    {
        "id": "smart_001",
        "domain": "Urban Mobility & Transportation",
        "title": "Autonomous Vehicle Readiness",
        "content": (
            "Cities preparing for autonomous vehicles (AVs) should focus on: (1) High-definition mapping of road "
            "network including lane markings, signage, and infrastructure. (2) V2X (vehicle-to-everything) "
            "communication infrastructure enabling vehicles to communicate with signals, signs, and pedestrians. "
            "(3) Regulatory frameworks for AV testing and deployment zones. (4) Curb management policies "
            "as AVs will dramatically increase drop-off/pick-up activity. (5) AV-ready zoning reducing minimum "
            "parking requirements. Full AV deployment could reduce crash fatalities by 90% and travel time by "
            "40% through platooning and coordinated signal systems."
        ),
        "tags": ["autonomous vehicle", "AV", "self-driving", "V2X", "future mobility"],
        "confidence_base": 0.83,
    },
    {
        "id": "smart_002",
        "domain": "Environmental Sustainability & Climate Resilience",
        "title": "Urban Agriculture and Food Systems",
        "content": (
            "Urban agriculture can supply 15-20% of a city's vegetable needs. Approaches: (1) Rooftop farms and "
            "greenhouses use hydroponic systems that produce 10-20x more food per square meter than conventional "
            "farming with 90% less water. (2) Community gardens provide food, social cohesion, and green space. "
            "(3) Vertical farms in repurposed industrial buildings can grow year-round with 95% water savings. "
            "(4) School gardens improve nutrition knowledge and healthy eating behaviors in children. Integration "
            "of urban farms into school and hospital procurement reduces food miles and improves diet quality. "
            "Detroit's urban farming movement has transformed 1,400+ vacant lots."
        ),
        "tags": ["urban agriculture", "food", "farming", "rooftop", "hydroponic", "community garden"],
        "confidence_base": 0.85,
    },
    {
        "id": "smart_003",
        "domain": "Citizen Engagement & Public Services",
        "title": "Affordable Housing and Zoning Reform",
        "content": (
            "Housing affordability crisis: 50% of renters are cost-burdened (>30% income on housing) in major cities. "
            "Solutions: (1) Inclusive zoning/density bonuses — developers get height bonuses in exchange for 10-20% "
            "affordable units. (2) Missing middle housing (duplexes, triplexes, townhouses) increases supply without "
            "high-rise construction. (3) Social housing land banks — public acquisition of land for permanently "
            "affordable housing. (4) Community land trusts remove land from speculative market. (5) Anti-displacement "
            "policies: just-cause eviction, rent stabilization, and right of first refusal for long-term tenants. "
            "Minneapolis's 2040 Plan (eliminating single-family zoning citywide) increased housing permits by 23%."
        ),
        "tags": ["housing", "affordable", "zoning", "rent", "equity", "displacement"],
        "confidence_base": 0.87,
    },
    {
        "id": "smart_004",
        "domain": "Public Safety & Emergency Preparedness",
        "title": "Climate Emergency Preparedness",
        "content": (
            "Cities face compound climate risks: floods, extreme heat, wildfires, and sea-level rise. Preparedness "
            "framework: (1) Climate risk assessment mapping all neighborhoods by vulnerability and exposure. "
            "(2) Heat action plans with cooling centers (1 per 10,000 residents), misting stations, and proactive "
            "wellness checks on vulnerable residents during heat events. (3) Community resilience hubs: "
            "neighborhood facilities that function as resource centers during and after disasters. (4) Business "
            "continuity planning for essential services. (5) Mutual aid networks: connecting neighbors for "
            "community self-help. Each $1 spent on climate preparedness avoids $4-11 in disaster recovery costs."
        ),
        "tags": ["climate", "emergency", "heat", "flood", "resilience", "preparedness"],
        "confidence_base": 0.90,
    },
    {
        "id": "smart_005",
        "domain": "Waste Management & Resource Optimization",
        "title": "Plastic Reduction and Single-Use Ban Programs",
        "content": (
            "Single-use plastics represent 50% of ocean plastic pollution. City-level interventions: (1) Single-use "
            "plastic bans (bags, straws, cups) with 6-12 month transition periods — effective when paired with "
            "alternatives infrastructure. (2) Plastic reduction levies (5-10 cents per bag) reduce consumption "
            "by 70-90%. (3) Reusable container programs for takeout (deposit-return system with app) reduce "
            "container waste by 90% in pilots. (4) Deposit-return systems (DRS) for bottles achieve 90%+ "
            "collection rates in Nordic countries vs. 30-50% in non-DRS states. (5) Plastic pollution monitoring "
            "in waterways tracks progress and identifies hotspots."
        ),
        "tags": ["plastic", "single-use", "ban", "ocean", "recycling", "deposit return"],
        "confidence_base": 0.88,
    },
]

# Domain color mapping for UI
DOMAIN_COLORS = {
    "Urban Mobility & Transportation": "#4CC9F0",
    "Environmental Sustainability & Climate Resilience": "#4ADE80",
    "Public Safety & Emergency Preparedness": "#F97316",
    "Healthcare Access & Wellness": "#EC4899",
    "Waste Management & Resource Optimization": "#A78BFA",
    "Citizen Engagement & Public Services": "#FBBF24",
}

# Domain icons
DOMAIN_ICONS = {
    "Urban Mobility & Transportation": "🚌",
    "Environmental Sustainability & Climate Resilience": "🌿",
    "Public Safety & Emergency Preparedness": "🚨",
    "Healthcare Access & Wellness": "🏥",
    "Waste Management & Resource Optimization": "♻️",
    "Citizen Engagement & Public Services": "🏛️",
}

ALL_DOMAINS = list(DOMAIN_COLORS.keys())

def get_all_chunks():
    """Return all knowledge chunks."""
    return KNOWLEDGE_BASE

def get_chunks_by_domain(domain: str):
    """Return knowledge chunks for a specific domain."""
    return [c for c in KNOWLEDGE_BASE if c["domain"] == domain]

def get_chunk_by_id(chunk_id: str):
    """Return a specific chunk by ID."""
    for c in KNOWLEDGE_BASE:
        if c["id"] == chunk_id:
            return c
    return None
