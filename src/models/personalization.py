import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import os
import torch

class PersonalizationEngine:
    def __init__(self):
        print("Initializing Personalization Engine (Industry Grade)...")
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.raw_dir = os.path.join(self.base_dir, 'data', 'raw')
        
        # Load Data
        self.products = pd.read_csv(os.path.join(self.raw_dir, 'products.csv'))
        self.content = pd.read_csv(os.path.join(self.raw_dir, 'content.csv'))
        self.interactions = pd.read_csv(os.path.join(self.raw_dir, 'interactions.csv'))
        # Try enhanced first, fall back to simple
        if os.path.exists(os.path.join(self.raw_dir, 'customers_enhanced.csv')):
             self.customers = pd.read_csv(os.path.join(self.raw_dir, 'customers_enhanced.csv'))
        else:
             self.customers = pd.read_csv(os.path.join(self.raw_dir, 'customers.csv'))

        
        # Prepare Unified Item Repo
        self.items = self._prepare_item_repo()
        
        # Load Model
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("Embedding model loaded successfully.")
            
            # Pre-compute Item Embeddings
            # Combine Title/Name + Category/Genre + Description for rich semantic matching
            self.item_texts = self.items.apply(
                lambda x: f"{x['title']} ({x['category']}): {x['description']}", axis=1
            ).tolist()
            
            self.item_embeddings = self.model.encode(self.item_texts, convert_to_tensor=True)
            print(f"Computed embeddings for {len(self.items)} items.")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def _prepare_item_repo(self):
        """Standardizes Products and Content into a single dataframe"""
        
        # Format Products
        p = self.products.copy()
        p['item_id'] = p['product_id']
        p['type'] = 'Product'
        p['title'] = p['name']
        # category is already there
        # description is there
        p = p[['item_id', 'type', 'title', 'category', 'description', 'price']]
        p['meta'] = p.apply(lambda x: f"Price: ${x['price']}", axis=1)

        # Format Content
        c = self.content.copy()
        c['item_id'] = c['content_id']
        c['type'] = 'Content'
        # title is there
        c['category'] = c['genre'] # Map genre to category
        # description is there
        c = c[['item_id', 'type', 'title', 'category', 'description']]
        c['meta'] = c['type'] # Movie/Article etc
        c['price'] = 0 # Free content
        
        # Combine
        combined = pd.concat([p, c], ignore_index=True)
        return combined

    def get_user_embedding(self, customer_id):
        """
        Creates a 'User Vector' based on everything they've interacted with.
        """
        user_history = self.interactions[self.interactions['customer_id'] == customer_id]
        
        if user_history.empty:
            return None
            
        # Get IDs of items visited
        visited_ids = user_history['item_id'].tolist()
        
        # Find indices in our master item list
        indices = self.items.index[self.items['item_id'].isin(visited_ids)].tolist()
        
        if not indices:
            return None
            
        # Get embeddings
        # We could weight this by action (Purchase > Cart > View), but simple average is fine for now
        history_embeddings = self.item_embeddings[indices]
        
        # Average vector
        user_vector = torch.mean(history_embeddings, dim=0)
        return user_vector

    def recommend_for_user(self, customer_id, top_k=5):
        """
        Hybrid Semantic Search Recommendation.
        Finds items semantically similar to what the user has liked before.
        """
        if self.model is None:
            return []

        user_vector = self.get_user_embedding(customer_id)
        
        if user_vector is None:
            # Cold Start: Recommend Trending/Random high quality items
            # For now, just random top items - but let's diversify
            return self.items.sample(top_k).to_dict('records')
            
        # Semantic Search for nearest neighbors
        cosine_scores = util.cos_sim(user_vector, self.item_embeddings)[0]
        
        # Get top results
        top_results = torch.topk(cosine_scores, k=top_k+20) # Get more to filter
        
        recommendations = []
        user_history_ids = self.interactions[self.interactions['customer_id'] == customer_id]['item_id'].tolist()
        
        for score, idx in zip(top_results.values, top_results.indices):
            idx = int(idx)
            item = self.items.iloc[idx]
            
            # Simple Filter: Don't show what they already saw
            if item['item_id'] not in user_history_ids:
                rec = item.to_dict()
                rec['score'] = float(score)
                recommendations.append(rec)
                
            if len(recommendations) >= top_k:
                break
                
        return recommendations

    def get_all_customers(self):
        return self.customers['customer_id'].tolist()
        
    def get_customer_details(self, customer_id):
         cust = self.customers[self.customers['customer_id'] == customer_id]
         if not cust.empty:
             return cust.iloc[0].to_dict()
         return {}
