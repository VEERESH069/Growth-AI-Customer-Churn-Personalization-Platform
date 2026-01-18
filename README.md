# 🚀 GrowthAI - Customer Churn & Personalization Platform

An **industry-grade AI platform** that predicts customer churn, generates personalized recommendations, and creates AI-powered retention campaigns.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange)

## ✨ Features

- **🔮 Churn Prediction** - XGBoost ML model to identify at-risk customers
- **🎯 Personalized Recommendations** - Hybrid semantic search using SentenceTransformers
- **✉️ AI Campaign Generator** - Gemini-powered retention email drafting
- **📊 Executive Dashboard** - Beautiful Streamlit UI with real-time analytics

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Streamlit     │────▶│    FastAPI      │────▶│   ML Models     │
│   Frontend      │     │    Backend      │     │  XGBoost/SBERT  │
│   (Port 8501)   │     │   (Port 8000)   │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  Gemini AI      │
                        │  (GenAI)        │
                        └─────────────────┘
```

## 🚀 Quick Start

### Option 1: Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/GrowthAI-Customer-Churn-Platform.git
cd GrowthAI-Customer-Churn-Platform

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set environment variable (optional, for AI emails)
$env:GEMINI_API_KEY = "your-api-key"  # PowerShell
# export GEMINI_API_KEY="your-api-key"  # Bash

# Terminal 1: Start Backend
uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Start Frontend
streamlit run src/app/streamlit_app.py
```

### Option 2: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access:
# - Frontend: http://localhost:8501
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

## 📁 Project Structure

```
├── src/
│   ├── api/
│   │   └── main.py              # FastAPI endpoints
│   ├── app/
│   │   └── streamlit_app.py     # Streamlit dashboard
│   ├── models/
│   │   ├── train_churn_model.py # XGBoost training
│   │   └── personalization.py   # Recommendation engine
│   ├── services/
│   │   └── gemini_service.py    # GenAI integration
│   └── data/
│       └── models.py            # SQLAlchemy models
├── data/
│   └── raw/                     # CSV datasets
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.streamlit
└── requirements.txt
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/data/customers` | GET | List all customers |
| `/data/customer/{id}` | GET | Get customer details |
| `/predict/churn` | POST | Predict churn risk |
| `/recommend` | POST | Get personalized recommendations |
| `/campaign/generate` | POST | Generate retention email |

## 🌐 Cloud Deployment

### Deploy to Railway
1. Push to GitHub
2. Connect repo to [Railway](https://railway.app)
3. Set environment variables (`GEMINI_API_KEY`)
4. Deploy!

### Deploy to Render
1. Create Web Service for API (Dockerfile)
2. Create Web Service for Frontend (Dockerfile.streamlit)
3. Link services via internal networking

### Deploy to AWS/GCP
- Use ECS/Cloud Run with the provided Dockerfiles
- Set up load balancer for production traffic

## 📊 Data

- **45 Customers** with segments (Budget, Premium, Tech-Savvy, Casual)
- **120 Products** (Electronics, Fashion, Home, Entertainment)
- **200 Content Items** (Movies, Articles, Podcasts)
- **700+ Interactions** for training the recommendation engine

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn, SQLAlchemy
- **Frontend**: Streamlit
- **ML**: XGBoost, Scikit-learn, SentenceTransformers
- **GenAI**: Google Gemini
- **Data**: Pandas, NumPy
- **Deployment**: Docker, Docker Compose

## 📝 License

MIT License

## 👨‍💻 Author

Built with ❤️ using AI-assisted development
