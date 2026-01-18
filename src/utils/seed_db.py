import pandas as pd
from src.data.database import SessionLocal, init_db
from src.data.models import Customer, Transaction
from datetime import datetime
import os

def seed_database():
    init_db()
    db = SessionLocal()
    
    # Check if empty
    if db.query(Customer).count() > 0:
        print("Database already seeded.")
        return

    print("Seeding database from CSVs...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    customers_df = pd.read_csv(os.path.join(base_dir, 'data/raw/customers.csv'))
    transactions_df = pd.read_csv(os.path.join(base_dir, 'data/raw/transactions.csv'))

    # Load Customers
    customers = []
    for _, row in customers_df.iterrows():
        customers.append(Customer(
            customer_id=row['customer_id'],
            age=row['age'],
            country=row['country'],
            signup_date=pd.to_datetime(row['signup_date']),
            email=f"{row['customer_id'].lower()}@example.com"
        ))
    db.add_all(customers)
    db.commit()
    print(f"Added {len(customers)} customers.")

    # Load Transactions
    # (Performance: do bulk insert in chunks for real apps, here simple loop is fine for 5k rows)
    transactions = []
    for _, row in transactions_df.iterrows():
        transactions.append(Transaction(
            transaction_id=row['order_id'],
            customer_id=row['customer_id'],
            amount=row['amount'],
            category=row['category'],
            order_date=pd.to_datetime(row['order_date'])
        ))
    db.add_all(transactions)
    db.commit()
    print(f"Added {len(transactions)} transactions.")
    
    db.close()

if __name__ == "__main__":
    seed_database()
