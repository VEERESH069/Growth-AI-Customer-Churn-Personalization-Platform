import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    customers = pd.read_csv(os.path.join(base_dir, 'data/raw/customers.csv'))
    transactions = pd.read_csv(os.path.join(base_dir, 'data/raw/transactions.csv'))
    events = pd.read_csv(os.path.join(base_dir, 'data/raw/events.csv'))
    return customers, transactions, events

def build_features(customers, transactions, events, reference_date_str='2024-07-01'):
    reference_date = pd.to_datetime(reference_date_str)
    
    # Process Transactions
    transactions['order_date'] = pd.to_datetime(transactions['order_date'])
    
    # Recency
    last_purchase = transactions.groupby('customer_id')['order_date'].max().reset_index()
    last_purchase['recency_days'] = (reference_date - last_purchase['order_date']).dt.days
    
    # Frequency (Total orders)
    frequency = transactions.groupby('customer_id')['order_id'].count().reset_index()
    frequency.rename(columns={'order_id': 'frequency_total'}, inplace=True)
    
    # Frequency 30d
    last_30d = reference_date - pd.Timedelta(days=30)
    freq_30d = transactions[transactions['order_date'] >= last_30d].groupby('customer_id')['order_id'].count().reset_index()
    freq_30d.rename(columns={'order_id': 'frequency_30d'}, inplace=True)
    
    # Monetary (Avg Order Value)
    monetary = transactions.groupby('customer_id')['amount'].mean().reset_index()
    monetary.rename(columns={'amount': 'avg_order_value'}, inplace=True)
    
    # Category Diversity
    diversity = transactions.groupby('customer_id')['category'].nunique().reset_index()
    diversity.rename(columns={'category': 'category_diversity'}, inplace=True)
    
    # Process Events
    events['event_date'] = pd.to_datetime(events['event_date'])
    
    # Login count 14d
    last_14d = reference_date - pd.Timedelta(days=14)
    logins = events[(events['event_type'] == 'login') & (events['event_date'] >= last_14d)]
    login_count = logins.groupby('customer_id').size().reset_index(name='login_count_14d')
    
    # Merge Features
    features = customers[['customer_id', 'age', 'country']].copy()
    features = features.merge(last_purchase[['customer_id', 'recency_days']], on='customer_id', how='left')
    features = features.merge(frequency, on='customer_id', how='left')
    features = features.merge(freq_30d, on='customer_id', how='left')
    features = features.merge(monetary, on='customer_id', how='left')
    features = features.merge(diversity, on='customer_id', how='left')
    features = features.merge(login_count, on='customer_id', how='left')
    
    # Fill NaNs
    features['recency_days'] = features['recency_days'].fillna(999) # Never purchased
    features['frequency_total'] = features['frequency_total'].fillna(0)
    features['frequency_30d'] = features['frequency_30d'].fillna(0)
    features['avg_order_value'] = features['avg_order_value'].fillna(0)
    features['category_diversity'] = features['category_diversity'].fillna(0)
    features['login_count_14d'] = features['login_count_14d'].fillna(0)
    
    # Generate Target Label (Churn)
    # Rule-based simulation for the sake of the example:
    # Churn = 1 if recency > 100 days OR (frequency_total < 2 AND recency > 60)
    features['churn'] = 0
    features.loc[features['recency_days'] > 100, 'churn'] = 1
    features.loc[(features['frequency_total'] < 2) & (features['recency_days'] > 60), 'churn'] = 1
    
    return features

if __name__ == "__main__":
    customers, transactions, events = load_data()
    features = build_features(customers, transactions, events)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_path = os.path.join(base_dir, 'data/processed/features.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    features.to_csv(output_path, index=False)
    print(f"Features built and saved to {output_path}")
