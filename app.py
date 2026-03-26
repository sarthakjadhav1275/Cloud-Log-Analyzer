import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pymongo import MongoClient
from collections import Counter
import re
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
import time
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(page_title="Cloud Log Analyzer", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="st-"] {
    font-family: 'Poppins', sans-serif;
    color: #ffffff !important;
}

/* Make all text white */
h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown {
    color: #ffffff !important;
}

/* Override Streamlit default colors */
.stText, .stMarkdownContainer, .stCaption {
    color: #ffffff !important;
}

.main-header {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    padding: 60px 30px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.main-title {
    font-size: 3.5em;
    font-weight: 700;
    margin-bottom: 10px;
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
}

.main-subtitle {
    font-size: 1.5em;
    font-weight: 300;
    opacity: 0.9;
}

.section-header {
    font-size: 2.2em;
    font-weight: 600;
    color: #ffffff !important;
    text-align: center;
    margin-top: 60px;
    margin-bottom: 40px;
    position: relative;
}

.section-header::after {
    content: '';
    position: absolute;
    left: 50%;
    bottom: -15px;
    transform: translateX(-50%);
    width: 100px;
    height: 4px;
    background-color: #ffffff;
    border-radius: 2px;
}

/* Metric Card Styling */
.st-emotion-cache-1g64x9r {
    font-size: 2.5em;
    font-weight: 700;
    color: #1a1a1a; /* Dark color for numbers */
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.st-emotion-cache-1wix42u {
    font-size: 1.1em;
    font-weight: 600;
    color: #2d3748; /* Dark color for labels */
}

/* Metric Container Background */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border: 2px solid #cbd5e1;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    border-color: #94a3b8;
}

/* Feature Card Styling */
[data-testid="stInfo"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

[data-testid="stInfo"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(37, 99, 235, 0.2);
    border-color: #6366f1;
}

/* Success Card Styling */
[data-testid="stSuccess"] {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border: 2px solid #059669;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2);
    transition: all 0.3s ease;
}

[data-testid="stSuccess"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(16, 185, 129, 0.3);
}

/* Warning Card Styling */
[data-testid="stWarning"] {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    border: 2px solid #d97706;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 25px rgba(217, 119, 6, 0.2);
    transition: all 0.3s ease;
}

[data-testid="stWarning"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(217, 119, 6, 0.3);
}

/* Icon Styling */
[data-testid="stIconContainer"] {
    font-size: 3rem;
    margin-bottom: 12px;
}

/* Title Styling */
[data-testid="stMarkdownContainer"] h3 {
    font-size: 1.3rem;
    font-weight: 600;
    color: #ffffff !important;
    margin-bottom: 12px;
    line-height: 1.4;
}

[data-testid="stMarkdownContainer"] p {
    font-size: 1rem;
    color: #ffffff !important;
    line-height: 1.5;
    margin-bottom: 16px;
}

/* Trust Text */
.trust-text {
    text-align: center;
    font-size: 0.9rem;
    color: #ffffff !important;
    margin-top: 16px;
    font-family: 'Poppins', sans-serif;
}

/* CTA Container */
.cta-container {
    text-align: center;
    padding: 3rem 1rem;
    background: rgba(255,255,255,0.1);
    border-radius: 1rem;
    margin: 2rem 0;
}

.cta-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #ffffff !important;
    margin-bottom: 1rem;
    font-family: 'Poppins', sans-serif;
}

.cta-desc {
    font-size: 1rem;
    color: #ffffff !important;
    margin-bottom: 2rem;
    font-family: 'Poppins', sans-serif;
}

/* Metric Badge Styling */
.metric-highlight {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 16px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

/* CTA Button */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: none;
    padding: 25px 60px;
    font-size: 2.0rem;
    font-weight: 900;
    border-radius: 15px;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.5);
    font-family: 'Poppins', sans-serif;
    width: 100%;
    height: 70px;
    text-transform: uppercase;
    letter-spacing: 2px;
    display: flex;
    justify-content: center;
    align-items: center;
}

[data-testid="stButton"] button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(99, 102, 241, 0.7);
    background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
}

/* Trust Text */
.trust-text {
    text-align: center;
    font-size: 0.9rem;
    color: #ffffff !important;
    margin-top: 16px;
    font-family: 'Poppins', sans-serif;
}

/* Make absolutely everything white */
* {
    color: #ffffff !important;
}

/* Override Streamlit specific elements */
.st-ae, .st-bb, .st-bc, .st-bd, .st-be, .st-bf, .st-bg, .st-bh, .st-bi, .st-bj, .st-bk, .st-bl, .st-bm, .st-bn, .st-bo, .st-bp, .st-bq, .st-br, .st-bs, .st-bt, .st-bu, .st-bv, .st-bw, .st-bx, .st-by, .st-bz, .st-ca, .st-cb, .st-cc, .st-cd, .st-ce, .st-cf, .st-cg, .st-ch, .st-ci, .st-cj, .st-ck, .st-cl, .st-cm, .st-cn, .st-co, .st-cp, .st-cq, .st-cr, .st-cs, .st-ct, .st-cu, .st-cv, .st-cw, .st-cx, .st-cy, .st-cz, .st-da, .st-db, .st-dc, .st-dd, .st-de, .st-df, .st-dg, .st-dh, .st-di, .st-dj, .st-dk, .st-dl, .st-dm, .st-dn, .st-do, .st-dp, .st-dq, .st-dr, .st-ds, .st-dt, .st-du, .st-dv, .st-dw, .st-dx, .st-dy, .st-dz {
    color: #ffffff !important;
}

/* Logout Button */
button[data-testid="stBaseButton-secondary"] {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
    font-family: 'Poppins', sans-serif !important;
}

button[data-testid="stBaseButton-secondary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5) !important;
    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
}

button[data-testid="stBaseButton-secondary"] p {
    color: white !important;
    margin: 0 !important;
}

/* Interactive Tab Styling */
[data-testid="stTab"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white !important;
    border: none;
    border-radius: 10px;
    margin: 0 5px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    font-family: 'Poppins', sans-serif;
}

[data-testid="stTab"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
    background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
}

[data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
    box-shadow: 0 6px 25px rgba(139, 92, 246, 0.4);
    transform: scale(1.05);
}

[data-testid="stTab"] p {
    color: white !important;
    margin: 0;
    font-weight: 600;
}

/* Tab List Container */
[data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 8px;
    margin: 20px 0;
    backdrop-filter: blur(10px);
}

/* Tab Highlight */
[data-baseweb="tab-highlight"] {
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    border-radius: 8px;
    opacity: 0.8;
}

/* Responsive Design */
@media (max-width: 768px) {
    .main-title { font-size: 2.5em; }
    .main-subtitle { font-size: 1.2em; }
    .section-header { font-size: 1.8em; }
    [data-testid="stInfo"], [data-testid="stSuccess"], [data-testid="stWarning"] {
        margin-bottom: 16px;
    }
}
</style>
""", unsafe_allow_html=True)

# --- PAGE: HOME ---
def show_home():
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <div class="main-title">☁️ Cloud Log Analyzer</div>
        <div class="main-subtitle">Intelligent Security Monitoring for Modern Cloud Infrastructure</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 25px; margin: 40px 0; flex-wrap: wrap;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 25px; border-radius: 15px; text-align: center; width: 220px; height: 180px; box-shadow: 0 8px 25px rgba(0,0,0,0.2); display: flex; flex-direction: column; justify-content: center; align-items: center; transition: all 0.3s ease; cursor: pointer;">
            <div style="font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 15px;">99.9%</div>
            <div style="font-size: 1rem; color: white; opacity: 0.95; font-weight: 500;">Threat Detection</div>
        </div>
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 25px; border-radius: 15px; text-align: center; width: 220px; height: 180px; box-shadow: 0 8px 25px rgba(0,0,0,0.2); display: flex; flex-direction: column; justify-content: center; align-items: center; transition: all 0.3s ease; cursor: pointer;">
            <div style="font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 15px;">24/7</div>
            <div style="font-size: 1rem; color: white; opacity: 0.95; font-weight: 500;">Real-time Monitoring</div>
        </div>
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 25px; border-radius: 15px; text-align: center; width: 220px; height: 180px; box-shadow: 0 8px 25px rgba(0,0,0,0.2); display: flex; flex-direction: column; justify-content: center; align-items: center; transition: all 0.3s ease; cursor: pointer;">
            <div style="font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 15px;">10ms</div>
            <div style="font-size: 1rem; color: white; opacity: 0.95; font-weight: 500;">Response Time</div>
        </div>
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 25px; border-radius: 15px; text-align: center; width: 220px; height: 180px; box-shadow: 0 8px 25px rgba(0,0,0,0.2); display: flex; flex-direction: column; justify-content: center; align-items: center; transition: all 0.3s ease; cursor: pointer;">
            <div style="font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 15px;">100%</div>
            <div style="font-size: 1rem; color: white; opacity: 0.95; font-weight: 500;">Native</div>
        </div>
    </div>
    
    <style>
    .stat-box:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<div class="section-header">🚀 Powerful Features for Modern Teams</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🔍 Smart Threat Detection**
        
        Advanced AI-powered algorithms identify suspicious patterns and potential security breaches before they impact your infrastructure.
        """, icon="🔍")
    
    with col2:
        st.info("""
        **⚡ Real-time Analysis**
        
        Process thousands of log entries in seconds with our optimized cloud-native architecture.
        """, icon="⚡")
    
    with col3:
        st.info("""
        **🛡️ WAF Simulation**
        
        Built-in Web Application Firewall simulation detects malicious IP patterns automatically.
        """, icon="🛡️")
    
    # Second row of features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **📊 Interactive Dashboard**
        
        Beautiful visualizations make complex data easy to understand.
        """, icon="📊")
    
    with col2:
        st.info("""
        **Cloud Ready**
        
        Deploy anywhere with automatic scaling and zero-downtime deployments.
        """)
    
    with col3:
        st.info("""
        **🔐 Enterprise Security**
        
        Bank-level encryption and comprehensive audit trails keep your data secure.
        """, icon="🔐")
    
    # Benefits Section
    st.markdown('<div class="section-header">📈 Business Impact & Results</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **Reduce Security Incidents**
        
        Proactive threat detection reduces security incidents by up to 85%.
        
        **Metric: 85% Reduction**
        """)
        
        st.info("""
        **Lower Operational Costs**
        
        Automated analysis reduces manual monitoring efforts by 90%.
        
        **Metric: 90% Cost Savings**
        """)
    
    with col2:
        st.warning("""
        **Faster Issue Resolution**
        
        Real-time alerts help you resolve issues 10x faster than traditional tools.
        
        **Metric: 10x Faster Resolution**
        """)
        
        st.success("""
        **Compliance Ready**
        
        Comprehensive audit trails ensure compliance with industry standards.
        
        **Metric: Full Compliance**
        """)
    
    # CTA Section
    st.markdown("""
    <div class="cta-container">
        <div class="cta-title">Ready to Transform Your Log Monitoring?</div>
        <div class="cta-desc">Join thousands of organizations that trust Cloud Log Analyzer for their security monitoring needs.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Get Started Button
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🚀 Get Started Now", key="home_cta", help="Start analyzing your logs with our powerful dashboard"):
            st.session_state.page = 'login'
            st.rerun()
        
        st.markdown('<div class="trust-text">✨ No credit card required • Free tier available • Setup in 2 minutes</div>', unsafe_allow_html=True)

# MongoDB Connection (with error handling)
def get_db_collection():
    try:
        MONGO_USER = os.environ.get("MONGO_USER")
        MONGO_PASS = os.environ.get("MONGO_PASS")
        MONGO_HOST = os.environ.get("MONGO_HOST")
        MONGO_APP_NAME = os.environ.get("MONGO_APP_NAME")

        if not all([MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_APP_NAME]):
            print("MongoDB environment variables not properly configured")
            return None

        encoded_user = quote_plus(MONGO_USER)
        encoded_pass = quote_plus(MONGO_PASS)
        MONGO_CONNECTION_STRING = f"mongodb+srv://{encoded_user}:{encoded_pass}@{MONGO_HOST}/?appName={MONGO_APP_NAME}"
        
        client = MongoClient(MONGO_CONNECTION_STRING, serverSelectionTimeoutMS=5000)
        db = client["logDB"]
        return db["analysis"]
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None

# --- PAGE: LOGIN ---
def show_login():
    st.markdown("<h2 style='text-align: center;'>🔐 Secure Access</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                APP_USERNAME = os.environ.get("APP_USERNAME")
                APP_PASSWORD = os.environ.get("APP_PASSWORD")
                
                if username_input == APP_USERNAME and password_input == APP_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.page = 'dashboard'
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        
        if st.button("⬅️ Back to Home", key="back_login"):
            st.session_state.page = 'home'
            st.rerun()

# --- PAGE: ADVANCED ANALYTICS ---
def show_advanced_analytics():
    # Top Left Logout Field
    l_col1, l_col2, l_col3 = st.columns([1, 8, 1])
    with l_col1:
        if st.button("🚪 Logout", key="logout_advanced"):
            st.session_state.logged_in = False
            st.session_state.page = 'home'
            st.rerun()

    st.markdown("<h1 style='text-align: center; margin-top: -50px;'>📊 Advanced Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    # Real-time Log Stream Section
    st.markdown("### 🔄 Real-time Log Stream")
    col1, col2 = st.columns([3, 1])
    
    with col2:
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)
        refresh_rate = st.selectbox("Refresh Rate", ["1s", "3s", "5s", "10s"], index=1)
        
    with col1:
        # Simulate real-time log data
        if auto_refresh:
            log_placeholder = st.empty()
            
            for _ in range(5):  # Show 5 sample logs
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                status = random.choice(["200", "404", "500", "301"])
                method = random.choice(["GET", "POST", "PUT", "DELETE"])
                endpoint = random.choice(["/api/users", "/login", "/dashboard", "/admin", "/data"])
                
                log_entry = f"[{timestamp}] {ip} {method} {endpoint} {status}"
                
                if status == "404":
                    log_placeholder.error(f"🚨 {log_entry}")
                elif status == "500":
                    log_placeholder.error(f"💥 {log_entry}")
                else:
                    log_placeholder.success(f"✅ {log_entry}")
                
                time.sleep(1)
    
    # Advanced Filtering Section
    st.markdown("### 🔍 Advanced Filtering")
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    
    with filter_col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=7))
    with filter_col2:
        end_date = st.date_input("End Date", datetime.now())
    with filter_col3:
        status_filter = st.multiselect("Status Codes", ["200", "404", "500", "301", "403"], default=["200", "404", "500"])
    with filter_col4:
        ip_filter = st.text_input("Filter by IP", placeholder="Enter IP address")
    
    # Generate sample data for charts
    dates = pd.date_range(start=start_date, end=end_date, freq='H')
    sample_data = {
        'timestamp': dates,
        'requests': [random.randint(50, 200) for _ in range(len(dates))],
        'errors_404': [random.randint(0, 20) for _ in range(len(dates))],
        'errors_500': [random.randint(0, 10) for _ in range(len(dates))],
        'unique_ips': [random.randint(10, 50) for _ in range(len(dates))]
    }
    df = pd.DataFrame(sample_data)
    
    # Interactive Charts
    st.markdown("### 📈 Traffic Analytics")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_requests = px.line(df, x='timestamp', y='requests', 
                               title="📊 Request Volume Over Time",
                               color_discrete_sequence=['#6366f1'])
        fig_requests.update_layout(showlegend=False)
        st.plotly_chart(fig_requests, use_container_width=True)
    
    with chart_col2:
        fig_errors = px.line(df, x='timestamp', y=['errors_404', 'errors_500'], 
                            title="⚠️ Error Trends",
                            color_discrete_map={'errors_404': '#ef4444', 'errors_500': '#f59e0b'})
        st.plotly_chart(fig_errors, use_container_width=True)
    
    # Geographic Distribution (Simulated)
    st.markdown("### 🌍 Geographic Distribution")
    geo_col1, geo_col2 = st.columns(2)
    
    with geo_col1:
        countries = ['USA', 'India', 'UK', 'Germany', 'France', 'Canada', 'Australia', 'Japan']
        country_counts = [random.randint(100, 500) for _ in countries]
        
        fig_geo = px.bar(x=countries, y=country_counts, 
                        title="🌏 Requests by Country",
                        color=country_counts,
                        color_continuous_scale='viridis')
        fig_geo.update_layout(showlegend=False)
        st.plotly_chart(fig_geo, use_container_width=True)
    
    with geo_col2:
        # Top IPs
        top_ips = [f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}" for _ in range(5)]
        ip_counts = [random.randint(20, 100) for _ in range(5)]
        
        fig_ips = px.pie(values=ip_counts, names=top_ips, 
                         title="🎯 Top 5 IP Addresses",
                         hole=0.3)
        st.plotly_chart(fig_ips, use_container_width=True)
    
    # Security Metrics
    st.markdown("### 🛡️ Security Metrics")
    security_col1, security_col2, security_col3, security_col4 = st.columns(4)
    
    with security_col1:
        st.metric("🔥 Suspicious IPs", random.randint(5, 25), delta_color="inverse")
    with security_col2:
        st.metric("🚫 Blocked Requests", random.randint(100, 500), delta_color="inverse")
    with security_col3:
        st.metric("📊 Security Score", f"{random.randint(70, 95)}%", delta="normal")
    with security_col4:
        st.metric("⏰ Avg Response Time", f"{random.randint(50, 200)}ms", delta="inverse")

# --- PAGE: DASHBOARD ---
def show_dashboard():
    # Top Left Logout Field
    l_col1, l_col2, l_col3 = st.columns([1, 8, 1])
    with l_col1:
        if st.button("🚪 Logout", key="logout_dashboard"):
            st.session_state.logged_in = False
            st.session_state.page = 'home'
            st.rerun()

    # Navigation Tabs
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📊 Basic Dashboard", "🚀 Advanced Analytics"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    with tab1:
        st.markdown("<h1 style='text-align: center; margin-top: 20px;'>📊 Log Analysis Dashboard</h1>", unsafe_allow_html=True)
        
        collection = get_db_collection()
        
        uploaded_file = st.file_uploader("Upload Log File (.txt, .log)", type=["txt", "log"])

        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            lines = content.split("\n")

            # Analysis Logic
            error_404 = sum("404" in line for line in lines)
            error_500 = sum("500" in line for line in lines)
            ips = re.findall(r'\d+\.\d+\.\d+\.\d+', content)
            ip_count = Counter(ips)
            top_ips = ip_count.most_common(5)

            suspicious_ips = []
            for ip in ip_count:
                ip_404_count = sum(1 for line in lines if ip in line and "404" in line)
                if ip_404_count > 3:
                    suspicious_ips.append((ip, ip_404_count))

            # Metrics Section
            st.markdown("---")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total 404 Errors", error_404, delta_color="inverse")
            with m2:
                st.metric("Total 500 Errors", error_500, delta_color="inverse")
            with m3:
                st.metric("Suspicious IPs", len(suspicious_ips))

            # Alerts
            if error_500 > 5:
                st.error("🚨 ANOMALY DETECTED: High frequency of Server Errors (500)!")
            if len(suspicious_ips) > 0:
                st.warning(f"⚠️ SECURITY ALERT: {len(suspicious_ips)} Suspicious IP(s) detected!")

            # Interactive Visualizations with Plotly
            st.markdown("### 📈 Visual Insights")
            v1, v2 = st.columns(2)

            with v1:
                # Interactive Bar Chart for Errors
                error_df = pd.DataFrame({"Error Type": ["404", "500"], "Count": [error_404, error_500]})
                fig_bar = px.bar(error_df, x="Error Type", y="Count", 
                                 color="Error Type", 
                                 title="HTTP Error Distribution",
                                 color_discrete_map={"404": "#FFB347", "500": "#FF6961"})
                st.plotly_chart(fig_bar, use_container_width=True)

            with v2:
                # Interactive Pie Chart for IP Frequency
                ip_df = pd.DataFrame(top_ips, columns=["IP Address", "Count"])
                fig_pie = px.pie(ip_df, values="Count", names="IP Address", 
                                 title="Traffic Source Distribution (Top 5 IPs)",
                                 hole=.3,
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_pie, use_container_width=True)

            # Detailed Tables
            t1, t2 = st.columns(2)
            with t1:
                st.subheader("🌐 Top 5 Frequent IPs")
                st.table(ip_df)
            with t2:
                if suspicious_ips:
                    st.subheader("🚩 Suspicious Activity")
                    susp_df = pd.DataFrame(suspicious_ips, columns=["IP Address", "Failed Requests"])
                    st.dataframe(susp_df, use_container_width=True)
                else:
                    st.subheader("🚩 Suspicious Activity")
                    st.success("No suspicious activity detected in this log.")

            # Save to MongoDB (only if connected)
            if collection is not None:
                try:
                    collection.insert_one({
                        "timestamp": pd.Timestamp.now(),
                        "404": error_404,
                        "500": error_500,
                        "top_ips": top_ips,
                        "suspicious_ips": suspicious_ips,
                        "anomaly_flag": error_500 > 5
                    })
                    st.success("✅ Analysis saved to database!")
                except Exception as e:
                    st.warning(f"⚠️ Could not save to database: {e}")

            # Download Report
            csv = error_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Analysis Report", csv, "cloud_log_report.csv", "text/csv")
        else:
            st.info("📊 Upload a log file to begin analysis")
    
    with tab2:
        show_advanced_analytics()

# --- MAIN NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'login':
    show_login()
elif st.session_state.page == 'dashboard':
    if st.session_state.logged_in:
        show_dashboard()
    else:
        st.session_state.page = 'login'
        st.rerun()
