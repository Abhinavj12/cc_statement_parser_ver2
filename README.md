
# Credit Card Statement Parser

This project is a sample implementation for a Credit Card Statement Parser assignment.
It extracts five key data points (Card Holder, Card Last 4 digits, Billing Period, Payment Due Date, Total Due)
from simple PDF statement samples for five issuers: HDFC, ICICI, Axis, SBI, and American Express.

## Structure
- `parser.py` - Main parser script. Run: `python parser.py samples/hdfc_statement.pdf`
- `app.py` - Streamlit demo app. Run: `streamlit run app.py`
- `samples/` - Contains sample PDF statements (anonymized and programmatically generated)
- `requirements.txt` - Suggested Python packages

## Notes
- The parser is pattern-based and uses regular expressions. For production-grade parsing you would:
  - use OCR for scanned PDFs,
  - build bank-specific templates,
  - use table extraction for transaction tables,
  - add robust date and currency normalization.

## Deliverables you can show
- `parser.py` demo run
- `samples/` folder with sample PDFs
- `output.json` (you can generate by running the parser)
