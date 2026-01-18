import streamlit as st
import requests
import pandas as pd
import numpy as np
import os

# API Configuration - Use env var for Docker, fallback to localhost
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="GrowthAI Platform", page_icon="🚀", layout="wide")

# Initialize session state
if 'churn_result' not in st.session_state:
    st.session_state.churn_result = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'campaign' not in st.session_state:
    st.session_state.campaign = None
if 'input_data' not in st.session_state:
    st.session_state.input_data = None

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .high-risk { background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%) !important; }
    .medium-risk { background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%) !important; }
    .low-risk { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important; }
    
    .rec-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .product-badge { background-color: #4CAF50; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
    .content-badge { background-color: #2196F3; color: white; padding: 3px 10px; border-radius: 12px; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 GrowthAI: Customer Retention & Personalization")
st.caption("AI-Powered Churn Prediction • Personalized Recommendations • Retention Campaigns")

# Sidebar
st.sidebar.header("🎯 Customer Selection")

@st.cache_data(ttl=60)
def get_customer_list():
    try:
        response = requests.get(f"{API_URL}/data/customers", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

customers = get_customer_list()

if not customers:
    st.error("⚠️ Cannot connect to Backend API. Please ensure the API is running:")
    st.code("uvicorn src.api.main:app --reload --port 8000", language="bash")
    st.stop()

selected_customer = st.sidebar.selectbox("Select Customer", customers, key="customer_select")

# Fetch customer details
details = {"name": "Unknown", "segment": "Unknown", "country": "US", "age": 30}
if selected_customer:
    try:
        resp = requests.get(f"{API_URL}/data/customer/{selected_customer}", timeout=5)
        if resp.status_code == 200:
            details = resp.json()
    except:
        pass

st.sidebar.markdown("---")
st.sidebar.markdown(f"**👤 Name:** {details.get('name', 'N/A')}")
st.sidebar.markdown(f"**📊 Segment:** {details.get('segment', 'N/A')}")
st.sidebar.markdown(f"**🌍 Country:** {details.get('country', 'N/A')}")
st.sidebar.markdown(f"**🎂 Age:** {details.get('age', 'N/A')}")

# Main content with tabs
tab1, tab2, tab3 = st.tabs(["📊 Churn Analysis", "🎯 Recommendations", "✉️ Campaign Generator"])

# =====================
# TAB 1: CHURN ANALYSIS
# =====================
with tab1:
    st.header("Customer Churn Risk Analysis")
    st.markdown("Analyze the likelihood of this customer leaving using our XGBoost ML model.")
    
    col_btn, col_info = st.columns([1, 3])
    
    with col_btn:
        analyze_btn = st.button("🔍 Analyze Churn Risk", type="primary", use_container_width=True)
    
    with col_info:
        st.info("Click to run real-time ML inference on customer behavior data")
    
    if analyze_btn:
        # Generate behavioral features (in production, fetch from feature store)
        st.session_state.input_data = {
            "customer_id": selected_customer,
            "age": int(details.get('age', 30)),
            "recency_days": int(np.random.randint(1, 90)),
            "frequency_total": int(np.random.randint(5, 50)),
            "frequency_30d": int(np.random.randint(1, 10)),
            "avg_order_value": float(np.random.uniform(20, 200)),
            "category_diversity": int(np.random.randint(1, 5)),
            "login_count_14d": int(np.random.randint(0, 20)),
            "country": details.get('country', "US")
        }
        
        with st.spinner("Running XGBoost inference..."):
            try:
                resp = requests.post(f"{API_URL}/predict/churn", json=st.session_state.input_data, timeout=10)
                if resp.status_code == 200:
                    st.session_state.churn_result = resp.json()
                else:
                    st.error(f"API Error: {resp.status_code} - {resp.text}")
            except Exception as e:
                st.error(f"Prediction failed: {e}")
    
    # Display results (persists after button click)
    if st.session_state.churn_result:
        st.markdown("---")
        st.subheader("📈 Analysis Results")
        
        res = st.session_state.churn_result
        churn_prob = res['churn_probability']
        risk_level = res['risk_segment']
        
        color_class = "low-risk"
        if risk_level == "HIGH": color_class = "high-risk"
        elif risk_level == "MEDIUM": color_class = "medium-risk"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card {color_class}">
                <h4>Risk Level</h4>
                <h1>{risk_level}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Churn Probability", f"{churn_prob:.1%}")
        
        with col3:
            if st.session_state.input_data:
                st.metric("Avg Order Value", f"${st.session_state.input_data['avg_order_value']:.2f}")
        
        # Feature breakdown
        st.markdown("---")
        st.subheader("🔬 Feature Analysis")
        if st.session_state.input_data:
            feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
            with feat_col1:
                st.metric("Days Since Last Order", st.session_state.input_data['recency_days'])
            with feat_col2:
                st.metric("Orders (30 days)", st.session_state.input_data['frequency_30d'])
            with feat_col3:
                st.metric("Category Diversity", st.session_state.input_data['category_diversity'])
            with feat_col4:
                st.metric("Logins (14 days)", st.session_state.input_data['login_count_14d'])

# =======================
# TAB 2: RECOMMENDATIONS
# =======================
with tab2:
    st.header("Personalized Recommendations")
    st.markdown("Get AI-powered product and content recommendations based on customer history using semantic search.")
    
    rec_btn = st.button("🎯 Generate Recommendations", type="primary", use_container_width=False)
    
    if rec_btn:
        with st.spinner("Running hybrid semantic search..."):
            try:
                resp = requests.post(f"{API_URL}/recommend", json={"customer_id": selected_customer}, timeout=20)
                if resp.status_code == 200:
                    st.session_state.recommendations = resp.json()
                else:
                    st.error(f"API Error: {resp.status_code}")
            except Exception as e:
                st.error(f"Recommendation failed: {e}")
    
    # Display recommendations
    if st.session_state.recommendations:
        st.markdown("---")
        st.subheader(f"🎁 Top Picks for {details.get('name', selected_customer)}")
        
        recs = st.session_state.recommendations
        
        if not recs:
            st.warning("No recommendations found.")
        else:
            cols = st.columns(3)
            for i, item in enumerate(recs):
                with cols[i % 3]:
                    item_type = item.get('type', 'Item')
                    badge_class = "product-badge" if item_type == "Product" else "content-badge"
                    
                    st.markdown(f"""
                    <div class="rec-card">
                        <span class="{badge_class}">{item_type}</span>
                        <h4 style="margin-top: 10px;">{item.get('title', 'Unknown')}</h4>
                        <p style="color: #666; font-size: 14px;">{item.get('category', 'N/A')}</p>
                        <p style="font-size: 13px;">{item.get('description', '')[:80]}...</p>
                        <p style="color: #4CAF50; font-weight: bold;">Match Score: {item.get('score', 0):.2%}</p>
                    </div>
                    """, unsafe_allow_html=True)

# =======================
# TAB 3: CAMPAIGN GENERATOR
# =======================
with tab3:
    st.header("AI Campaign Generator")
    st.markdown("Generate personalized retention emails using Google Gemini AI.")
    
    if st.session_state.churn_result is None:
        st.warning("⚠️ Please run Churn Analysis first (Tab 1) to unlock this feature.")
    else:
        st.success(f"✅ Customer {selected_customer} identified as **{st.session_state.churn_result['risk_segment']}** risk")
        
        campaign_btn = st.button("✨ Generate Retention Email", type="primary")
        
        if campaign_btn:
            with st.spinner("Gemini is crafting your email..."):
                payload = {
                    "customer_id": selected_customer,
                    "risk_segment": st.session_state.churn_result['risk_segment'],
                    "churn_probability": st.session_state.churn_result['churn_probability']
                }
                try:
                    resp = requests.post(f"{API_URL}/campaign/generate", json=payload, timeout=30)
                    if resp.status_code == 200:
                        st.session_state.campaign = resp.json()
                    else:
                        st.error(f"API Error: {resp.status_code} - {resp.text}")
                except Exception as e:
                    st.error(f"Campaign generation failed: {e}")
        
        if st.session_state.campaign:
            st.markdown("---")
            camp = st.session_state.campaign
            
            st.subheader("📧 Generated Email")
            st.text_input("Subject Line", value=camp.get('subject_line', ''), key="email_subject")
            st.text_area("Email Body", value=camp.get('email_body', ''), height=250, key="email_body")
            
            st.markdown("---")
            st.info(f"**📋 Strategy:** {camp.get('strategy', 'N/A')}")
            
            col_copy, col_send = st.columns(2)
            with col_copy:
                st.button("📋 Copy to Clipboard", use_container_width=True)
            with col_send:
                st.button("📤 Send via Email", use_container_width=True, disabled=True)

# Footer
st.markdown("---")
st.caption("GrowthAI Platform v1.0 | Powered by XGBoost, SentenceTransformers & Google Gemini")
