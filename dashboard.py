import streamlit as st
import requests
import time

st.set_page_config(page_title="Apex Store Intelligence", layout="wide")
API_URL = "http://localhost:8000"
STORE_ID = "STORE_BLR_002"

st.title(f"🏬 Live Store Dashboard: {STORE_ID}")

# Auto-refresh mechanism
placeholder = st.empty()

while True:
    try:
        metrics = requests.get(f"{API_URL}/stores/{STORE_ID}/metrics").json()
        health = requests.get(f"{API_URL}/health").json()
        anomalies = requests.get(f"{API_URL}/stores/{STORE_ID}/anomalies").json()
        funnel = requests.get(f"{API_URL}/stores/{STORE_ID}/funnel").json()

        with placeholder.container():
            # --- TOP ROW: METRICS ---
            st.subheader("Real-Time Traffic")
            col1, col2, col3 = st.columns(3)
            col1.metric("Unique Visitors Today", metrics.get("unique_visitors", 0))
            col2.metric("Est. Conversion Rate", f"{metrics.get('conversion_rate', 0.0) * 100:.1f}%")
            col3.metric("Data Confidence", metrics.get("data_confidence", "LOW"))
            
            st.divider()
            
            # --- MIDDLE ROW: FUNNEL & ANOMALIES ---
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Conversion Funnel")
                f_counts = funnel.get("funnel_counts", {})
                st.write(f"🚶 Entry: {f_counts.get('1_entry', 0)}")
                st.write(f"👀 Zone Visit: {f_counts.get('2_zone_visit', 0)}")
                st.write(f"🛒 Billing Queue: {f_counts.get('3_billing_queue', 0)}")
                
            with col_b:
                st.subheader("System Alerts")
                active_anomalies = anomalies.get("active_anomalies", [])
                if active_anomalies:
                    for a in active_anomalies:
                        if a["severity"] == "WARN":
                            st.error(f"🚨 {a['type']}: {a['description']}")
                        else:
                            st.info(f"ℹ️ {a['type']}: {a['description']}")
                else:
                    st.success("All systems nominal. No active anomalies.")
                    
            # --- BOTTOM ROW: HEALTH ---
            st.caption(f"API Status: {health.get('status', 'Unknown')} | Last updated: {time.strftime('%X')}")
            
    except requests.exceptions.ConnectionError:
        with placeholder.container():
            st.error("Cannot connect to API. Please ensure `uvicorn app.main:app` is running.")
            
    time.sleep(2) # Refresh every 2 seconds