Home Page  
<img width="1917" height="730" alt="image" src="https://github.com/user-attachments/assets/e6b720b6-acd0-402c-a081-babbfa343b2a" />

<img width="1912" height="915" alt="image" src="https://github.com/user-attachments/assets/5546cc67-2ce2-4c46-a184-d2babe07b0d4" />

<img width="1876" height="891" alt="image" src="https://github.com/user-attachments/assets/b74123ab-2120-40a8-a432-896fbba6c450" />

cc_statement_parser/
│
├── .venv/                          # Virtual environment (ignore)
│
├── parsers/                        # All parser modules
│   ├── __init__.py                 # Empty file (makes it a package)
│   ├── hdfc_parser.py              # HDFC credit card parser
│   ├── sbi_parser.py               # SBI savings account parser
│   ├── credit_card_parser.py       # ICICI & Axis unified parser
│   └── amex_parser.py              # American Express parser
│
├── samples/                        # Sample PDF files for testing
│   ├── 391657900-SBI-statement-sample.pdf
│   ├── amex_statement.pdf
│   ├── Axis_complex_statement.pdf
│   ├── HDFC-credit-card-statement.pdf
│   └── ICICI_complex_statement.pdf
│
├── app.py                          # Main Streamlit app
├── statement_parser.py             # Core routing logic
│
├── README.md                       # Documentation
├── requirements.txt                # Python dependencies
│
└── (generated files)
    ├── HDFC-credit-card-statement_transactions.csv
    ├── ICICI_complex_statement_transactions.csv
    ├── etc...

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

1. **Run the App**
   ```bash
   streamlit run app.py
Upload a Statement

Click Browse files or drag and drop a .pdf bank statement.

View Results

Summary cards show important details like total amount due, payment received, etc.

Review Transactions

All parsed transactions appear in a sortable and filterable table.

Download CSV

Export the transactions by clicking Download CSV.

⚙️ How It Works
🧾 PDF Text Extraction

Uses multiple fallback methods for robust text reading:

pdfplumber — Primary extraction method for accurate results.

PyPDF2 — Fallback for PDFs with layout issues.

Raw reading — Last resort for edge cases.

🔍 Bank Detection

The parser auto-detects the bank by scanning for:

Bank names (e.g., HDFC, ICICI, Axis, SBI, AMEX)

Keywords (Credit Card, Account, Statement)

Unique formatting patterns

🧮 Transaction Parsing

Each bank-specific parser:

Extracts dates, descriptions, and amounts

Detects Debit/Credit transactions

Calculates summary totals

Handles multiple date formats

Supports both ₹ and $ currency symbols

📊 Extracted Data

Common Fields (All Banks):

Bank Name

Statement Date / Period

Total / Minimum Amount Due

Transactions (Date, Description, Amount)
