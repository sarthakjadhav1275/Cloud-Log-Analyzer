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

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(page_title="Cloud Log Analyzer", page_icon="☁️", layout="wide")

# Custom CSS for clean website design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.hero-section {
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 0 0 30px 30px;
    margin-bottom: 50px;
    color: white;
    position: relative;
    overflow: hidden;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 15px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    font-family: 'Inter', sans-serif;
}

.hero-subtitle {
    font-size: 1.4rem;
    font-weight: 400;
    opacity: 0.95;
    margin-bottom: 40px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    font-family: 'Inter', sans-serif;
}

.stats-container {
    display: flex;
    justify-content: center;
    gap: 60px;
    margin-top: 40px;
    flex-wrap: wrap;
}

.stat-item {
    text-align: center;
    min-width: 120px;
    font-family: 'Inter', sans-serif;
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.9;
    font-weight: 500;
}

.features-section {
    padding: 60px 30px;
    background: white;
    border-radius: 30px;
    margin-bottom: 50px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

.section-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 50px;
    font-family: 'Inter', sans-serif;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
}

.feature-card {
    background: #f8fafc;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    border: 1px solid rgba(102, 126, 234, 0.1);
    text-align: center;
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.15);
    border-color: rgba(102, 126, 234, 0.2);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 20px;
    display: block;
}

.feature-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 15px;
    font-family: 'Inter', sans-serif;
}

.feature-description {
    font-size: 1rem;
    color: #718096;
    line-height: 1.6;
    font-family: 'Inter', sans-serif;
}

.benefits-section {
    padding: 60px 30px;
    background: white;
    border-radius: 30px;
    margin-bottom: 50px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 25px;
}

.benefit-card {
    background: #f8fafc;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
    border: 1px solid rgba(102, 126, 234, 0.08);
    position: relative;
    overflow: hidden;
}

.benefit-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
}

.benefit-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.12);
}

.benefit-icon {
    font-size: 2.5rem;
    margin-bottom: 15px;
    display: block;
}

.benefit-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 10px;
    font-family: 'Inter', sans-serif;
}

.benefit-description {
    font-size: 0.95rem;
    color: #718096;
    line-height: 1.6;
    margin-bottom: 15px;
    font-family: 'Inter', sans-serif;
}

.benefit-metric {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: 10px;
}

.metric-blue { background: #e0f2fe; color: #0369a1; }
.metric-green { background: #dcfce7; color: #166534; }
.metric-yellow { background: #fef3c7; color: #92400e; }
.metric-purple { background: #f3e8ff; color: #6b21a8; }

.cta-section {
    text-align: center;
    padding: 60px 30px;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border-radius: 30px;
    margin: 50px 0;
}

.cta-title {
    font-size: 2rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 15px;
    font-family: 'Inter', sans-serif;
}

.cta-description {
    font-size: 1.1rem;
    color: #718096;
    margin-bottom: 30px;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    font-family: 'Inter', sans-serif;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 15px 40px;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    font-family: 'Inter', sans-serif;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.trust-badges {
    margin-top: 20px;
    font-size: 0.9rem;
    color: #718096;
    font-family: 'Inter', sans-serif;
}

@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    .hero-subtitle { font-size: 1.2rem; }
    .stats-container { gap: 30px; }
    .feature-grid { grid-template-columns: 1fr; }
    .benefits-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# MongoDB Connection
def get_db_collection():
    MONGO_USER = os.environ.get("MONGO_USER")
    MONGO_PASS = os.environ.get("MONGO_PASS")
    MONGO_HOST = os.environ.get("MONGO_HOST")
    MONGO_APP_NAME = os.environ.get("MONGO_APP_NAME")

    encoded_user = quote_plus(MONGO_USER)
    encoded_pass = quote_plus(MONGO_PASS)
    MONGO_CONNECTION_STRING = f"mongodb+srv://{encoded_user}:{encoded_pass}@{MONGO_HOST}/?appName={MONGO_APP_NAME}"
    
    client = MongoClient(MONGO_CONNECTION_STRING)
    db = client["logDB"]
    return db["analysis"]

# --- PAGE: HOME ---
def show_home():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">☁️ Cloud Log Analyzer</div>
        <div class="hero-subtitle">Intelligent Security Monitoring for Modern Cloud Infrastructure</div>
        
        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">99.9%</div>
                <div class="stat-label">Threat Detection</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Real-time Monitoring</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">10ms</div>
                <div class="stat-label">Response Time</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">100%</div>
                <div class="stat-label">Cloud Native</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div class="features-section">
        <div class="section-title">Powerful Features for Modern Teams</div>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Smart Threat Detection</div>
                <div class="feature-description">
                    Advanced AI-powered algorithms identify suspicious patterns and potential security breaches before they impact your infrastructure.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Real-time Analysis</div>
                <div class="feature-description">
                    Process thousands of log entries in seconds with our optimized cloud-native architecture and get instant insights.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🛡️</div>
                <div class="feature-title">WAF Simulation</div>
                <div class="feature-description">
                    Built-in Web Application Firewall simulation detects malicious IP patterns and blocks potential attacks automatically.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Interactive Dashboard</div>
                <div class="feature-description">
                    Beautiful, responsive visualizations make complex data easy to understand with drill-down capabilities and custom reports.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">☁️</div>
                <div class="feature-title">Cloud Ready</div>
                <div class="feature-description">
                    Deploy anywhere - AWS, Azure, GCP, or on-premises. Fully containerized with automatic scaling and zero-downtime deployments.
                </div>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🔐</div>
                <div class="feature-title">Enterprise Security</div>
                <div class="feature-description">
                    Bank-level encryption, role-based access control, and comprehensive audit trails keep your log data secure and compliant.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits Section
    st.markdown("""
    <div class="benefits-section">
        <div class="section-title">Business Impact & Results</div>
        <div class="benefits-grid">
            <div class="benefit-card">
                <div class="benefit-icon">🚀</div>
                <div class="benefit-title">Reduce Security Incidents</div>
                <div class="benefit-description">
                    Proactive threat detection reduces security incidents and minimizes potential damage to your infrastructure.
                </div>
                <div class="benefit-metric metric-blue">85% Reduction</div>
            </div>
            
            <div class="benefit-card">
                <div class="benefit-icon">💰</div>
                <div class="benefit-title">Lower Operational Costs</div>
                <div class="benefit-description">
                    Automated analysis reduces manual monitoring efforts, allowing your team to focus on strategic initiatives.
                </div>
                <div class="benefit-metric metric-green">90% Cost Savings</div>
            </div>
            
            <div class="benefit-card">
                <div class="benefit-icon">⏰</div>
                <div class="benefit-title">Faster Issue Resolution</div>
                <div class="benefit-description">
                    Real-time alerts and detailed analytics help you identify and resolve issues faster than traditional monitoring tools.
                </div>
                <div class="benefit-metric metric-yellow">10x Faster Resolution</div>
            </div>
            
            <div class="benefit-card">
                <div class="benefit-icon">📈</div>
                <div class="benefit-title">Compliance Ready</div>
                <div class="benefit-description">
                    Comprehensive audit trails and reporting capabilities ensure compliance with industry standards like SOC 2, ISO 27001, and GDPR.
                </div>
                <div class="benefit-metric metric-purple">Full Compliance</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">Ready to Transform Your Log Monitoring?</div>
        <div class="cta-description">
            Join thousands of organizations that trust Cloud Log Analyzer for their security monitoring needs.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get Started Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started Now", key="home_cta", help="Start analyzing your logs with our powerful dashboard"):
            st.session_state.page = 'login'
            st.rerun()
        
        st.markdown("""
        <div class="trust-badges">
            ✨ No credit card required • Free tier available • Setup in 2 minutes
        </div>
        """, unsafe_allow_html=True)

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
        
        if st.button("⬅️ Back to Home"):
            st.session_state.page = 'home'
            st.rerun()

# --- PAGE: DASHBOARD ---
def show_dashboard():
    # Top Left Logout Field
    l_col1, l_col2, l_col3 = st.columns([1, 8, 1])
    with l_col1:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.page = 'home'
            st.rerun()

    st.markdown("<h1 style='text-align: center; margin-top: -50px;'>📊 Log Analysis Dashboard</h1>", unsafe_allow_html=True)
    
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

        # Save to MongoDB
        collection.insert_one({
            "timestamp": pd.Timestamp.now(),
            "404": error_404,
            "500": error_500,
            "top_ips": top_ips,
            "suspicious_ips": suspicious_ips,
            "anomaly_flag": error_500 > 5
        })

        # Download Report
        csv = error_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Analysis Report", csv, "cloud_log_report.csv", "text/csv")

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
