# 🏙️ VitaCity AI — Decision Intelligence Platform

> **Intelligent Assistant for Better Living and Smarter Communities**
> Powered by Google Gemini + RAG · Built for Google Cloud Hackathon 2026

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red.svg)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.0-green.svg)](https://ai.google.dev)
[![Cloud Run](https://img.shields.io/badge/Google%20Cloud-Cloud%20Run-blue.svg)](https://cloud.google.com/run)

---

## ✨ What is VitaCity AI?

VitaCity AI is a production-ready **Decision Intelligence Platform** that helps citizens, city planners, and community organizations make smarter, evidence-based decisions across six key urban domains:

| Domain | Focus Area |
|--------|-----------|
| 🚌 **Urban Mobility** | Transit, traffic, EVs, cycling, pedestrian safety |
| 🌿 **Environment** | Carbon reduction, air quality, flood resilience, renewables |
| 🚨 **Public Safety** | Emergency response, crime prevention, disaster preparedness |
| 🏥 **Healthcare** | Primary care access, mental health, telehealth, chronic disease |
| ♻️ **Waste Management** | Zero waste, smart collection, food waste, e-waste |
| 🏛️ **Civic Engagement** | Digital government, participatory budgeting, 311, open data |

---

## 🚀 Features

### 🤖 Smart Chat Interface
- Conversational AI powered by **Gemini 2.0 Flash**
- **RAG (Retrieval-Augmented Generation)** over 35+ curated knowledge chunks
- 6 quick-start scenario buttons for impressive demos
- **Multimodal image analysis** — upload photos of potholes, waste, or floods
- Per-response confidence scores, source citations, and follow-up questions

### 📊 City Intelligence Dashboard
- 30+ live KPI metrics across 6 domains
- Interactive **Plotly charts** (line, bar, radar, donut)
- 12-district performance comparison with colored scoring
- Real-time city alerts panel
- AI decision query log

### 🎯 Decision Simulator
- Input any proposed policy or investment decision
- **5-dimension impact scoring**: Environmental, Economic, Social Equity, Health & Safety, Mobility
- Timeline projection chart with confidence decay
- Risk assessment matrix
- Cost-benefit summary

### ⚖️ Responsible AI Framework
- RAG architecture visualization
- Confidence methodology explanation
- Model transparency card
- Bias mitigation principles
- Data sources and known limitations

---

## 🛠️ Quick Start (Local)

### Prerequisites
- Python 3.11+
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 1. Clone and Setup

```bash
# Navigate to project directory
cd "GEN AI"

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your Gemini API key:
# GEMINI_API_KEY=your_key_here
```

### 4. Run the App

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

> **Note:** The app works in **Demo Mode** without a Gemini API key, showing curated, realistic responses. Add your key for live Gemini inference.

---

## ☁️ Deploy to Google Cloud Run

### Prerequisites
- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated
- Docker installed

### 1. Set Up Google Cloud Project

```bash
# Set your project
export PROJECT_ID="your-gcp-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com
```

### 2. Create Artifact Registry Repository

```bash
gcloud artifacts repositories create vitacityai \
  --repository-format=docker \
  --location=us-central1 \
  --description="VitaCity AI container registry"
```

### 3. Store API Key as Secret

```bash
echo -n "your_gemini_api_key" | \
  gcloud secrets create vitacityai-gemini-key \
    --data-file=- \
    --replication-policy=automatic

# Grant Cloud Build access to the secret
gcloud secrets add-iam-policy-binding vitacityai-gemini-key \
  --member="serviceAccount:$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')@cloudbuild.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Grant Cloud Run access to the secret
gcloud secrets add-iam-policy-binding vitacityai-gemini-key \
  --member="serviceAccount:$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 4. Deploy

```bash
# Submit build and deploy to Cloud Run
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_SERVICE_NAME=vitacityai,_REGION=us-central1
```

### 5. Get the Service URL

```bash
gcloud run services describe vitacityai \
  --region=us-central1 \
  --format='value(status.url)'
```

---

## 🏗️ Architecture

```
app.py                          # Streamlit main entry point
├── ui/
│   ├── theme.py                # Premium dark-mode CSS & HTML helpers
│   ├── components.py           # Shared Plotly charts & UI components
│   ├── chat_page.py            # AI chat with RAG + multimodal
│   ├── dashboard_page.py       # KPIs, charts, district comparison
│   ├── simulator_page.py       # Decision impact simulator
│   └── responsible_ai_page.py  # Explainability & transparency
├── core/
│   ├── gemini_client.py        # Gemini 2.0 Flash wrapper (text + vision)
│   ├── rag_engine.py           # TF-IDF RAG (scikit-learn, in-memory)
│   └── decision_simulator.py   # 5-dimension impact scoring engine
└── data/
    ├── knowledge_base.py       # 35+ knowledge chunks across 6 domains
    └── mock_metrics.py         # Realistic city KPIs and trend data
```

### Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit 1.40, Custom CSS, Plotly |
| AI Engine | Google Gemini 2.0 Flash (text + vision) |
| RAG | scikit-learn TF-IDF + Cosine Similarity |
| Data | Mock realistic city data (Metro Vitacity) |
| Deployment | Docker, Google Cloud Run |
| CI/CD | Google Cloud Build + Artifact Registry |

---

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API Key (required for live mode) | — |
| `GEMINI_MODEL` | Gemini model name | `gemini-2.0-flash` |
| `APP_ENV` | `development` or `production` | `development` |
| `RAG_TOP_K` | Number of RAG chunks to retrieve | `5` |

---

## 🎯 Demo Scenarios

Try these questions in the chat interface:

1. **"What are the top 3 causes of traffic congestion in our district?"**
   - Gets BRT recommendations, signal timing analysis, congestion pricing ROI

2. **"How can we reduce our city's carbon footprint by 20% in 5 years?"**
   - Full sector breakdown, cost estimates, renewable energy pathway

3. **"Which neighborhoods have the lowest emergency response times?"**
   - District-level analysis, CPTED recommendations, CFR program ROI

4. **"Where are the healthcare deserts and how do we fix them?"**
   - Mobile clinic proposals, telehealth equity, mental health access

5. **"What waste reduction programs have the highest ROI?"**
   - Smart bins ROI, composting targets, contamination reduction

6. **Upload a pothole photo** → AI severity assessment + repair priority + cost estimate

---

## 📋 Google Cloud Best Practices Applied

- ✅ **Containerization** — Docker multi-stage build for minimal image size
- ✅ **Secret Management** — Gemini API key stored in Secret Manager (not env vars in prod)
- ✅ **Cloud Run** — Serverless, auto-scaling, pay-per-request
- ✅ **Artifact Registry** — Container images stored in GCP Artifact Registry
- ✅ **IAM Least Privilege** — Cloud Run service account with minimum permissions
- ✅ **Health Checks** — Streamlit health endpoint monitored
- ✅ **Responsible AI** — Follows Google's AI Principles: Fair, Safe, Accountable

---

## 🤝 Contributing

This project was built for the **Google Cloud Hackathon 2026**. The codebase is structured for extensibility:

- **Swap RAG backend**: Replace TF-IDF with Vertex AI Vector Search for production scale
- **Add domains**: Extend `data/knowledge_base.py` with new knowledge chunks
- **Add pages**: Create new `ui/<page_name>.py` and register in `app.py`
- **Real data**: Replace `data/mock_metrics.py` with live API connections (BigQuery, Pub/Sub)

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

*VitaCity AI — Making cities smarter, one decision at a time. 🏙️*
