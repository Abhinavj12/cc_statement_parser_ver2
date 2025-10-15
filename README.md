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
Multi-Bank Statement Parser
A powerful Python application that automatically extracts summary information and transaction details from credit card and bank account statements in PDF format. Supports multiple Indian and international banks with a clean, interactive web interface.
Features

Multi-Bank Support: Parse statements from ICICI, Axis, SBI, HDFC, and American Express
Automatic Bank Detection: Intelligently detects which bank based on statement content
Transaction Extraction: Automatically extracts all transactions with dates, descriptions, and amounts
CSV Export: Download transaction data as CSV for further analysis
Web Interface: User-friendly Streamlit interface with real-time parsing
Flexible Parsing: Handles multiple PDF text extraction methods for reliability
Bank-Specific Display: Tailored UI for each bank type showing relevant financial data

Using the Web Interface

Upload PDF: Click "Browse files" or drag-and-drop a bank statement PDF
View Results: Summary information appears automatically
Review Transactions: Table displays all extracted transactions
Download CSV: Click the download button to export transactions as CSV

How It Works
PDF Text Extraction
The parser uses multiple fallback methods for robust text extraction:

pdfplumber - Primary method for accurate text extraction
PyPDF2 - Secondary fallback
Raw file reading - Last resort for problematic PDFs

Bank Detection
Automatically identifies the bank by scanning for:

Bank names (HDFC, ICICI, Axis, SBI, American Express)
Statement keywords (Credit Card, Account, etc.)
Specific formatting patterns

Transaction Parsing
Each bank parser:

Extracts transaction dates (multiple date formats supported)
Parses descriptions and amounts
Identifies transaction types (Credit/Debit)
Calculates totals and summaries
Handles currency conversions (₹ and $)

Extracted Data
Common Fields (All Banks)

Bank name
Statement date/period
Payment due date
Total amount due
Transactions with dates, descriptions, and amounts

Bank-Specific Fields
ICICI/Axis/HDFC:

Card name and last 4 digits
Card holder name
Previous balance
Payment received
New charges
Statement balance
Minimum amount due

SBI:

Account holder name
Account number
Branch
Opening balance
Closing balance
Total credits/debits
Net change

AMEX:

Member name
Account number
Statement period
Previous balance
Payments made
New charges

File Format Requirements

Format: PDF (.pdf)
Max Size: 200MB
Recommended: Scanned or digital bank statements
Language: English

Error Handling
The application handles:

Corrupted or password-protected PDFs
Missing or poorly formatted fields
Multiple date formats
Currency symbol variations
Encoding issues

If parsing fails, the application displays:

Clear error message
Python traceback for debugging
Suggested troubleshooting steps

Troubleshooting
"Unsupported bank" Error

Ensure the PDF is a valid bank statement
Check that the bank name appears in the supported list
Verify the PDF contains expected statement elements

"No transactions detected"

The PDF may use unusual formatting
Try uploading a different statement
Check the DEBUG panel for extracted text

Missing Fields

Some fields may be optional (not all statements contain all info)
Use the DEBUG panel to see what was extracted
The application displays "—" for missing fields

Sample Files
Test files are included in the samples/ folder:

391657900-SBI-statement-sample.pdf - SBI savings account
Axis_complex_statement.pdf - Axis credit card
HDFC-credit-card-statement.pdf - HDFC credit card
ICICI_complex_statement.pdf - ICICI credit card
amex_statement.pdf - American Express statement

Security & Privacy

PDFs are processed locally on your machine
No data is sent to external servers
Temporary files are cleaned up automatically
CSV exports are saved locally only

Output Formats
Web Display

Summary cards with key information
Transaction table with sorting/filtering
Analysis charts and statistics
Bank-specific customized layouts

CSV Export
Includes columns:

Date
Type (Debit/Credit)
Description
Amount
Bank-specific fields





