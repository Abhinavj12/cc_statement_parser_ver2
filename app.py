import streamlit as st
import os
import tempfile
import pandas as pd

from statement_parser import parse_statement_file

st.set_page_config(page_title="💳 Multi-Bank Statement Parser", layout="wide")

st.title("💳 Multi-Bank Statement Parser")
st.write("Upload a bank statement PDF to extract summary and transactions automatically.")
st.write("**Supported Banks:** ICICI, Axis, SBI, HDFC, AMEX")

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
            bank = result.get('bank', result.get('Bank', 'Unknown'))
            st.success(f"✅ Parsed successfully! Bank detected: **{bank}**")
        except Exception as e:
            st.error(f"❌ Parsing failed: {e}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()

    # DEBUG: Show raw extracted data
    with st.expander("🔧 DEBUG - Raw Extracted Data"):
        st.json(result)

    # ============= SUMMARY SECTION =============
    st.subheader("📘 Summary")

    bank = result.get('bank', result.get('Bank', 'Unknown'))

    # ===== ICICI / AXIS Credit Card =====
    if bank in ['ICICI', 'Axis']:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🏦 Bank", bank)
            st.write("**💳 Card Name:**", result.get('Card Name', '—'))

        with col2:
            st.write("**🔢 Card Last 4:**", result.get('Card Last 4', '—'))
            st.write("**🗓️ Statement Date:**", result.get('Statement Date', '—'))

        with col3:
            st.write("**📅 Payment Due:**", result.get('Payment Due Date', '—'))
            st.write("**💰 Total Due:**", f"₹ {result.get('Total Amount Due', 0):,.2f}")
            st.write("**💰 Min. Due:**", f"₹ {result.get('Minimum Amount Due', 0):,.2f}")

        # Account Summary Section
        st.markdown("---")
        st.subheader("💰 Account Summary")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            prev_bal = result.get('Previous Balance', 0)
            st.metric("Previous Balance", f"₹ {prev_bal:,.2f}")

        with col2:
            payment = result.get('Payment Received', 0)
            st.metric("Payment Received", f"₹ {payment:,.2f}" if payment else "—")

        with col3:
            new_charges = result.get('New Charges', 0)
            st.metric("New Charges", f"₹ {new_charges:,.2f}")

        with col4:
            stmt_bal = result.get('Statement Balance', 0)
            st.metric("Statement Balance", f"₹ {stmt_bal:,.2f}")

    # ===== SBI Savings Account =====
    elif bank == 'SBI':
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

    # ===== HDFC Credit Card =====
    elif bank == 'HDFC':
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🏦 Bank", bank)
            st.write("**👤 Card Holder:**", result.get('Card Holder Name', '—'))

        with col2:
            st.write("**🔢 Card Last 4:**", result.get('Card Last 4', '—'))
            st.write("**🗓️ Statement Date:**", result.get('Statement Date', '—'))

        with col3:
            st.write("**📅 Payment Due:**", result.get('Payment Due Date', '—'))
            st.write("**💰 Total Due:**", f"₹ {result.get('Total Amount Due', 0):,.2f}")

        # Account Summary
        st.markdown("---")
        st.subheader("💰 Account Summary")
        col1, col2 = st.columns(2)

        with col1:
            prev_bal = result.get('Previous Balance', 0)
            st.metric("Previous Balance", f"₹ {prev_bal:,.2f}")
            new_charges = result.get('New Charges', 0)
            st.metric("New Charges", f"₹ {new_charges:,.2f}")

        with col2:
            payment = result.get('Payment Received', 0)
            st.metric("Payment Received", f"₹ {payment:,.2f}" if payment else "—")
            stmt_bal = result.get('Statement Balance', 0)
            st.metric("Statement Balance", f"₹ {stmt_bal:,.2f}")

    # ===== AMEX Credit Card =====
    elif bank == 'AMEX':
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🏦 Bank", bank)
            st.write("**👤 Member Name:**", result.get('Member Name', '—'))

        with col2:
            st.write("**🔢 Account Number:**", result.get('Account Number', '—'))
            st.write("**📅 Statement Period:**", result.get('Statement Period', '—'))

        with col3:
            st.write("**📅 Due Date:**", result.get('Due Date', '—'))
            st.write("**💰 Amount Due:**", f"${result.get('Amount Due', 0):,.2f}")

        # Account Summary
        st.markdown("---")
        st.subheader("💰 Account Summary")
        col1, col2, col3 = st.columns(3)

        with col1:
            prev_bal = result.get('Previous Balance', 0)
            st.metric("Previous Balance", f"${prev_bal:,.2f}")

        with col2:
            payments = result.get('Payments', 0)
            st.metric("Payments", f"${payments:,.2f}" if payments else "—")

        with col3:
            new_charges = result.get('New Charges', 0)
            st.metric("New Charges", f"${new_charges:,.2f}")

    else:
        st.info("Bank-specific display not configured. Showing raw data.")
        for key, value in result.items():
            if key not in ('transactions_count', 'transactions_csv', 'bank', 'Bank'):
                st.write(f"**{key}:**", value)

    # ============= TRANSACTIONS SECTION =============
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

        # Optional: Show statistics for credit card statements
        if bank in ['ICICI', 'Axis', 'HDFC']:
            st.markdown("---")
            st.subheader("📈 Transaction Analysis")
            col1, col2 = st.columns(2)

            total_debits = result.get('Total Debits', 0)
            total_credits = result.get('Total Credits', 0)

            with col1:
                st.metric("Total Debits", f"₹ {total_debits:,.2f}")
            with col2:
                st.metric("Total Credits", f"₹ {total_credits:,.2f}")

        elif bank == 'AMEX':
            st.markdown("---")
            st.subheader("📈 Transaction Analysis")
            col1, col2 = st.columns(2)

            total_transactions = result.get('Total Transactions', 0)
            total_amount = result.get('Total Amount', 0)

            with col1:
                st.metric("Total Transactions", total_transactions)
            with col2:
                st.metric("Total Amount", f"${total_amount:,.2f}")

    else:
        st.info("No transactions detected.")

else:
    st.info("👆 Please upload a PDF to begin parsing.")