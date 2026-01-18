import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_synthetic_data(num_customers=1000, num_transactions=5000, num_events=10000):
    np.random.seed(42)
    random.seed(42)
    
    print(f"Generating {num_customers} customers...")
    
    # 1. Customers
    customer_ids = [f"C{str(i).zfill(4)}" for i in range(1, num_customers + 1)]
    countries = ['US', 'India', 'UK', 'Canada', 'Germany', 'France', 'Australia', 'Brazil']
    
    customers_data = {
        'customer_id': customer_ids,
        'age': np.random.randint(18, 70, size=num_customers),
        'country': np.random.choice(countries, size=num_customers),
        'signup_date': [
            (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 700))).strftime('%Y-%m-%d')
            for _ in range(num_customers)
        ]
    }
    df_customers = pd.DataFrame(customers_data)
    
    # Assign 'Hidden' Churn Status for simulation consistency
    # (We want the data to actually reflect churn signals)
    # 20% churn rate
    churn_status = np.random.choice([0, 1], size=num_customers, p=[0.8, 0.2])
    
    print(f"Generating {num_transactions} transactions...")
    
    # 2. Transactions
    categories = ['Electronics', 'Books', 'Home', 'Fashion', 'Beauty', 'Sports']
    transactions_list = []
    
    reference_date = datetime(2024, 7, 1)
    
    for idx, cid in enumerate(customer_ids):
        is_churned = churn_status[idx]
        
        # Determine number of transactions for this customer
        # Churners might have fewer overall, or stopped long ago
        if is_churned:
            n_tx = np.random.randint(1, 5)
            # Last transaction was a while ago (60-180 days)
            days_ago_start = 60
            days_ago_end = 180
        else:
            n_tx = np.random.randint(3, 15)
            # Last transaction recent (0-30 days)
            days_ago_start = 0
            days_ago_end = 30
            
        # Generate dates
        last_date = reference_date - timedelta(days=np.random.randint(days_ago_start, days_ago_end + 1))
        
        for _ in range(n_tx):
            # Transactions spread out before the last date
            tx_date = last_date - timedelta(days=np.random.randint(0, 365))
            if tx_date < datetime(2022, 1, 1):
                tx_date = datetime(2022, 1, 1)
                
            amount = round(np.random.uniform(20, 500), 2)
            cat = random.choice(categories)
            
            transactions_list.append({
                'customer_id': cid,
                'order_id': f"O{len(transactions_list)+1000}",
                'amount': amount,
                'category': cat,
                'order_date': tx_date.strftime('%Y-%m-%d')
            })
            
    df_transactions = pd.DataFrame(transactions_list)
    
    print(f"Generating {num_events} events...")
    
    # 3. Events
    event_types = ['login', 'view_product', 'add_to_cart', 'checkout']
    events_list = []
    
    for idx, cid in enumerate(customer_ids):
        is_churned = churn_status[idx]
        
        if is_churned:
            # Churners stopped logging in recently
            n_events = np.random.randint(0, 5)
            # Events overlap with their active transaction period (old)
            days_ago_start = 60
            days_ago_end = 180 
        else:
            # Active users log in often recently
            n_events = np.random.randint(10, 50)
            days_ago_start = 0
            days_ago_end = 30
            
        for _ in range(n_events):
            days_back = np.random.randint(days_ago_start, days_ago_end + 1)
            evt_date = reference_date - timedelta(days=days_back)
            
            evt_type = np.random.choice(event_types, p=[0.5, 0.3, 0.15, 0.05])
            
            events_list.append({
                'customer_id': cid,
                'event_type': evt_type,
                'event_date': evt_date.strftime('%Y-%m-%d')
            })
            
    df_events = pd.DataFrame(events_list)
    
    # Save Files
    os.makedirs('../../data/raw', exist_ok=True)
    df_customers.to_csv('../../data/raw/customers.csv', index=False)
    df_transactions.to_csv('../../data/raw/transactions.csv', index=False)
    df_events.to_csv('../../data/raw/events.csv', index=False)
    
    print(f"Successfully generated:")
    print(f"- {len(df_customers)} Customers")
    print(f"- {len(df_transactions)} Transactions")
    print(f"- {len(df_events)} Events")
    print("Files saved to data/raw/")

if __name__ == "__main__":
    generate_synthetic_data()
