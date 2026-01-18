# GrowthAI  Customer Churn & Personalization Platform

GrowthAI is a production-ready AI platform designed to help businesses predict customer churn, personalize engagement, and automate retention workflows using a combination of classical machine learning, semantic search, and generative AI.

The system is built with clear service boundaries, model-driven decisioning, and a scalable API-first architecture suitable for real-world deployment.

What This Platform Does

GrowthAI addresses three high-impact customer lifecycle problems:

Churn Risk Identification — Predict which customers are likely to leave

Personalized Engagement — Recommend products and content tailored to user behavior

Automated Retention Campaigns — Generate targeted, AI-powered outreach at scale

## Key Capabilities
# Churn Prediction

Gradient-boosted decision tree model (XGBoost)

Trained on structured customer behavior and interaction data

Outputs churn probability and risk classification

Designed for low-latency, API-based inference

# Personalized Recommendations

Hybrid recommendation system combining:

Behavioral signals

Semantic similarity using SentenceTransformers

Supports personalized product and content ranking

Designed to be model-agnostic and extensible

# AI-Powered Retention Campaigns

Gemini-powered generative AI service

Automatically drafts personalized retention emails

Context-aware prompting using customer profile + churn risk

Clean service abstraction for easy model replacement

# Executive Analytics Dashboard

Streamlit-based frontend for rapid iteration and visibility

Real-time churn metrics and customer segmentation

Designed for product managers and growth teams

**System Architecture**
┌──────────────────┐      ┌──────────────────┐      ┌────────────────────┐
│   Streamlit UI   │ ───▶ │   FastAPI        │ ───▶ │  ML Services        │
│   Frontend       │      │   Backend        │      │  XGBoost / SBERT    │
│   (8501)         │      │   (8000)         │      │                    │
└──────────────────┘      └──────────────────┘      └────────────────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │   Gemini AI       │
                          │   GenAI Service   │
                          └──────────────────┘


**Design Principles**

API-first backend

Stateless services

Clear separation of ML, GenAI, and presentation layers

Container-ready for cloud deployment

## Tech Stack
# Backend

FastAPI — High-performance API framework

Uvicorn — ASGI server

SQLAlchemy — ORM for data access and modeling

# Frontend

Streamlit — Interactive analytics and control plane UI

## Machine Learning

XGBoost — Churn prediction model

Scikit-learn — Feature preprocessing and evaluation

SentenceTransformers (SBERT) — Semantic embeddings for personalization

# Generative AI

Google Gemini — Retention email generation

# Data & Utilities

Pandas, NumPy — Data processing and feature engineering

## Deployment

Docker, Docker Compose — Containerization and local orchestration

Cloud-ready for Render, Railway, AWS ECS, GCP Cloud Run

## API Surface
Endpoint	Method	Description
/	GET	Health check
/data/customers	GET	List customers
/data/customer/{id}	GET	Customer profile
/predict/churn	POST	Churn risk prediction
/recommend	POST	Personalized recommendations
/campaign/generate	POST	Generate retention email

Auto-generated OpenAPI docs available at:

/docs

**Project Structure**
src/
├── api/
│   └── main.py              # FastAPI application
├── app/
│   └── streamlit_app.py     # Analytics dashboard
├── models/
│   ├── train_churn_model.py # XGBoost training pipeline
│   └── personalization.py  # Recommendation engine
├── services/
│   └── gemini_service.py    # GenAI abstraction
├── data/
│   └── models.py            # SQLAlchemy models
data/
└── raw/                     # Source datasets

**Data Overview**

45 customer profiles across multiple segments

120 products spanning key commerce categories

200 content items (articles, media, podcasts)

700+ interaction events for personalization training

Deployment Options
Local Development

Python virtual environment

FastAPI + Streamlit running independently

Hot reload enabled for rapid iteration

**Docker (Recommended)**

Fully containerized services

Single docker-compose up for local parity with production

**Cloud**

Railway / Render — Managed container services

AWS ECS / GCP Cloud Run — Production-grade deployment

Designed for horizontal scaling and service isolation

**Engineering Highlights**

Clean service boundaries between ML, GenAI, and API layers

Model inference exposed via stable REST interfaces

Extensible design for swapping models or vendors

Built for observability, reproducibility, and deployment realism

## License

MIT

**Author Note**

This project reflects how modern AI platforms are built in practice:
predictive models for decisioning, semantic systems for personalization, and generative AI for automation combined into a cohesive, deployable product.
