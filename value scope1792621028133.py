import math
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="ValueScope — PSX Stock Valuation",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Custom Styling
st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        color: #10B981 !important;
        font-weight: 700;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #10B981;
        margin-bottom: 0px;
    }
    .tagline-box {
        background-color: #0F172A;
        border-left: 4px solid #10B981;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 25px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Header & Branding Section
st.markdown("<div class='main-header'>ValueScope</div>", unsafe_allow_html=True)
st.markdown(
    "**Analyze • Find • Invest** — *Smarter insights for a stronger Pakistan"
    " Stock Exchange*",
    unsafe_allow_html=True,
)

st.markdown("""
<div class="tagline-box">
    <b>Core Features:</b> Analyze Stocks | Find Value | Spot Opportunities | Grow Your Wealth
</div>
""", unsafe_allow_html=True)

# 4. Sidebar Inputs
st.sidebar.header("⚙️ Configuration & Inputs")

default_ticker = "LUCK"
default_price = 850.0
default_eps = 65.40
default_bvps = 450.20
default_dps = 20.0

ticker = st.sidebar.text_input("Ticker Symbol", value=default_ticker).upper()
market_price = st.sidebar.number_input(
    "Market Price (PKR)", value=default_price, min_value=0.01
)
eps = st.sidebar.number_input("EPS (PKR)", value=default_eps)
bvps = st.sidebar.number_input(
    "Book Value / Share (BVPS) (PKR)", value=default_bvps
)
dps = st.sidebar.number_input("Dividend / Share (DPS) (PKR)", value=default_dps)

# 5. Core Valuation Logic
pe_ratio = market_price / eps if eps > 0 else float("inf")
pb_ratio = market_price / bvps if bvps > 0 else float("inf")
earnings_yield = (eps / market_price) * 100 if market_price > 0 else 0.0
dividend_yield = (dps / market_price) * 100 if market_price > 0 else 0.0

if eps > 0 and bvps > 0:
  graham_number = math.sqrt(22.5 * eps * bvps)
else:
  graham_number = 0.0

price_to_graham_pct = (
    ((market_price - graham_number) / graham_number) * 100
    if graham_number > 0
    else 0.0
)

# 6. Dashboard Display
st.subheader(f"📊 Valuation Analysis for `{ticker}`")

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric(
    "P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio != float("inf") else "N/A"
)
m2.metric(
    "Price / Book", f"{pb_ratio:.2f}" if pb_ratio != float("inf") else "N/A"
)
m3.metric("Earnings Yield", f"{earnings_yield:.2f}%")
m4.metric("Dividend Yield", f"{dividend_yield:.2f}%")
m5.metric("Graham Fair Value", f"PKR {graham_number:.2f}")

st.markdown("---")

# 7. Price vs Fair Value Chart
st.subheader("🎯 Market Price vs. Graham Number")

chart_data = pd.DataFrame({
    "Metric": ["Market Price", "Graham Number"],
    "Value (PKR)": [market_price, graham_number],
})
st.bar_chart(chart_data.set_index("Metric"))

if market_price <= graham_number:
  st.success(
      f"🟢 **Undervalued Signal:** Market price (PKR {market_price:.2f}) is"
      f" below Graham Fair Value (PKR {graham_number:.2f})."
  )
else:
  st.warning(
      f"🟡 **Premium Valuation:** Market price (PKR {market_price:.2f}) is"
      f" {price_to_graham_pct:.1f}% above Graham Fair Value (PKR"
      f" {graham_number:.2f})."
  )

st.markdown("---")

# 8. Detailed Breakdown & CSV Export
st.subheader("📋 Valuation Metrics Breakdown")

details_df = pd.DataFrame([
    {
        "Metric": "Ticker Symbol",
        "Value": ticker,
        "Notes": "Pakistan Stock Exchange Symbol",
    },
    {
        "Metric": "Market Price",
        "Value": f"PKR {market_price:.2f}",
        "Notes": "Current share price",
    },
    {"Metric": "EPS", "Value": f"PKR {eps:.2f}", "Notes": "Earnings per share"},
    {
        "Metric": "BVPS",
        "Value": f"PKR {bvps:.2f}",
        "Notes": "Book value per share",
    },
    {
        "Metric": "DPS",
        "Value": f"PKR {dps:.2f}",
        "Notes": "Annual dividend per share",
    },
    {
        "Metric": "P/E Ratio",
        "Value": f"{pe_ratio:.2f}" if pe_ratio != float("inf") else "N/A",
        "Notes": "Price-to-Earnings",
    },
    {
        "Metric": "P/B Ratio",
        "Value": f"{pb_ratio:.2f}" if pb_ratio != float("inf") else "N/A",
        "Notes": "Price-to-Book",
    },
    {
        "Metric": "Earnings Yield",
        "Value": f"{earnings_yield:.2f}%",
        "Notes": "EPS / Price",
    },
    {
        "Metric": "Dividend Yield",
        "Value": f"{dividend_yield:.2f}%",
        "Notes": "DPS / Price",
    },
    {
        "Metric": "Graham Number",
        "Value": f"PKR {graham_number:.2f}",
        "Notes": "sqrt(22.5 * EPS * BVPS)",
    },
])

st.dataframe(details_df, use_container_width=True)

st.download_button(
    label="📥 Download Valuation Report (CSV)",
    data=details_df.to_csv(index=False).encode("utf-8"),
    file_name=f"{ticker}_valuescope_report.csv",
    mime="text/csv",
)

st.markdown("---")
st.caption(
    "⚠️ **Disclaimer:** ValueScope is an educational stock analysis tool,"
    " not financial advice. Verify all numbers via official PSX financial"
    " statements."
)