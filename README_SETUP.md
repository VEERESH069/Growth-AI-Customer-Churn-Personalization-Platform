# GrowthAI Customer Churn & Personalization Platform

## 🚀 Setup & Execution Guide

You have successfully installed the dependencies. Now, follow these steps to build the data pipeline, train the model, and launch the API.

### 1. Data Processing (Feature Engineering)
Convert raw data into features for the model.

```bash
cd src/features
python build_features.py
```
*Output:* `data/processed/features.csv`

### 2. Train the Churn Prediction Model
Train the XGBoost classifier and log experiments to MLflow.

```bash
cd ../models
python train_churn_model.py
```
*Output:* `src/models/churn_model.pkl`

### 3. Run the API (Locally)
Start the FastAPI server.

```bash
cd ../..
uvicorn src.api.main:app --reload
```
*Access API:* [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Run with Docker (Production Mode)
Build and run the entire stack (API + MLflow) using Docker Compose.

```bash
docker-compose up --build
```

---

## 🧠 System Architecture

- **Predictive Model**: XGBoost (trained on `features.csv`)
- **Personalization**: SentenceTransformers (Embeddings for semantic matching)
- **API**: FastAPI (serves predictions and recommendations)
- **Tracking**: MLflow (tracks model versions)

## 🧪 Test the API

**Predict Churn:**
POST `/predict/churn`
```json
{
  "customer_id": "C001",
  "recency_days": 45,
  "frequency_30d": 1,
  "avg_order_value": 520,
  "category_diversity": 2,
  "login_count_14d": 3
}
```

**Get Recommendation:**
POST `/recommend`
```json
{
  "customer_id": "C001",
  "risk_segment": "HIGH",
  "preferred_categories": ["Electronics", "Books"]
}
```
