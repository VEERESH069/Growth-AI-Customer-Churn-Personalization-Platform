import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_industry_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    
    np.random.seed(42)
    random.seed(42)
    
    print("Generating industry-grade data...")

    # ==========================
    # 1. CUSTOMERS (45)
    # ==========================
    num_customers = 45
    customer_ids = [f"C{str(i).zfill(3)}" for i in range(1, num_customers + 1)]
    countries = ['US', 'India', 'UK', 'Canada', 'Germany', 'Japan']
    segments = ['Budget', 'Premium', 'Tech-Savvy', 'Casual']
    
    customers_data = []
    for cid in customer_ids:
        customers_data.append({
            'customer_id': cid,
            'name': f"User_{cid}",
            'age': np.random.randint(18, 65),
            'country': np.random.choice(countries),
            'segment': np.random.choice(segments, p=[0.3, 0.2, 0.3, 0.2]),
            'signup_date': (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 500))).strftime('%Y-%m-%d')
        })
    df_customers = pd.DataFrame(customers_data)
    df_customers.to_csv(os.path.join(raw_dir, 'customers_enhanced.csv'), index=False)
    print(f"Generated {len(df_customers)} customers.")

    # ==========================
    # 2. PRODUCTS (120 - Physical Items)
    # ==========================
    product_categories = {
        'Electronics': ['Wireless Earbuds', 'Smart Watch', '4K Monitor', 'Gaming Mouse', 'Mechanical Keyboard', 'Drone', 'VR Headset'],
        'Fashion': ['Running Shoes', 'Denim Jacket', 'Smart Backpack', 'Designer Sunglasses', 'Winter Coat'],
        'Home': ['Smart Bulb', 'Robot Vacuum', 'Air Purifier', 'Coffee Maker', 'Standing Desk'],
        'Entertainment': ['Gaming Console', 'Portable Projector', 'Bluetooth Speaker', 'Vinyl Player']
    }
    
    products_data = []
    for i in range(1, 121):
        cat = random.choice(list(product_categories.keys()))
        item_base = random.choice(product_categories[cat])
        adjectives = ['Pro', 'Ultra', 'Lite', 'Max', 'Series X', '2025 Edition', 'Eco']
        
        products_data.append({
            'product_id': f"P{str(i).zfill(3)}",
            'name': f"{item_base} {random.choice(adjectives)}",
            'category': cat,
            'price': round(random.uniform(20, 1500), 2),
            'description': f"High quality {item_base.lower()} suitable for {cat.lower()} enthusiasts. Features state-of-the-art technology."
        })
        
    df_products = pd.DataFrame(products_data)
    df_products.to_csv(os.path.join(raw_dir, 'products.csv'), index=False)
    print(f"Generated {len(df_products)} products.")

    # ==========================
    # 3. CONTENT (200 - Digital Media)
    # ==========================
    content_genres = ['Action', 'Sci-Fi', 'Documentary', 'Comedy', 'Drama', 'Tech Review']
    content_types = ['Movie', 'c', 'Article', 'Podcast']
    
    content_data = []
    for i in range(1, 201):
        genre = random.choice(content_genres)
        ctype = random.choice(content_types)
        
        titles = {
            'Action': ['The Last Stand', 'Crypto Heist', 'Speed Run', 'Battlefield Earth'],
            'Sci-Fi': ['Mars Colony', 'AI Uprising', 'Cyber Soul', 'Star Warp'],
            'Documentary': ['Nature Unbound', 'History of Tech', 'Deep Ocean', 'Space Race'],
            'Comedy': ['Office Pranks', 'Standup Special', 'Funny Fails', 'Sitcom Life'],
            'Drama': ['The CEO', 'Family Secrets', 'Courtroom Justice', 'Medical Ward'],
            'Tech Review': ['Latest GPU Test', 'Smartphone War', 'Coding 101', 'Future of AI']
        }
        
        title_base = random.choice(titles[genre])
        
        content_data.append({
            'content_id': f"CT{str(i).zfill(3)}",
            'title': f"{title_base} - {random.randint(1, 99)}",
            'genre': genre,
            'type': ctype,
            'description': f"A engaging {genre.lower()} {ctype.lower()} about {title_base}."
        })
        
    df_content = pd.DataFrame(content_data)
    df_content.to_csv(os.path.join(raw_dir, 'content.csv'), index=False)
    print(f"Generated {len(df_content)} content items.")

    # ==========================
    # 4. INTERACTIONS (History)
    # ==========================
    interactions = []
    
    for cid in customer_ids:
        num_actions = random.randint(5, 25)
        
        for _ in range(num_actions):
            if random.random() > 0.4:
                item = df_content.sample(1).iloc[0]
                interactions.append({
                    'customer_id': cid,
                    'item_id': item['content_id'],
                    'item_type': 'content',
                    'title_or_name': item['title'],
                    'category': item['genre'],
                    'action': random.choice(['view', 'like', 'watch_later']),
                    'timestamp': (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d')
                })
            else:
                item = df_products.sample(1).iloc[0]
                interactions.append({
                    'customer_id': cid,
                    'item_id': item['product_id'],
                    'item_type': 'product',
                    'title_or_name': item['name'],
                    'category': item['category'],
                    'action': random.choice(['view', 'cart', 'purchase']),
                    'timestamp': (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d')
                })

    df_interactions = pd.DataFrame(interactions)
    df_interactions.to_csv(os.path.join(raw_dir, 'interactions.csv'), index=False)
    print(f"Generated {len(df_interactions)} interactions.")
    
    # Legacy files update for consistency
    purchases = df_interactions[df_interactions['action'] == 'purchase'].copy()
    if not purchases.empty:
        # Map back to legacy transaction columns implicitly
        # Just create dummy cols to satisfy constraints if needed, but for now just dump basic info
        purchases['order_id'] = range(1000, 1000 + len(purchases))
        purchases['amount'] = 50.0 # Placeholder
        purchases.rename(columns={'timestamp': 'order_date'}, inplace=True)
        purchases[['customer_id', 'order_id', 'amount', 'order_date']].to_csv(os.path.join(raw_dir, 'transactions.csv'), index=False)

    events = df_interactions.copy()
    events.rename(columns={'action': 'event_type', 'timestamp': 'event_date'}, inplace=True)
    events[['customer_id', 'event_type', 'event_date']].to_csv(os.path.join(raw_dir, 'events.csv'), index=False)

if __name__ == "__main__":
    generate_industry_data()
