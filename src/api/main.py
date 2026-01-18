from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np
import os
from typing import List, Optional, Any

# Database
from sqlalchemy.orm import Session
from src.data.database import get_db, engine, Base
from src.data.models import Customer, MarketingInteraction

# AI Services
from src.services.gemini_service import GeminiRetentionService
from src.models.personalization import PersonalizationEngine

# Init DB Tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GrowthAI Churn & Personalization API")

# Initialize Services
gemini = GeminiRetentionService()

# Global RecSys Engine
recsys_engine = PersonalizationEngine()

# Load Models (Lazy loading or global)
churn_model = None

def load_churn_model():
    global churn_model
    try:
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'churn_model.pkl')
        if os.path.exists(model_path):
            churn_model = joblib.load(model_path)
            print("Churn model loaded.")
        else:
            print("Churn model not found. API running without ML model.")
    except Exception as e:
        print(f"Error loading model: {e}")
        churn_model = None

# Input Schemas
class ChurnInput(BaseModel):
    customer_id: str
    age: int = 30
    recency_days: float
    frequency_total: int = 10
    frequency_30d: int
    avg_order_value: float
    category_diversity: int
    login_count_14d: int
    country: Optional[str] = "US"

class ChurnResponse(BaseModel):
    customer_id: str
    churn_probability: float
    risk_segment: str

# Recommendation Schemas
class RecRequest(BaseModel):
    customer_id: str

class RecItem(BaseModel):
    item_id: str
    title: str
    category: str
    type: str
    description: str
    score: float
    meta: Optional[str] = None

# Campaign Schema
class GenerateCampaignRequest(BaseModel):
    customer_id: str
    risk_segment: str
    churn_probability: float

class CampaignResponse(BaseModel):
    subject_line: str
    email_body: str
    strategy: str

@app.on_event("startup")
def startup_event():
    load_churn_model()

@app.get("/")
def read_root():
    return {"message": "Welcome to GrowthAI API"}

# --- Data Endpoints for UI ---
@app.get("/data/customers")
def get_customers():
    """Returns list of all customer IDs"""
    try:
        return recsys_engine.get_all_customers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/customer/{customer_id}")
def get_customer_details(customer_id: str):
    """Returns details for a specific customer"""
    details = recsys_engine.get_customer_details(customer_id)
    if not details:
        raise HTTPException(status_code=404, detail="Customer not found")
    return details
    
# --- ML / AI Endpoints ---

@app.post("/predict/churn", response_model=ChurnResponse)
def predict_churn(data: ChurnInput, db: Session = Depends(get_db)):
    # Mock prediction if model missing
    if not churn_model:
        return {
            "customer_id": data.customer_id,
            "churn_probability": 0.45,
            "risk_segment": "MEDIUM" # Default fallback
        }
    
    # Build feature vector matching model training schema
    # Model expects: age, recency_days, frequency_total, frequency_30d, avg_order_value,
    #                category_diversity, login_count_14d, country_Canada, country_France,
    #                country_Germany, country_India, country_UK, country_US
    
    countries = ['Canada', 'France', 'Germany', 'India', 'UK', 'US']
    country_features = {f'country_{c}': 1 if data.country == c else 0 for c in countries}
    
    feature_row = {
        'age': data.age,
        'recency_days': data.recency_days,
        'frequency_total': data.frequency_total,
        'frequency_30d': data.frequency_30d,
        'avg_order_value': data.avg_order_value,
        'category_diversity': data.category_diversity,
        'login_count_14d': data.login_count_14d,
        **country_features
    }
    
    # Create DataFrame with correct column order
    feature_cols = ['age', 'recency_days', 'frequency_total', 'frequency_30d', 'avg_order_value',
                    'category_diversity', 'login_count_14d', 'country_Canada', 'country_France',
                    'country_Germany', 'country_India', 'country_UK', 'country_US']
    
    X = pd.DataFrame([feature_row])[feature_cols]
    
    prob = churn_model.predict_proba(X)[0][1]
    
    risk_segment = "LOW"
    if prob > 0.7:
        risk_segment = "HIGH"
    elif prob > 0.4:
        risk_segment = "MEDIUM"
        
    return {
        "customer_id": data.customer_id,
        "churn_probability": float(prob),
        "risk_segment": risk_segment
    }

@app.post("/recommend", response_model=List[RecItem])
def recommend(data: RecRequest):
    """
    Get personalized recommendations based on interaction history.
    """
    recs = recsys_engine.recommend_for_user(data.customer_id, top_k=6)
    return recs

@app.post("/campaign/generate", response_model=CampaignResponse)
async def generate_campaign(data: GenerateCampaignRequest):
    """
    Generates a personalized retention email using Gemini.
    """
    # Create a simple profile text
    # In a real app we would fetch name, past purchases etc. here
    
    # Check if we have customer details in our RecSys engine to augment context
    cust_details = recsys_engine.get_customer_details(data.customer_id)
    cust_name = cust_details.get('name', 'Valued Customer')
    
    # Get recommendations to include in the email
    recs = recsys_engine.recommend_for_user(data.customer_id, top_k=2)
    rec_text = "Recommanded for you: " + ", ".join([r['title'] for r in recs]) if recs else ""
    
    prompt = f"""
    Write a retention email for customer {cust_name}.
    Risk Level: {data.risk_segment} (Churn Prob: {data.churn_probability:.2f}).
    Context: {rec_text}
    Goal: Prevent them from leaving. Offer them something relevant.
    """
    
    return gemini.generate_retention_content(data.risk_segment, prompt)
