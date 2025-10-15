import streamlit as st
import os
import tempfile
import pandas as pd

from statement_parser import parse_statement_file

st.set_page_config(page_title="💳 Multi-Bank Statement Parser", layout="wide")

st.title("💳 Multi-Bank Statement Parser")
st.write("Upload a bank statement PDF to extract summary and transactions automatically.")
st.write("**Supported Banks:** HDFC, SBI, (easily extensible to ICICI, Axis, etc.)")

uploaded = st.file_uploader("📄 Upload a Bank Statement (PDF)", type=["pdf"])

if uploaded:
    # Save uploaded PDF to a temporary file
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tf.write(uploaded.read())
    tf.close()
    pdf_path = tf.name

    with st.spinner("🔍 Parsing your PDF statement..."):
        try:
            result, transactions = parse_statement_file(pdf_path, export_csv=True)
            st.success(f"✅ Parsed successfully! Bank detected: **{result.get('bank', 'Unknown')}**")
        except Exception as e:
            st.error(f"❌ Parsing failed: {e}")
            import traceback

            st.code(traceback.format_exc())
            st.stop()

    # DEBUG: Show raw extracted data
    with st.expander("🔧 DEBUG - Raw Extracted Data"):
        st.json(result)

    # ---------------- Summary ----------------
    st.subheader("📘 Summary")

    bank = result.get('bank', 'Unknown')

    # Display bank-specific fields
    if bank == "HDFC":
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🏦 Bank", bank)
            card_holder = result.get('Card Holder Name', '—')
            st.write("**👤 Card Holder:**", card_holder if card_holder else "❌ NOT EXTRACTED")

        with col2:
            st.write("**💳 Card Last 4:**", result.get('Card Last 4', '—'))
            st.write("**🗓️ Statement Date:**", result.get('Statement Date', '—'))

        with col3:
            payment_due = result.get('Payment Due Date', '—')
            st.write("**📅 Payment Due Date:**", payment_due if payment_due else "❌ NOT EXTRACTED")
            st.write("**💰 Total Amount Due:**", result.get('Total Amount Due', '—'))

    elif bank == "SBI":
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🏦 Bank", bank)
            st.write("**👤 Account Holder:**", result.get('Account Holder', '—'))

        with col2:
            st.write("**🔢 Account Number:**", result.get('Account Number', '—'))
            st.write("**🏢 Branch:**", result.get('Branch', '—'))

        with col3:
            period = result.get('Statement Period', '—')
            st.write("**📅 Statement Period:**", period)
            st.write("**💰 Opening Balance:**", f"₹ {result.get('Opening Balance', 0):,.2f}")
            st.write("**💰 Closing Balance:**", f"₹ {result.get('Closing Balance', 0):,.2f}")

        # Transaction Summary for SBI
        if result.get('Total Credits') is not None:
            st.markdown("---")
            st.subheader("💰 Transaction Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Credits", f"₹ {result.get('Total Credits', 0):,.2f}")
            with col2:
                st.metric("Total Debits", f"₹ {result.get('Total Debits', 0):,.2f}")
            with col3:
                st.metric("Net Change", f"₹ {result.get('Net Change', 0):,.2f}")

    else:
        st.info("Bank-specific display not configured. Showing raw data.")
        for key, value in result.items():
            if key not in ('transactions_count', 'transactions_csv', 'bank'):
                st.write(f"**{key}:**", value)

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