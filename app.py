import streamlit as st
import os
import sys
import tempfile
import pandas as pd
import json

# ✅ Ensure the current directory is in Python path so statement_parser.py is found
sys.path.append(os.path.dirname(__file__))
from statement_parser import parse_statement_file

st.set_page_config(page_title="💳 Credit Card Statement Parser — HDFC (Real PDF)", layout="wide")

st.title("💳 Credit Card Statement Parser — HDFC (Real PDF)")
st.write("Upload a credit card statement PDF to extract summary and transactions automatically.")

uploaded = st.file_uploader("📄 Upload a Credit Card Statement (PDF)", type=["pdf"])

if uploaded:
    # Save uploaded PDF to a temporary file
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tf.write(uploaded.read())
    tf.close()
    pdf_path = tf.name

    with st.spinner("🔍 Parsing your PDF statement..."):
        try:
            result, transactions = parse_statement_file(pdf_path, export_csv=True)
            st.success("✅ Parsed successfully!")
        except Exception as e:
            st.error(f"❌ Parsing failed: {e}")
            st.stop()

    # DEBUG: Show raw extracted data
    with st.expander("🔧 DEBUG - Raw Extracted Data"):
        st.json(result)

    # ---------------- Summary ----------------
    st.subheader("📘 Summary")

    summary = {
        k: v for k, v in result.items()
        if k not in ('transactions_count', 'transactions_csv', 'bank')
    }

    # Arrange summary fields in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏦 Bank", result.get('bank', 'Unknown'))
        card_holder = result.get('Card Holder Name', '—')
        st.write("**👤 Card Holder:**", card_holder if card_holder else "❌ NOT EXTRACTED")

    with col2:
        st.write("**💳 Card Last 4:**", result.get('Card Last 4', '—'))
        st.write("**🗓️ Statement Date:**", result.get('Statement Date', '—'))

    with col3:
        payment_due = result.get('Payment Due Date', '—')
        st.write("**📅 Payment Due Date:**", payment_due if payment_due else "❌ NOT EXTRACTED")
        st.write("**💰 Total Amount Due:**", result.get('Total Amount Due', '—'))

    # ---------------- Transactions ----------------
    st.markdown("---")
    st.subheader(f"📊 Transactions ({result.get('transactions_count', 0)})")

    if transactions:
        df = pd.DataFrame(transactions)
        st.dataframe(df, use_container_width=True)

        # Allow download as CSV
        csv_path = result.get('transactions_csv')
        if csv_path and os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                st.download_button(
                    label="📥 Download Transactions CSV",
                    data=f,
                    file_name=os.path.basename(csv_path),
                    mime="text/csv"
                )
    else:
        st.info("No transactions detected.")
else:
    st.info("👆 Please upload a PDF to begin parsing.")