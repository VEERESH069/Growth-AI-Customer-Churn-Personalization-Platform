import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib
import mlflow
import mlflow.xgboost
import os

def train_model():
    # Load data
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_path = os.path.join(base_dir, 'data/processed/features.csv')
    data = pd.read_csv(data_path)
    
    # Prepare X and y
    # Drop non-numeric or ID columns
    X = data.drop(columns=['customer_id', 'country', 'churn', 'signup_date'], errors='ignore')
    # Simple encoding for now if needed (country is categorical). 
    # For now I dropped country to keep it simple, but let's encode it for better model.
    if 'country' in data.columns:
        X = pd.concat([X, pd.get_dummies(data['country'], prefix='country')], axis=1)
        
    y = data['churn']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # MLflow tracking
    mlflow.set_experiment("churn_prediction")
    
    with mlflow.start_run():
        # Train XGBoost
        model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        model.fit(X_train, y_train)
        
        # Evaluate
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, preds)
        auc = roc_auc_score(y_test, probs) if len(set(y_test)) > 1 else 0.5
        
        print(f"Accuracy: {acc}")
        print(f"AUC: {auc}")
        
        # Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("auc", auc)
        
        # Log model
        mlflow.xgboost.log_model(model, "model")
        
        # Save locally for API
        model_output_path = os.path.join(base_dir, 'src/models/churn_model.pkl')
        joblib.dump(model, model_output_path)
        print(f"Model saved to {model_output_path}")

if __name__ == "__main__":
    train_model()
