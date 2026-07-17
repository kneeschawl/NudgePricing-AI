# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from core.architect import inject_decoy_price
from core.simulator import generate_consumer_agents, run_choice_simulation
from agents.llm_client import get_llm_client, MODEL_NAME
from agents.prompt_templates import get_bounded_system_prompt

# --- ENTERPRISE UI CONFIGURATION ---
st.set_page_config(
    page_title="NudgePricing AI | Enterprise Suite", 
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Inject modern, enterprise-grade custom CSS (Theme-Adaptive)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
        
        /* Global Typography - Let Streamlit handle colors dynamically! */
        html, body, [class*="ViewContainer"] {
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }
        
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Sleek Status Pill with safe top margin to prevent clipping */
        .engine-pill {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            background-color: rgba(56, 189, 248, 0.15);
            color: #38BDF8; /* Vibrant sky blue */
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-top: 1.5rem; /* Pushes the pill down away from the header ceiling */
            margin-bottom: 0.5rem;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }

        /* Metric Card Overhaul - Transparent to adapt to Light/Dark Mode automatically */
        div[data-testid="stMetric"] {
            background-color: rgba(128, 128, 128, 0.05);
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 0.75rem;
            padding: 1rem 1.25rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15);
            border-color: rgba(128, 128, 128, 0.4);
        }
        div[data-testid="stMetricValue"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 2.25rem !important;
            font-weight: 800 !important;
        }
        div[data-testid="stMetricLabel"] {
            font-family: 'Inter', sans-serif !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            opacity: 0.7; 
        }
    </style>
""", unsafe_allow_html=True)

# Initialize persistent multi-agent backend state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "consumer_agents" not in st.session_state:
    st.session_state.consumer_agents = generate_consumer_agents(num_agents=1000)

# --- HEADER FRAME ---
st.markdown('<div class="engine-pill">Quantitative Behavioral Engine</div>', unsafe_allow_html=True)
st.title("NudgePricing AI")
st.markdown("*An analytical modeling sandbox for asymmetric pricing architecture and consumer choice emulation.*")
st.divider()

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.header("Control Suite")
    ui_mode = st.radio(
        "Configuration Strategy:",
        ["Manual Price Tester", "AI Automated Optimization"],
        help="Select your preferred method for generating the pricing tier architecture."
    )

    p1, p2, p3 = 0.0, 0.0, 0.0

    if ui_mode == "Manual Price Tester":
        st.divider()
        st.subheader("1. Core Metadata")
        product_context = st.text_input("Product Category", "Premium Organic Coffee Beans")

        st.subheader("2. Pricing Architecture")
        p1 = st.number_input("Base Tier Price (Small) ($)", min_value=0.01, value=6.00, step=0.50)
        p2 = st.number_input("Decoy Tier Price (Medium) ($)", min_value=0.01, value=12.12, step=0.50)
        p3 = st.number_input("Premium Tier Price (Large) ($)", min_value=0.01, value=13.20, step=0.50)
        
        if p1 >= p2 or p2 >= p3:
            st.error("⚠️ Behavioral Boundary: Maintain structural integrity (Small < Medium < Large).")

    else:
        st.divider()
        st.subheader("1. Profit Metrics")
        product_context = st.text_input("Product Category", "Premium Organic Coffee Beans")
        cogs = st.number_input("Cost of Goods Sold ($)", min_value=0.50, value=3.00, step=0.50)
        target_margin = st.slider("Target Baseline Margin (%)", 10, 80, 50) / 100

        st.subheader("2. Asymmetric Controls")
        alpha = st.slider("Decoy Compression Ratio (Alpha)", 0.05, 0.35, 0.15, 
                          help="Closer to 0 pushes the decoy closer to the premium price. Closer to 1 pushes it toward the base price.")

        p1 = round(cogs / (1 - target_margin), 2)
        p3 = round(p1 * 2.2, 2)
        p2 = inject_decoy_price(p1, p3, alpha)

pricing_strategy = {"Small (Base)": p1, "Medium (Decoy)": p2, "Large (Premium)": p3}

# --- SIMULATION ENGINE PLATFORM ---
sim_results = run_choice_simulation(pricing_strategy, st.session_state.consumer_agents)

# UI Layout Grid Splits
col1, col2 = st.columns([5, 4], gap="large")

with col1:
    st.subheader("Architectural Matrix & Market Share")
    
    # Financial metrics laid out cleanly
    m_cols = st.columns(3)
    m_cols[0].metric("Base Tier", f"${p1:.2f}")
    m_cols[1].metric("Decoy Tier", f"${p2:.2f}")
    m_cols[2].metric("Premium Tier", f"${p3:.2f}")
    
    st.write("") # Spacer

    # Enterprise Plotly Chart
    plot_df = pd.DataFrame([
        {"Tier": k, "Share": float(v.replace("%", ""))} 
        for k, v in sim_results.items() if k != "Total Revenue Generated"
    ])
    
    fig = px.bar(
        plot_df, x="Tier", y="Share", text="Share",
        labels={"Share": "Market Selection Share (%)", "Tier": ""},
        color="Tier",
        color_discrete_map={
            "Small (Base)": "#38BDF8",     # Modern Sky Blue
            "Medium (Decoy)": "#818CF8",   # Soft Indigo
            "Large (Premium)": "#312E81",  # Deep Corporate Navy
            "No Purchase": "#E11D48"       # Muted Rose/Red
        }
    )
    
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        height=320,
        hovermode="x unified"
    )
    
    fig.update_yaxes(
        gridcolor="rgba(128,128,128,0.15)", 
        title_font=dict(size=12),
        zeroline=False
    )
    fig.update_xaxes(
        tickfont=dict(size=13, family="Plus Jakarta Sans, sans-serif")
    )
    fig.update_traces(
        texttemplate='<b>%{text}%</b>', 
        textposition='outside',
        textfont=dict(size=14, family="Plus Jakarta Sans")
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    st.subheader("Financial Performance Metrics")
    
    st.metric("Projected Batch Revenue", sim_results["Total Revenue Generated"])
    st.caption("Modeled performance distribution calculated across 1,000 synthetic consumer agents.")
    
    st.write("") # Spacer
    
    # ─── DYNAMIC STATE SELECTOR FOR MARKET FRICTION ───
    abandonment_rate_str = sim_results["No Purchase"]
    abandonment_val = float(abandonment_rate_str.replace("%", ""))
    
    if abandonment_val < 25.0:
        st.success(
            f"**Optimal Market Capture**\n\nOnly **{abandonment_rate_str}** of target consumers exited without purchasing. The perceived value effectively overcomes price friction at these tiers.", 
            icon="✅"
        )
    elif 25.0 <= abandonment_val <= 50.0:
        st.warning(
            f"**Moderate Friction Detected**\n\n**{abandonment_rate_str}** of target consumers abandoned their carts. Consider slightly compressing the decoy gap to capture more budget-sensitive agents.", 
            icon="⚠️"
        )
    else:
        st.error(
            f"**Critical Abandonment Rate**\n\n**{abandonment_rate_str}** of your market walked away. The current pricing architecture exceeds the population's maximum utility threshold.", 
            icon="🚨"
        )

st.divider()

# --- DIALOGUE ANALYTICS LAYER ---
st.subheader("Executive Strategy Briefing")
st.caption("Consult your AI pricing architect to review structural optimization vectors derived directly from the current dataset.")

context_document = get_bounded_system_prompt(product_context, pricing_strategy, sim_results)

# Render Chat Interface
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Inquire regarding pricing friction patterns..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    messages_payload = [{"role": "system", "content": context_document}]
    for msg in st.session_state.chat_history[-5:]:
        messages_payload.append({"role": msg["role"], "content": msg["content"]})
        
    with st.chat_message("assistant"):
        try:
            client = get_llm_client()
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages_payload,
                temperature=0.2
            )
            bot_reply = response.choices[0].message.content
            st.markdown(bot_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        except Exception as e:
            st.error(f"Execution Error. Verify your local backend instance configurations. Details: {str(e)}")