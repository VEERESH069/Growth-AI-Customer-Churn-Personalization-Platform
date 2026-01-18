from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    customer_id = Column(String, primary_key=True, index=True)
    age = Column(Integer)
    country = Column(String)
    signup_date = Column(DateTime)
    email = Column(String, nullable=True)  # Mock email for outreach
    
    # ML Computed Fields (Cached for speed)
    churn_probability = Column(Float, nullable=True)
    risk_segment = Column(String, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    transactions = relationship("Transaction", back_populates="customer")
    interactions = relationship("MarketingInteraction", back_populates="customer")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String, unique=True, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    amount = Column(Float)
    category = Column(String)
    order_date = Column(DateTime)
    
    customer = relationship("Customer", back_populates="transactions")

class MarketingInteraction(Base):
    """
    Stores the AI-generated content sent to users. 
    Essential for 'Human-in-the-loop' review and A/B testing AI copy.
    """
    __tablename__ = "marketing_interactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"))
    
    # What the ML model thought (Context)
    risk_level_at_time = Column(String)
    
    # What the GenAI created
    ai_generated_subject = Column(String)
    ai_generated_body = Column(Text)
    ai_explanation_reasoning = Column(Text) # Chain of thought
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="interactions")
