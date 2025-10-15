**Deployed Link**_ : https://abhinavj12-cc-statement-parser-ver2-app-t6mr6l.streamlit.app/

Home Page  
<img width="1917" height="730" alt="image" src="https://github.com/user-attachments/assets/e6b720b6-acd0-402c-a081-babbfa343b2a" />

<img width="1912" height="915" alt="image" src="https://github.com/user-attachments/assets/5546cc67-2ce2-4c46-a184-d2babe07b0d4" />

<img width="1876" height="891" alt="image" src="https://github.com/user-attachments/assets/b74123ab-2120-40a8-a432-896fbba6c450" />



# 💳 Multi-Bank Statement Parser

A powerful **Streamlit-based Python application** that automatically extracts, summarizes, and displays data from **bank and credit card statements (PDFs)**.  
Supports multiple **Indian and international banks**, providing a unified dashboard for financial insights.

---

## 🏦 Supported Banks

- **ICICI Bank**
- **Axis Bank**
- **HDFC Bank**
- **SBI (Savings Account)**
- **American Express**

---

## ✨ Key Features

✅ **Multi-Bank Support** — Automatically detects and parses statements from major banks.  
✅ **Automatic Bank Detection** — Identifies bank type using keywords and formatting.  
✅ **Transaction Extraction** — Extracts all transactions with date, description, and amount.  
✅ **CSV Export** — Download transactions for further analysis.  
✅ **Web Interface** — Simple, responsive Streamlit UI for quick viewing.  
✅ **Flexible Parsing** — Handles both digital and scanned statements using multiple extraction methods.  
✅ **Bank-Specific Display** — Tailored UI showing relevant financial details.

---

## 🖥️ Web Interface – How to Use

### 📤 Upload a Statement
Click **Browse files** or drag and drop a `.pdf` bank statement.

### 📈 View Results
Summary cards show important details like **total amount due**, **payment received**, etc.

### 📋 Review Transactions
All parsed transactions appear in a **sortable and filterable** table.

### 💾 Download CSV
Export the transactions by clicking **Download CSV**.

---

## ⚙️ How It Works

### 🧾 PDF Text Extraction
Uses multiple fallback methods for robust text reading:
- `pdfplumber` — Primary extraction method for accurate results.
- `PyPDF2` — Fallback for PDFs with layout issues.
- **Raw reading** — Last resort for edge cases.

### 🔍 Bank Detection
The parser auto-detects the bank by scanning for:
- Bank names (e.g., *HDFC, ICICI, Axis, SBI, AMEX*)
- Keywords (*Credit Card, Account, Statement*)
- Unique formatting patterns

### 🧮 Transaction Parsing
Each bank-specific parser:
- Extracts **dates**, **descriptions**, and **amounts**
- Detects **Debit/Credit** transactions
- Calculates **summary totals**
- Handles **multiple date formats**
- Supports both **₹ and $** currency symbols

---

## 📊 Extracted Data

### Common Fields (All Banks)
- Bank Name  
- Statement Date / Period  
- Total / Minimum Amount Due  
- Transactions (Date, Description, Amount)

### Bank-Specific Fields

| Bank | Unique Fields |
|------|----------------|
| **ICICI / Axis / HDFC** | Cardholder Name, Last 4 Digits, New Charges, Payment Received, Statement Balance |
| **SBI** | Account Number, Branch, Opening/Closing Balance, Total Credits/Debits |
| **AMEX** | Member Name, Account Number, Statement Period, Payments, New Charges |

---

## 📁 Project Structure

<img width="852" height="790" alt="image" src="https://github.com/user-attachments/assets/c15be588-6b2c-46f7-b01e-608f217a0441" />



---

## 🧩 Error Handling

The parser automatically handles:
- Corrupted or password-protected PDFs  
- Missing or inconsistent data  
- Multiple date formats  
- Currency symbol variations  

If parsing fails, the app displays:
- A **clear error message**
- A **debug trace** for investigation
- **Suggested troubleshooting** steps

---

## 🧠 Troubleshooting Guide

### "Unsupported Bank"
- Ensure the PDF is a valid statement  
- Check if the bank name is in the supported list  
- Try a cleaner, digital version of the PDF  

### "No Transactions Detected"
- Some PDFs use non-standard layouts  
- Try a different extraction method or statement version  

### "Missing Fields"
- Some statements omit fields like “Minimum Amount Due”  
- Missing fields are displayed as “—”

---

## 🧪 Sample Files

Sample PDFs for testing are available under the `/samples` folder:
- `391657900-SBI-statement-sample.pdf`
- `Axis_complex_statement.pdf`
- `HDFC-credit-card-statement.pdf`
- `ICICI_complex_statement.pdf`
- `amex_statement.pdf`

---

## 🔒 Security & Privacy

- All processing is **local** — no data leaves your device.  
- Temporary files are **auto-deleted** after use.  
- CSV exports are **stored locally** only.  

---

## 🛠️ Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/Abhinavj12/cc_statement_parser_ver2.git
cd cc_statement_parser_ver2

