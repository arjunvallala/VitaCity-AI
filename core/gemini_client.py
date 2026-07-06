"""
VitaCity AI — Gemini Client
Wraps the Google Gemini API (google-genai SDK) with structured prompting for city intelligence.
Supports both text chat and multimodal image analysis.
"""

import os
import json
import re
import logging
import io
from typing import Optional

from PIL import Image
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# ─── System prompt for VitaCity context ──────────────────────────────────────
SYSTEM_PROMPT = """You are VitaCity AI, an advanced Decision Intelligence Assistant for urban communities.
You help citizens, city planners, and community organizations make smarter, evidence-based decisions across six key domains:
1. Urban Mobility & Transportation
2. Environmental Sustainability & Climate Resilience
3. Public Safety & Emergency Preparedness
4. Healthcare Access & Wellness
5. Waste Management & Resource Optimization
6. Citizen Engagement & Public Services

Your responses must:
- Be grounded in the provided knowledge context (RAG)
- Give specific, actionable recommendations with measurable targets
- Reference real-world case studies and best practices when relevant
- Include confidence levels based on evidence strength
- Be professional but accessible — suitable for both citizens and city officials
- Identify trade-offs and potential unintended consequences
- Suggest next steps and implementation pathways

Always respond in valid JSON with this exact schema:
{
  "answer": "<comprehensive, well-structured answer in markdown>",
  "confidence": <float between 0.0 and 1.0>,
  "domain": "<primary domain name>",
  "key_recommendations": ["<rec1>", "<rec2>", "<rec3>"],
  "sources_used": ["<source title 1>", "<source title 2>"],
  "predicted_impact": "<brief impact statement>",
  "follow_up_questions": ["<question1>", "<question2>"]
}
"""

IMAGE_ANALYSIS_PROMPT = """You are VitaCity AI analyzing an urban infrastructure image for the city decision intelligence platform.

Analyze this image and provide:
1. What urban issue is visible (pothole, waste, flooding, safety hazard, etc.)
2. Severity assessment (Low / Medium / High / Critical)
3. Estimated repair/remediation priority score (1-10)
4. Recommended immediate actions
5. Estimated cost range for remediation
6. Which city department should be notified

Respond in valid JSON:
{
  "issue_detected": "<issue type>",
  "severity": "<Low|Medium|High|Critical>",
  "priority_score": <1-10>,
  "description": "<detailed description of what's visible>",
  "immediate_actions": ["<action1>", "<action2>"],
  "responsible_department": "<department name>",
  "cost_estimate": "<cost range>",
  "timeline": "<remediation timeline>",
  "confidence": <float between 0.0 and 1.0>
}
"""


def _try_import_genai():
    """Try to import the new google-genai SDK, fall back to old one."""
    try:
        from google import genai
        from google.genai import types
        return genai, types, "new"
    except ImportError:
        pass
    try:
        import google.generativeai as genai
        return genai, None, "old"
    except ImportError:
        return None, None, None


class GeminiClient:
    """Google Gemini API wrapper for VitaCity AI. Supports both google-genai and google-generativeai SDKs."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self._configured = False
        self._sdk_version = None
        self._client = None   # new SDK client
        self._model = None    # old SDK model

        if self.api_key:
            self._setup()

    def _setup(self):
        """Configure Gemini SDK — prefers new google-genai, falls back to old google-generativeai."""
        genai, types, version = _try_import_genai()
        if genai is None:
            logger.error("No Gemini SDK found. Install google-genai or google-generativeai.")
            return

        try:
            if version == "new":
                self._client = genai.Client(api_key=self.api_key)
                self._sdk_version = "new"
            else:
                # Old SDK
                genai.configure(api_key=self.api_key)
                generation_config = genai.GenerationConfig(
                    temperature=0.4,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                )
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ]
                self._model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    system_instruction=SYSTEM_PROMPT,
                )
                self._sdk_version = "old"
            self._configured = True
            logger.info(f"Gemini client configured ({self._sdk_version} SDK).")
        except Exception as e:
            logger.error(f"Gemini setup failed: {e}")
            self._configured = False

    @property
    def is_configured(self) -> bool:
        return self._configured and bool(self.api_key)

    def _parse_json_response(self, text: str) -> dict:
        """Robustly extract JSON from Gemini response text."""
        text = text.strip()
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0].strip()
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0].strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r'\{[\s\S]*\}', text)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
        return {}

    def _generate_with_new_sdk(self, prompt: str, system: str = None) -> str:
        """Generate text using the new google-genai SDK."""
        from google.genai import types
        config = types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=2048,
            system_instruction=system or SYSTEM_PROMPT,
        )
        response = self._client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )
        return response.text

    def _generate_with_new_sdk_multimodal(self, parts: list) -> str:
        """Generate content with mixed image+text using new SDK."""
        from google.genai import types
        config = types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=1024,
        )
        response = self._client.models.generate_content(
            model=self.model_name,
            contents=parts,
            config=config,
        )
        return response.text

    def chat(
        self,
        user_message: str,
        rag_context: str = "",
        chat_history: Optional[list] = None,
    ) -> dict:
        """
        Send a message to Gemini with optional RAG context.
        Returns a structured dict with answer, confidence, recommendations, etc.
        """
        if not self.is_configured:
            return self._demo_response(user_message)

        prompt_parts = []
        if rag_context:
            prompt_parts.append(
                f"## Relevant Knowledge Context (use this to ground your answer):\n\n{rag_context}\n\n---\n\n"
            )
        prompt_parts.append(f"## User Question:\n{user_message}")
        full_prompt = "".join(prompt_parts)

        try:
            if self._sdk_version == "new":
                text = self._generate_with_new_sdk(full_prompt)
            else:
                # Old SDK with chat history
                history = []
                if chat_history:
                    for msg in chat_history[-6:]:
                        role = "user" if msg["role"] == "user" else "model"
                        history.append({"role": role, "parts": [msg["content"]]})
                if history:
                    chat_session = self._model.start_chat(history=history)
                    response = chat_session.send_message(full_prompt)
                else:
                    response = self._model.generate_content(full_prompt)
                text = response.text

            result = self._parse_json_response(text)
            if result:
                return result
            return {
                "answer": text,
                "confidence": 0.80,
                "domain": "General",
                "key_recommendations": [],
                "sources_used": [],
                "predicted_impact": "Analysis complete.",
                "follow_up_questions": [],
            }
        except Exception as e:
            logger.error(f"Gemini chat error: {e}")
            return self._error_response(str(e))

    def analyze_image(self, image: Image.Image, context: str = "") -> dict:
        """Analyze an uploaded image for urban issues."""
        if not self.is_configured:
            return self._demo_image_response()

        try:
            prompt_text = IMAGE_ANALYSIS_PROMPT
            if context:
                prompt_text += f"\n\nAdditional context: {context}"

            if self._sdk_version == "new":
                # Convert PIL image to bytes for new SDK
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                buf.seek(0)
                from google.genai import types
                image_part = types.Part.from_bytes(
                    data=buf.getvalue(),
                    mime_type="image/png",
                )
                text = self._generate_with_new_sdk_multimodal([prompt_text, image_part])
            else:
                response = self._model.generate_content([prompt_text, image])
                text = response.text

            result = self._parse_json_response(text)
            if result:
                return result
            return {
                "issue_detected": "Urban infrastructure issue",
                "severity": "Medium",
                "priority_score": 6,
                "description": text,
                "immediate_actions": ["Inspect site", "File service request"],
                "responsible_department": "Public Works",
                "cost_estimate": "$5,000 - $15,000",
                "timeline": "2-4 weeks",
                "confidence": 0.75,
            }
        except Exception as e:
            logger.error(f"Image analysis error: {e}")
            return self._demo_image_response()

    def _demo_response(self, user_message: str) -> dict:
        """High-quality demo response when API key is not configured."""
        msg_lower = user_message.lower()

        if any(w in msg_lower for w in ["traffic", "congestion", "transit", "bus", "mobility", "transport"]):
            return {
                "answer": (
                    "## Traffic Congestion Analysis - Metro Vitacity\n\n"
                    "Based on our urban mobility data and AI analysis, the **top 3 causes** of traffic congestion in your district are:\n\n"
                    "### 1. Signal Timing Inefficiency (Impact: High)\n"
                    "Only **42% of intersections** have adaptive signal control. Fixed-cycle signals waste 18-22% of green-light time during off-peak hours, creating artificial bottlenecks.\n\n"
                    "### 2. Insufficient BRT Coverage (Impact: High)\n"
                    "The Riverside and Central Hub corridors handle **38,000 daily vehicle trips** but lack dedicated transit lanes. Adding BRT on these corridors would divert ~8,500 daily car trips to transit.\n\n"
                    "### 3. Single-Occupancy Vehicle Dominance (Impact: Medium)\n"
                    "**74% of commuters** drive alone. The city's average vehicle occupancy of 1.18 persons/vehicle is below the national benchmark of 1.54.\n\n"
                    "### Projected Improvements\n"
                    "| Intervention | Cost | Congestion Reduction | Timeline |\n"
                    "|---|---|---|---|\n"
                    "| Adaptive Signals | $2.4M | 12-18% | 6 months |\n"
                    "| Riverside BRT Lane | $8.1M | 22-28% | 18 months |\n"
                    "| Congestion Pricing | $1.2M | 8-15% | 3 months |\n\n"
                    "**Recommended starting point:** Adaptive signal deployment in the Central Hub district — highest ROI with 6-month implementation timeline."
                ),
                "confidence": 0.89,
                "domain": "Urban Mobility & Transportation",
                "key_recommendations": [
                    "Deploy adaptive traffic signals at 45 key intersections (est. 15% congestion reduction)",
                    "Launch Riverside BRT corridor with dedicated lanes and signal priority",
                    "Implement dynamic congestion pricing downtown ($2-5/day based on volume)",
                ],
                "sources_used": ["Traffic Congestion Root Causes", "Bus Rapid Transit Implementation", "Smart Parking Systems"],
                "predicted_impact": "Estimated 25-35% reduction in peak-hour congestion within 24 months, saving commuters an average of 11 minutes/day.",
                "follow_up_questions": [
                    "Which specific intersections have the worst signal timing?",
                    "What is the current park-and-ride capacity at transit nodes?",
                ],
            }

        elif any(w in msg_lower for w in ["carbon", "climate", "green", "emission", "environment", "renewable", "solar", "energy"]):
            return {
                "answer": (
                    "## Carbon Footprint Reduction Strategy - 20% in 5 Years\n\n"
                    "Achieving a **20% reduction** in Metro Vitacity's annual 1,842 kt CO2 requires cutting **368 kt CO2** by 2031.\n\n"
                    "### Current Emissions Breakdown\n"
                    "| Sector | Share | Reduction Target |\n"
                    "|---|---|---|\n"
                    "| Buildings | 35% | 100 kt CO2 |\n"
                    "| Transportation | 28% | 145 kt CO2 |\n"
                    "| Industry | 22% | 80 kt CO2 |\n"
                    "| Waste | 8% | 30 kt CO2 |\n"
                    "| Other | 7% | 13 kt CO2 |\n\n"
                    "### High-Impact Interventions\n\n"
                    "**1. Municipal Building Electrification** - Retrofit 840 city-owned buildings\n"
                    "- Estimated savings: **72 kt CO2/year** | Cost: $45M | Payback: 7 years\n\n"
                    "**2. Renewable Energy Transition** - Expand solar from 38% to 65%\n"
                    "- Estimated savings: **110 kt CO2/year** | Cost: $120M | Payback: 8 years\n\n"
                    "**3. E-Bus Fleet Replacement** - Replace 240 diesel buses\n"
                    "- Estimated savings: **58 kt CO2/year** | Cost: $85M | Payback: 9 years\n\n"
                    "**Quick Wins (Year 1):**\n"
                    "- LED streetlight upgrade: saves 8,400 tCO2/year at $3.2M cost\n"
                    "- Green procurement policy for all new city fleet purchases"
                ),
                "confidence": 0.91,
                "domain": "Environmental Sustainability & Climate Resilience",
                "key_recommendations": [
                    "Launch municipal building efficiency retrofit program targeting 30% energy reduction by 2028",
                    "Expand solar capacity from 142 MW to 280 MW through rooftop and community solar programs",
                    "Replace entire diesel bus fleet with electric vehicles on a 3-year rolling schedule",
                ],
                "sources_used": ["Urban Carbon Footprint Reduction Strategies", "Renewable Energy Transition for Municipalities"],
                "predicted_impact": "20-23% CO2 reduction achievable by 2031, saving an estimated $42M/year in energy costs.",
                "follow_up_questions": [
                    "What financing mechanisms are available (green bonds, PACE, grants)?",
                    "How can we track and verify emissions reductions in real-time?",
                ],
            }

        elif any(w in msg_lower for w in ["safety", "crime", "emergency", "police", "fire", "response", "ambulance"]):
            return {
                "answer": (
                    "## Public Safety Analysis - Metro Vitacity\n\n"
                    "Our AI analysis reveals significant **geographic disparities** in emergency response times.\n\n"
                    "### Emergency Response Time Analysis\n"
                    "| District | Fire Response | EMS Response | Status |\n"
                    "|---|---|---|---|\n"
                    "| Innovation Dist | 4.2 min | 5.8 min | Excellent |\n"
                    "| Northgate | 5.1 min | 6.9 min | Good |\n"
                    "| Southpark | 8.4 min | 11.2 min | Critical |\n"
                    "| Eastfield | 7.8 min | 10.1 min | Poor |\n\n"
                    "### Priority Recommendations\n\n"
                    "**Southpark District (Highest Priority):**\n"
                    "- Current 8.4-min fire response exceeds NFPA 1710 standard by 4+ minutes\n"
                    "- Recommended: Community First Responder (CFR) program\n"
                    "- Cost: $1.8M/year for CFR vs. $4.2M for new station\n\n"
                    "**Crime Prevention (City-wide):**\n"
                    "- Current rate: 18.4/1,000 (down 13% from 2024 - positive trend)\n"
                    "- CPTED audit recommended for 8 high-crime corridors\n\n"
                    "A $3.2M targeted safety investment package could:\n"
                    "- Reduce crime rate by 18-22% over 3 years\n"
                    "- Improve EMS response to <8 min citywide"
                ),
                "confidence": 0.90,
                "domain": "Public Safety & Emergency Preparedness",
                "key_recommendations": [
                    "Establish Community First Responder program in Southpark and Eastfield districts",
                    "Conduct CPTED audits and lighting upgrades on 8 identified high-crime corridors",
                    "Deploy AI-assisted predictive positioning for EMS units (12% response time improvement)",
                ],
                "sources_used": ["Emergency Response Time Optimization", "Crime Prevention Through Environmental Design (CPTED)"],
                "predicted_impact": "Southpark EMS response time reduced from 11.2 min to 7.8 min within 12 months.",
                "follow_up_questions": [
                    "What is the current staffing level at Southpark's nearest fire station?",
                    "Are there existing community organizations that could support a CFR program?",
                ],
            }

        elif any(w in msg_lower for w in ["health", "hospital", "medical", "clinic", "wellness", "mental", "doctor"]):
            return {
                "answer": (
                    "## Healthcare Access Assessment - Metro Vitacity\n\n"
                    "AI analysis reveals **critical gaps** in three areas of Metro Vitacity.\n\n"
                    "### Key Findings\n"
                    "- **2.8 PCPs per 10,000 residents** - below the 3.5 threshold\n"
                    "- **42% mental health access rate** - 57% of residents needing care cannot access it\n"
                    "- **Average ER wait: 48 minutes** - down from 62 min in January\n"
                    "- **Telehealth adoption: 12,400 visits/month** - growing 52% year-over-year\n\n"
                    "### Healthcare Desert Mapping\n"
                    "| District | PCP Ratio | Mental Health | Priority |\n"
                    "|---|---|---|---|\n"
                    "| Southpark | 1.2/10k | Poor | Critical |\n"
                    "| Harbor View | 2.1/10k | Limited | High |\n"
                    "| Eastfield | 2.4/10k | Fair | Medium |\n\n"
                    "### Intervention Recommendations\n\n"
                    "**1. Mobile Health Clinic (Southpark)** - $420K/year\n"
                    "- Serves 4,200 additional patients annually\n\n"
                    "**2. Mental Health Crisis Stabilization Unit** - $1.2M setup\n"
                    "- Diverts 70-80% of mental health ER visits\n\n"
                    "**3. Telehealth Equity Program** - $180K/year\n"
                    "- Device lending library (500 tablets) for low-income seniors"
                ),
                "confidence": 0.88,
                "domain": "Healthcare Access & Wellness",
                "key_recommendations": [
                    "Launch mobile health clinic serving Southpark (4,200 additional patients/year)",
                    "Establish Crisis Stabilization Unit to divert mental health ER visits",
                    "Expand telehealth equity program with device lending and digital literacy support",
                ],
                "sources_used": ["Primary Healthcare Access Gaps", "Mental Health and Community Wellness Programs"],
                "predicted_impact": "Addressing healthcare deserts could reduce preventable hospitalizations by 23% and save $8.4M/year.",
                "follow_up_questions": [
                    "Are there federal grants available for FQHC expansion in underserved areas?",
                    "What is the current wait time for mental health appointments in Southpark?",
                ],
            }

        elif any(w in msg_lower for w in ["waste", "recycle", "recycling", "garbage", "compost", "trash", "landfill"]):
            return {
                "answer": (
                    "## Waste Management Optimization - Metro Vitacity\n\n"
                    "Metro Vitacity achieves **71% landfill diversion** - above national average of 35% but below our 80% target.\n\n"
                    "### Current Performance\n"
                    "| Stream | Current | Target | Gap |\n"
                    "|---|---|---|---|\n"
                    "| Recycling | 44% | 55% | -11% |\n"
                    "| Composting | 27% | 35% | -8% |\n"
                    "| Landfill Diversion | 71% | 80% | -9% |\n\n"
                    "### Highest ROI Programs\n\n"
                    "**1. Organics Expansion** (ROI: 4.2x)\n"
                    "- Mandatory organics separation reaches 75%+ participation\n"
                    "- Generates 8,200+ tonnes of compost worth $410K in avoided landfill costs\n\n"
                    "**2. Smart Bin Scale-Up** (ROI: 3.8x)\n"
                    "- Expanding 2,840 to 4,200 bins saves $640K/year in collection costs\n\n"
                    "**3. Contamination Reduction Campaign** (ROI: 6.1x)\n"
                    "- Northgate contamination at 22% (above 15% threshold)\n"
                    "- Door-to-door education recovers 1,200 additional tonnes/year"
                ),
                "confidence": 0.93,
                "domain": "Waste Management & Resource Optimization",
                "key_recommendations": [
                    "Implement mandatory organics separation with 12-month community education campaign",
                    "Scale smart bin deployment from 2,840 to 4,200 units targeting dense areas",
                    "Launch contamination reduction campaign in Northgate and Central Hub districts",
                ],
                "sources_used": ["Zero Waste Strategy and Circular Economy", "Smart Waste Collection Systems"],
                "predicted_impact": "80% landfill diversion would save $2.1M/year and reduce GHG emissions by 12,400 tCO2e annually.",
                "follow_up_questions": [
                    "Is there capacity at the regional composting facility for increased organics volumes?",
                    "What incentives can we offer residents to increase recycling participation?",
                ],
            }

        elif any(w in msg_lower for w in ["citizen", "civic", "engagement", "government", "participation", "service", "311"]):
            return {
                "answer": (
                    "## Citizen Engagement Strategy - Metro Vitacity\n\n"
                    "Metro Vitacity's civic engagement score of **65/100** is the lowest of all six domains.\n\n"
                    "### Current Engagement Metrics\n"
                    "- **Civic App Users:** 84,200 (16.4% of population - target: 35%)\n"
                    "- **311 Resolution Time:** 4.2 days (target: 2.0 days)\n"
                    "- **Digital Services Rate:** 72%\n"
                    "- **Participatory Budget Participants:** 12,800 (2.5% of population)\n\n"
                    "### Engagement Acceleration Strategy\n\n"
                    "**1. Multilingual Digital Platform Expansion**\n"
                    "- Current: English and Spanish only\n"
                    "- Adding 8 languages spoken by 5,000+ residents each\n"
                    "- Projected: +24,000 additional app users\n\n"
                    "**2. 311 AI Chatbot Integration**\n"
                    "- AI chatbot handles 65% of routine requests automatically\n"
                    "- Reduces resolution time from 4.2 to 1.8 days\n"
                    "- Estimated savings: $840K/year in staff time\n\n"
                    "**3. Neighborhood Innovation Budget ($500K/district)**\n"
                    "- Annual participatory budget in each of 12 districts\n"
                    "- Track record: increases participation by 3-5x over 3 years"
                ),
                "confidence": 0.87,
                "domain": "Citizen Engagement & Public Services",
                "key_recommendations": [
                    "Expand civic platform to 10 languages, targeting 35% population engagement by 2027",
                    "Deploy AI-powered 311 chatbot to reduce resolution time from 4.2 to <2.0 days",
                    "Launch $500K/district participatory budgeting across all 12 districts",
                ],
                "sources_used": ["Digital Government Services Transformation", "Participatory Budgeting"],
                "predicted_impact": "Tripling civic engagement from 16% to 35% could improve service delivery outcomes by 40%.",
                "follow_up_questions": [
                    "Which neighborhoods have the lowest civic app adoption rates?",
                    "What are the top 5 service requests in the 311 system this year?",
                ],
            }

        else:
            return {
                "answer": (
                    "## VitaCity AI - Decision Intelligence Response\n\n"
                    "Thank you for your question. Based on Metro Vitacity's integrated urban data platform, "
                    "I've analyzed the relevant factors across our six domains:\n\n"
                    "**Urban Mobility | Environment | Safety | Healthcare | Waste | Civic Engagement**\n\n"
                    "### Recommended Action Framework\n"
                    "1. **Diagnose** - Gather neighborhood-level data to identify root causes\n"
                    "2. **Prioritize** - Use equity mapping to identify highest-need communities first\n"
                    "3. **Design** - Co-create solutions with community members\n"
                    "4. **Implement** - Pilot in 1-2 districts before city-wide scale\n"
                    "5. **Measure** - Track KPIs with 90-day review cycles\n\n"
                    "Please try one of the quick-start scenarios or ask a specific question about any of the six urban domains."
                ),
                "confidence": 0.78,
                "domain": "General",
                "key_recommendations": [
                    "Use the Domain filter to focus your query on a specific urban challenge",
                    "Try the Decision Simulator for policy impact analysis",
                    "Explore the Dashboard for current city metrics across all domains",
                ],
                "sources_used": [],
                "predicted_impact": "Integrated urban intelligence improves decision quality by an average of 35%.",
                "follow_up_questions": [
                    "What specific district or neighborhood are you focused on?",
                    "What is the primary outcome you want to improve?",
                ],
            }

    def _demo_image_response(self) -> dict:
        return {
            "issue_detected": "Road Pavement Deterioration (Pothole)",
            "severity": "High",
            "priority_score": 8,
            "description": (
                "The image shows significant road surface degradation with multiple potholes ranging from "
                "15-40 cm in diameter and 5-12 cm in depth. The affected area covers approximately 12 m2 "
                "of the lane. Edge cracking and base course exposure are visible, indicating advanced "
                "deterioration that poses risk of vehicle damage and cyclist hazard."
            ),
            "immediate_actions": [
                "Place temporary warning signs and traffic cones around affected area",
                "File emergency repair work order with Public Works (target: 48-hour response)",
                "Notify traffic management to reduce speed limit to 20 km/h on affected block",
            ],
            "responsible_department": "Public Works - Road Maintenance Division",
            "cost_estimate": "$2,800 - $4,500 (temporary patch) | $18,000 - $26,000 (full resurfacing)",
            "timeline": "Emergency patch: 48 hours | Full remediation: 2-3 weeks",
            "confidence": 0.87,
        }

    def _error_response(self, error_msg: str) -> dict:
        return {
            "answer": (
                f"I encountered a temporary issue processing your request. "
                f"Please check your API key configuration and try again.\n\n"
                f"**Technical details:** {error_msg[:200]}"
            ),
            "confidence": 0.0,
            "domain": "Error",
            "key_recommendations": ["Check GEMINI_API_KEY in your .env file"],
            "sources_used": [],
            "predicted_impact": "N/A",
            "follow_up_questions": [],
        }


# Singleton
_client: Optional[GeminiClient] = None

def get_gemini_client() -> GeminiClient:
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client
