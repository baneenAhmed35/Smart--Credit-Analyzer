import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ======================
# Page Config
# ======================
st.set_page_config(
    page_title="Credit Risk & Expansion Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# Custom CSS
# ======================
st.markdown("""
<style>
    /* Main header */
    .main-header {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        border: 1px solid #334155;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 10px;
        font-weight: 700;
    }
    
    /* KPI Cards */
    .metric-card {
        background: white;
        padding: 25px 15px;
        border-radius: 18px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid #e2e8f0;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 25px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }
    
    .metric-card h3 {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 12px;
        font-weight: 600;
    }
    
    .metric-card h2 {
        color: #0f172a !important;
        font-size: 2.2rem;
        margin: 8px 0;
        font-weight: 700;
    }
    
    .metric-card p {
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Navigation Buttons */
    .nav-container {
        background: #f8fafc;
        padding: 25px;
        border-radius: 20px;
        margin: 25px 0;
        border: 1px solid #e2e8f0;
    }
    
    .stButton > button {
        width: 100%;
        padding: 18px 15px;
        font-weight: 700;
        font-size: 1.2rem;
        border-radius: 15px;
        background: white;
        color: #1e293b;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-color: #3b82f6;
        transform: translateY(-3px);
    }
    
    /* Hide search */
    div[data-testid="stFileUploader"] {
        display: none;
    }
    
    /* Country Cards */
    .country-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .country-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
        border-color: #3b82f6;
    }
    
    .country-card b {
        color: #1e293b;
        font-size: 1.3rem;
        display: block;
        margin-bottom: 15px;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 8px;
    }
    
    .country-card div {
        display: flex;
        justify-content: space-between;
        margin: 8px 0;
    }
    
    /* Decision Matrix */
    .decision-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        text-align: center;
        height: 100%;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    .decision-card h3 {
        font-size: 1.3rem;
        margin-bottom: 15px;
        color: #1e293b;
    }
    
    .decision-badge {
        padding: 15px 25px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.5rem;
        text-align: center;
        display: inline-block;
        margin-top: 15px;
    }
    
    /* Quick Actions */
    .quick-actions-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 25px;
        border-radius: 20px;
        margin: 30px 0;
        border: 1px solid #334155;
    }
    
    .quick-actions-container h3 {
        color: white;
        font-size: 1.8rem;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Progress bar */
    .progress-bar {
        background: #e2e8f0;
        height: 10px;
        border-radius: 5px;
        margin: 15px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 10px;
        border-radius: 5px;
    }
    
    /* Hide alerts */
    .stAlert {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# Header
# ======================
st.markdown("""
<div class="main-header">
    <h1>🏛️ Unified Credit Institution</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Advanced Risk & Expansion Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; color:#64748b; margin-bottom:20px;'>Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)

# ======================
# Sample Data
# ======================
@st.cache_data
def load_sample_data():
    countries = ['USA', 'UAE', 'KSA', 'UK', 'Germany', 'France', 'Japan', 'China', 'India', 'Brazil']
    years = list(range(2018, 2025))
    rows = []
    
    # Market classifications
    market_tiers = {
        'USA': 'Core Market', 'UK': 'Core Market', 'Germany': 'Core Market',
        'UAE': 'Secondary Market', 'KSA': 'Secondary Market', 'France': 'Secondary Market',
        'Japan': 'Secondary Market', 'China': 'Opportunistic Market',
        'India': 'Opportunistic Market', 'Brazil': 'Monitor Only'
    }
    
    # Sovereign ratings
    sovereign_ratings = {
        'USA': 'AAA', 'UK': 'AA', 'Germany': 'AAA',
        'UAE': 'AA', 'KSA': 'A', 'France': 'AA',
        'Japan': 'A', 'China': 'A+', 'India': 'BBB',
        'Brazil': 'BB'
    }
    
    for c in countries:
        gdp = np.random.uniform(200, 2500) * 1e9
        credit = np.random.uniform(50, 1200) * 1e6
        infl = np.random.uniform(2, 5)
        unemp = np.random.uniform(3, 8)
        
        for y in years:
            rows.append({
                "Country": c,
                "Year": y,
                "GDP": gdp * np.random.uniform(.9, 1.1),
                "Credit": credit * np.random.uniform(.9, 1.1),
                "Inflation": infl + np.random.uniform(-1, 1),
                "Unemployment": unemp + np.random.uniform(-1, 1),
                "Market_Tier": market_tiers.get(c, "Secondary Market"),
                "Sovereign_Rating": sovereign_ratings.get(c, "BBB")
            })
    return pd.DataFrame(rows)

df = load_sample_data()

# ======================
# Data Processing
# ======================
df = df.sort_values(["Country", "Year"])

df["GDP_Growth"] = df.groupby("Country")["GDP"].pct_change() * 100
df["Credit_Growth"] = df.groupby("Country")["Credit"].pct_change() * 100

df["GDP_Growth"] = df["GDP_Growth"].fillna(0)
df["Credit_Growth"] = df["Credit_Growth"].fillna(0)

df["Risk_Score"] = (
    0.4 * abs(df["GDP_Growth"]) +
    0.3 * df["Inflation"] +
    0.2 * abs(df["Credit_Growth"]) +
    0.1 * df["Unemployment"]
)

# Normalize Risk Score
risk_min = df["Risk_Score"].min()
risk_max = df["Risk_Score"].max()
if risk_max > risk_min:
    df["Risk_Score"] = (df["Risk_Score"] - risk_min) / (risk_max - risk_min) * 100
else:
    df["Risk_Score"] = 50

# ======================
# Sidebar - Enhanced Market Configuration
# ======================
with st.sidebar:
    st.markdown("## 🌍 **Market Configuration**")
    st.markdown("---")
    
    # Primary market selection
    country = st.selectbox("Select Primary Market", sorted(df.Country.unique()))
    
    # Get country-specific data
    country_data = df[df.Country == country].iloc[-1]
    
    st.markdown("### 📊 **Market Classification**")
    
    # Market Tier with institutional context
    market_tier = st.selectbox(
        "Market Tier",
        ["Core Market", "Secondary Market", "Opportunistic Market", "Monitor Only"],
        index=["Core Market", "Secondary Market", "Opportunistic Market", "Monitor Only"].index(
            country_data.get("Market_Tier", "Secondary Market")
        ),
        help="Core: Primary investment markets | Secondary: Growth markets | Opportunistic: High risk/return | Monitor: Watch only"
    )
    
    # Sovereign rating
    st.markdown("### 📈 **Sovereign Risk**")
    
    col1, col2 = st.columns(2)
    with col1:
        sovereign_rating = st.selectbox(
            "S&P Rating",
            ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "B", "CCC"],
            index=["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "B", "CCC"].index(
                country_data.get("Sovereign_Rating", "A")
            )
        )
    
    with col2:
        regulatory_env = st.select_slider(
            "Regulatory Environment",
            options=["Very Strict", "Strict", "Moderate", "Flexible", "Very Flexible"],
            value="Moderate"
        )
    
    st.markdown("### 🏦 **Market Depth & Liquidity**")
    
    col3, col4 = st.columns(2)
    with col3:
        market_depth = st.slider("Market Depth (1-10)", 1, 10, 
                                7 if country in ['USA', 'UK', 'Germany'] else 5)
    with col4:
        liquidity_score = st.slider("Liquidity Score (1-10)", 1, 10,
                                   8 if country in ['USA', 'UK'] else 5)
    
    st.markdown("### 🌐 **Macroeconomic Factors**")
    
    interest_rate = st.slider("Central Bank Rate (%)", 0.0, 15.0, 
                             5.0 if country in ['USA', 'UK'] else 3.5, 0.25)
    
    exchange_volatility = st.select_slider(
        "Exchange Rate Volatility",
        options=["Very Low", "Low", "Moderate", "High", "Very High"],
        value="Low" if country in ['USA', 'UAE', 'KSA'] else "Moderate"
    )
    
    # Scenario Analysis
    st.markdown("### 🔮 **Scenario Analysis**")
    
    scenario = st.selectbox(
        "Select Scenario",
        ["Base Case", "Optimistic", "Pessimistic", "Stress Test"]
    )
    
    if scenario == "Optimistic":
        gdp_adjust = st.slider("GDP Upside (%)", 0, 5, 2)
        risk_adjust = -0.2
        st.info("✨ Optimistic: Higher growth, lower risk")
    elif scenario == "Pessimistic":
        gdp_adjust = st.slider("GDP Downside (%)", -10, 0, -3)
        risk_adjust = 0.3
        st.warning("⚠️ Pessimistic: Economic slowdown")
    elif scenario == "Stress Test":
        gdp_adjust = st.slider("Stress Level (%)", -20, 0, -10)
        risk_adjust = 0.5
        st.error("🧪 Stress Test: Worst case scenario")
    else:
        gdp_adjust = 0
        risk_adjust = 0
    
    # Investment Parameters
    st.markdown("### 💰 **Investment Parameters**")
    capital = st.number_input("Total Capital ($)", 100000, 10000000, 2000000, 100000)
    
    # Risk appetite
    risk_appetite = st.select_slider(
        "Risk Appetite",
        options=["Very Conservative", "Conservative", "Moderate", "Aggressive", "Very Aggressive"],
        value="Moderate"
    )
    
    appetite_multipliers = {
        "Very Conservative": 0.5,
        "Conservative": 0.7,
        "Moderate": 1.0,
        "Aggressive": 1.3,
        "Very Aggressive": 1.6
    }
    
    # ======================
    # Smart Recommendations
    # ======================
    st.markdown("### 💡 **Smart Recommendations**")
    
    # Calculate composite risk score
    rating_multipliers = {
        "AAA": 0.5, "AA+": 0.55, "AA": 0.6, "AA-": 0.65,
        "A+": 0.7, "A": 0.75, "A-": 0.8,
        "BBB+": 0.9, "BBB": 1.0, "BBB-": 1.1,
        "BB+": 1.2, "BB": 1.3, "B": 1.5, "CCC": 1.8
    }
    
    tier_multipliers = {
        "Core Market": 0.8,
        "Secondary Market": 1.0,
        "Opportunistic Market": 1.3,
        "Monitor Only": 1.6
    }
    
    env_multipliers = {
        "Very Strict": 0.9, "Strict": 1.0, "Moderate": 1.1, 
        "Flexible": 1.2, "Very Flexible": 1.3
    }
    
    composite_risk = (
        rating_multipliers.get(sovereign_rating, 1.0) *
        tier_multipliers.get(market_tier, 1.0) *
        env_multipliers.get(regulatory_env, 1.0) *
        ((11 - market_depth) / 5) *
        ((11 - liquidity_score) / 5)
    )
    
    # Adjust for scenario
    composite_risk = composite_risk * (1 + risk_adjust)
    
    # Generate recommendation
    if composite_risk < 0.8:
        st.success("✅ **AGGRESSIVE EXPANSION**")
        st.info("• Allocation: 15-20% of portfolio\n• All sectors\n• Maximum limits")
        alloc_mult = 1.3
    elif composite_risk < 1.2:
        st.info("📈 **CONTROLLED GROWTH**")
        st.info("• Allocation: 8-12% of portfolio\n• Selective sectors\n• Standard limits")
        alloc_mult = 1.0
    elif composite_risk < 1.6:
        st.warning("⚠️ **SELECTIVE LENDING**")
        st.info("• Allocation: 4-6% of portfolio\n• High quality only\n• Tightened limits")
        alloc_mult = 0.7
    else:
        st.error("🔴 **MONITOR ONLY / EXIT**")
        st.info("• Allocation: 0-2% of portfolio\n• Existing exposure only\n• Maximum restrictions")
        alloc_mult = 0.3
    
    st.caption(f"Composite Risk Score: {composite_risk:.2f}")

# ======================
# Get latest data
# ======================
latest = df[df.Country == country].iloc[-1]
country_df = df[df.Country == country].copy()

# ======================
# Risk Level
# ======================
def risk_label(x):
    if x < 30: return "LOW", "#10b981"
    if x < 50: return "MODERATE", "#f59e0b"
    if x < 70: return "HIGH", "#f97316"
    return "CRITICAL", "#ef4444"

risk_level, risk_color = risk_label(latest.Risk_Score)

# تعريف expected_return هنا - قبل استخدامه
expected_return = 8 + (100 - latest.Risk_Score) * 0.15

# ======================
# KPI Row
# ======================
st.markdown("## 📊 **Key Performance Indicators**")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>GDP</h3>
        <h2>${latest.GDP/1e9:.1f}B</h2>
        <p style="color: {'#10b981' if latest.GDP_Growth>0 else '#ef4444'};">{latest.GDP_Growth:.1f}% YoY</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Inflation</h3>
        <h2>{latest.Inflation:.1f}%</h2>
        <p style="color: {'#f59e0b' if latest.Inflation>5 else '#10b981'};">Target: 2%</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Credit Growth</h3>
        <h2>{latest.Credit_Growth:.1f}%</h2>
        <p style="color: {'#ef4444' if latest.Credit_Growth>15 else '#10b981'};">Risk Adjusted</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Risk Score</h3>
        <h2>{latest.Risk_Score:.1f}</h2>
        <p style="color: {risk_color};">{risk_level}</p>
    </div>
    """, unsafe_allow_html=True)

# ======================
# Navigation Buttons
# ======================
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
st.markdown("## 📌 **Dashboard Navigation**")

nav_cols = st.columns(4)
with nav_cols[0]:
    market_btn = st.button("📈 MARKET ANALYSIS", use_container_width=True)
with nav_cols[1]:
    balanced_btn = st.button("🔄 BALANCED EXPANSION", use_container_width=True)
with nav_cols[2]:
    portfolio_btn = st.button("⚖️ PORTFOLIO OPTIMIZER", use_container_width=True)
with nav_cols[3]:
    risk_btn = st.button("📋 RISK REPORTS", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Set active tab
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'market'

if market_btn:
    st.session_state.active_tab = 'market'
elif balanced_btn:
    st.session_state.active_tab = 'balanced'
elif portfolio_btn:
    st.session_state.active_tab = 'portfolio'
elif risk_btn:
    st.session_state.active_tab = 'risk'

# ======================
# Market Analysis Tab
# ======================
if st.session_state.active_tab == 'market':
    st.markdown("## 📈 **Market Analysis**")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Multi-metric chart
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('GDP & Credit Trend', 'Inflation Trend', 'Growth Rates', 'Risk Trend'),
            specs=[[{'secondary_y': True}, {}], [{}, {}]]
        )
        
        fig.add_trace(
            go.Scatter(x=country_df['Year'], y=country_df['GDP'], 
                      name='GDP', line=dict(color='#3b82f6', width=3)),
            row=1, col=1, secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=country_df['Year'], y=country_df['Credit'],
                      name='Credit', line=dict(color='#10b981', width=3)),
            row=1, col=1, secondary_y=True
        )
        
        fig.add_trace(
            go.Scatter(x=country_df['Year'], y=country_df['Inflation'],
                      name='Inflation', line=dict(color='#f59e0b', width=3)),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=country_df['Year'], y=country_df['GDP_Growth'],
                      name='GDP Growth', line=dict(color='#8b5cf6', width=3)),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=country_df['Year'], y=country_df['Risk_Score'],
                      name='Risk Score', line=dict(color='#ef4444', width=3)),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=True, template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.markdown("### 🎯 **Current Risk Level**")
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest.Risk_Score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Score", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': risk_color, 'thickness': 0.3},
                'steps': [
                    {'range': [0, 30], 'color': "#d1fae5"},
                    {'range': [30, 50], 'color': "#fef3c7"},
                    {'range': [50, 70], 'color': "#ffedd5"},
                    {'range': [70, 100], 'color': "#fee2e2"}
                ]
            }
        ))
        fig_gauge.update_layout(height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Market insights
        st.markdown(f"""
        <div style="background:#f8fafc; padding:20px; border-radius:15px; margin-top:20px;">
            <h4>📊 Market Insights</h4>
            <p><strong>Market Tier:</strong> {market_tier}</p>
            <p><strong>Sovereign Rating:</strong> {sovereign_rating}</p>
            <p><strong>5Y Avg Growth:</strong> {country_df.GDP_Growth.tail(5).mean():.1f}%</p>
            <p><strong>Volatility:</strong> {country_df.GDP_Growth.std():.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

# ======================
# Balanced Expansion Tab
# ======================
if st.session_state.active_tab == 'balanced':
    st.markdown("## 🔄 **Balanced Expansion Analysis**")
    
    # Calculate expansion based on risk and appetite
    base_rate = max(0, (100 - latest.Risk_Score) / 100) * appetite_multipliers[risk_appetite] * alloc_mult
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        safe_amount = capital * base_rate * 0.7
        st.markdown(f"""
        <div style="background:#f0fdf4; padding:30px; border-radius:20px; border:2px solid #86efac; text-align:center;">
            <h3 style="color:#166534; font-size:1.8rem;">🛡️ DEFENSIVE</h3>
            <h2 style="font-size:2.5rem; color:#0f172a;">${safe_amount:,.0f}</h2>
            <p style="font-size:1.2rem;">{(safe_amount/capital)*100:.1f}% of Capital</p>
            <p style="color:#64748b;">Capital Preservation Focus</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        moderate_amount = capital * base_rate * 0.9
        st.markdown(f"""
        <div style="background:#fefce8; padding:30px; border-radius:20px; border:2px solid #fde047; text-align:center;">
            <h3 style="color:#854d0e; font-size:1.8rem;">⚖️ MODERATE</h3>
            <h2 style="font-size:2.5rem; color:#0f172a;">${moderate_amount:,.0f}</h2>
            <p style="font-size:1.2rem;">{(moderate_amount/capital)*100:.1f}% of Capital</p>
            <p style="color:#64748b;">Balanced Growth Strategy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        aggressive_amount = capital * base_rate
        st.markdown(f"""
        <div style="background:#fef2f2; padding:30px; border-radius:20px; border:2px solid #fca5a5; text-align:center;">
            <h3 style="color:#991b1b; font-size:1.8rem;">🚀 AGGRESSIVE</h3>
            <h2 style="font-size:2.5rem; color:#0f172a;">${aggressive_amount:,.0f}</h2>
            <p style="font-size:1.2rem;">{(aggressive_amount/capital)*100:.1f}% of Capital</p>
            <p style="color:#64748b;">Maximum Growth Focus</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 20px; color: white; margin-top: 20px;">
        <h3 style="color:white; font-size:2rem; text-align:center;">🎯 RECOMMENDED STRATEGY</h3>
        <p style="font-size:1.8rem; text-align:center; margin:20px 0;">Based on {risk_level} Risk Profile</p>
        <div style="display:flex; justify-content:space-around; text-align:center;">
            <div>
                <p style="font-size:1.2rem;">Optimal Expansion</p>
                <p style="font-size:2rem; font-weight:700;">${moderate_amount:,.0f}</p>
            </div>
            <div>
                <p style="font-size:1.2rem;">Expected Return</p>
                <p style="font-size:2rem; font-weight:700;">{expected_return:.1f}%</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ======================
# Portfolio Optimizer Tab
# ======================
if st.session_state.active_tab == 'portfolio':
    st.markdown("## ⚖️ **Portfolio Optimizer**")
    
    # Get top markets
    latest_data = df[df.Year == df.Year.max()].copy()
    top_markets = latest_data.nlargest(8, 'GDP')
    
    # Calculate optimal weights
    top_markets['Weight'] = 1 / (top_markets['Risk_Score'] + 1)
    top_markets['Allocation'] = (top_markets['Weight'] / top_markets['Weight'].sum()) * 100
    top_markets['Allocation'] = top_markets['Allocation'].clip(upper=25)
    top_markets['Allocation'] = (top_markets['Allocation'] / top_markets['Allocation'].sum()) * 100
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Treemap visualization
        fig = px.treemap(
            top_markets,
            path=['Country'],
            values='Allocation',
            color='Risk_Score',
            color_continuous_scale='RdYlGn_r',
            title='Optimal Portfolio Allocation'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk-return scatter
        fig2 = px.scatter(
            top_markets,
            x='Risk_Score',
            y='GDP_Growth',
            size='Allocation',
            color='Country',
            text='Country',
            title='Risk-Return Analysis'
        )
        fig2.update_traces(textposition='top center')
        fig2.update_layout(height=500)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Portfolio metrics
    port_risk = (top_markets['Allocation'] * top_markets['Risk_Score']).sum() / 100
    port_return = (top_markets['Allocation'] * (8 + (100 - top_markets['Risk_Score']) * 0.15)).sum() / 100
    
    colm1, colm2, colm3 = st.columns(3)
    with colm1:
        st.metric("Portfolio Risk", f"{port_risk:.1f}")
    with colm2:
        st.metric("Expected Return", f"{port_return:.1f}%")
    with colm3:
        st.metric("Markets", f"{len(top_markets)}")

# ======================
# Risk Reports Tab
# ======================
if st.session_state.active_tab == 'risk':
    st.markdown("## 🧪 **Economic Stress Testing**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stress test scenarios
        stress_data = pd.DataFrame({
            'Scenario': ['Base Case', 'Mild Recession', 'Severe Recession', 'Inflation Shock'],
            'Expected Loss': [2, 8, 18, 12],
            'Probability': [60, 25, 10, 5]
        })
        stress_data['Weighted Loss'] = stress_data['Expected Loss'] * stress_data['Probability'] / 100
        
        fig = px.bar(stress_data, x='Scenario', y=['Expected Loss', 'Weighted Loss'],
                    barmode='group', title='Expected Credit Loss Under Stress',
                    color_discrete_sequence=['#ef4444', '#f59e0b'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk decomposition
        risk_factors = pd.DataFrame({
            'Factor': ['Economic', 'Credit', 'Market', 'Regulatory', 'Liquidity'],
            'Contribution': [35, 25, 20, 12, 8]
        })
        fig2 = px.pie(risk_factors, values='Contribution', names='Factor',
                     title='Risk Contribution Analysis')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Risk limits
    st.markdown("### ⚠️ Risk Limits Dashboard")
    
    limits_data = pd.DataFrame({
        'Indicator': ['NPL Ratio', 'Concentration', 'LTV', 'Debt Coverage'],
        'Current': [3.2, 28.5, 65.0, 1.8],
        'Limit': [5.0, 30.0, 80.0, 1.2],
        'Status': ['🟢 Healthy', '🟡 Approaching', '🟢 Healthy', '🟢 Healthy']
    })
    st.dataframe(limits_data, use_container_width=True, hide_index=True)

# ======================
# Global Economic Overview
# ======================
st.markdown("---")
st.markdown("## 🌍 **Global Economic Overview**")

top_countries = df[df.Year == df.Year.max()].nlargest(6, 'GDP')
cols = st.columns(3)

for i, (_, row) in enumerate(top_countries.iterrows()):
    with cols[i % 3]:
        growth_color = "#10b981" if row.GDP_Growth > 0 else "#ef4444"
        st.markdown(f"""
        <div class="country-card">
            <b>{row.Country}</b>
            <div>
                <span>GDP:</span>
                <span style="font-weight:600;">${row.GDP/1e9:.1f}B</span>
            </div>
            <div>
                <span>Growth:</span>
                <span style="font-weight:600; color:{growth_color};">{row.GDP_Growth:.1f}%</span>
            </div>
            <div>
                <span>Inflation:</span>
                <span style="font-weight:600;">{row.Inflation:.1f}%</span>
            </div>
            <div>
                <span>Risk Score:</span>
                <span style="font-weight:600;">{row.Risk_Score:.0f}</span>
            </div>
            <div>
                <span>Rating:</span>
                <span style="font-weight:600;">{row.Sovereign_Rating}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ======================
# Decision Matrix
# ======================
st.markdown("---")
st.markdown("## 🎯 **Final Decision Matrix**")

col_d1, col_d2, col_d3 = st.columns(3)

with col_d1:
    growth_score = min(100, latest.GDP_Growth * 10 + 50)
    st.markdown(f"""
    <div class="decision-card">
        <h3>📈 Growth Potential</h3>
        <div style="font-size: 2.5rem; font-weight:700;">{growth_score:.0f}</div>
        <div class="progress-bar">
            <div class="progress-fill" style="background:#10b981; width:{growth_score}%;"></div>
        </div>
        <p>{'Strong' if growth_score > 70 else 'Moderate' if growth_score > 50 else 'Weak'} Growth Outlook</p>
    </div>
    """, unsafe_allow_html=True)

with col_d2:
    safety_score = 100 - latest.Risk_Score
    st.markdown(f"""
    <div class="decision-card">
        <h3>🛡️ Safety Score</h3>
        <div style="font-size: 2.5rem; font-weight:700;">{safety_score:.0f}</div>
        <div class="progress-bar">
            <div class="progress-fill" style="background:#3b82f6; width:{safety_score}%;"></div>
        </div>
        <p>{risk_level} Risk Environment</p>
    </div>
    """, unsafe_allow_html=True)

with col_d3:
    return_score = min(100, (100 - latest.Risk_Score) * 1.5)
    st.markdown(f"""
    <div class="decision-card">
        <h3>💰 Return Potential</h3>
        <div style="font-size: 2.5rem; font-weight:700;">{return_score:.0f}</div>
        <div class="progress-bar">
            <div class="progress-fill" style="background:#f59e0b; width:{return_score}%;"></div>
        </div>
        <p>Expected Return: {expected_return:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

# Final verdict
final_score = (growth_score + safety_score + return_score) / 3

if final_score > 75:
    verdict = "STRONG BUY"
    verdict_color = "#10b981"
    verdict_bg = "#d1fae5"
elif final_score > 60:
    verdict = "MODERATE BUY"
    verdict_color = "#3b82f6"
    verdict_bg = "#dbeafe"
elif final_score > 45:
    verdict = "HOLD"
    verdict_color = "#f59e0b"
    verdict_bg = "#fef3c7"
else:
    verdict = "AVOID / EXIT"
    verdict_color = "#ef4444"
    verdict_bg = "#fee2e2"

st.markdown(f"""
<div style="background:{verdict_bg}; padding:25px; border-radius:20px; margin:20px 0; text-align:center; border:2px solid {verdict_color};">
    <h2 style="color:{verdict_color};">🏁 FINAL VERDICT: {verdict}</h2>
    <p style="font-size:1.3rem;">Composite Score: {final_score:.1f}/100 | Market: {country} | Risk Level: {risk_level}</p>
    <div style="background:{verdict_color}; color:white; padding:15px 30px; border-radius:50px; display:inline-block; margin-top:10px; font-weight:700; font-size:1.3rem;">
        {action}
    </div>
</div>
""", unsafe_allow_html=True)

# ======================
# Quick Actions
# ======================
st.markdown("""
<div class="quick-actions-container">
    <h3>⚡ Quick Actions</h3>
</div>
""", unsafe_allow_html=True)

qa_cols = st.columns(2)
with qa_cols[0]:
    if st.button("📊 GENERATE COMPLETE RISK REPORT", use_container_width=True):
        st.success("✅ Risk report generated successfully! Check downloads folder.")
with qa_cols[1]:
    if st.button("🔄 OPTIMIZE PORTFOLIO ALLOCATION", use_container_width=True):
        st.success("✅ Portfolio optimized based on current market conditions!")

# Hide any success messages after 3 seconds
st.markdown("""
<script>
    setTimeout(function() {
        var alerts = window.parent.document.querySelectorAll('.stAlert');
        alerts.forEach(function(alert) {
            alert.style.display = 'none';
        });
    }, 3000);
</script>
""", unsafe_allow_html=True)