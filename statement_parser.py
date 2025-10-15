import os
import csv
from typing import List, Dict, Tuple

# Import bank-specific parsers
from parsers.hdfc_parser import HDFCParser
from parsers.sbi_parser import SBIParser


def extract_text_from_pdf(path: str) -> str:
    """Extract text from PDF using multiple fallback methods"""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                ptext = page.extract_text()
                if ptext:
                    text += ptext + "\n"
    except Exception:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            for p in reader.pages:
                try:
                    ptext = p.extract_text()
                except Exception:
                    ptext = ""
                if ptext:
                    text += ptext + "\n"
        except Exception:
            with open(path, "rb") as f:
                raw = f.read()
            try:
                text = raw.decode("utf-8", errors="ignore")
            except Exception:
                text = ""
    return text


def detect_bank(text: str) -> str:
    """Detect which bank the statement belongs to"""
    t = text.upper()
    if "HDFC" in t and ("CREDIT CARD" in t or "CARD NO" in t):
        return "HDFC"
    if "STATE BANK OF INDIA" in t or "SBI" in t:
        return "SBI"
    if "ICICI" in t:
        return "ICICI"
    if "AXIS" in t:
        return "AXIS"
    if "AMERICAN EXPRESS" in t or "AMEX" in t:
        return "AMEX"
    return "UNKNOWN"


def parse_statement_file(path: str, export_csv: bool = True, csv_path: str = None) -> Tuple[Dict, List[Dict]]:
    """
    Main parsing function that detects bank and routes to appropriate parser

    Args:
        path: Path to PDF file
        export_csv: Whether to export transactions to CSV
        csv_path: Custom CSV path (optional)

    Returns:
        Tuple of (result_dict, transactions_list)
    """
    # Extract text from PDF
    text = extract_text_from_pdf(path)

    # Detect bank
    bank = detect_bank(text)

    # Initialize result
    result = {"bank": bank}
    transactions = []

    # Route to appropriate parser
    if bank == "HDFC":
        parser = HDFCParser()
        summary, transactions = parser.parse(text)
        result.update(summary)

    elif bank == "SBI":
        parser = SBIParser()
        summary, transactions = parser.parse(text)
        result.update(summary)

    # Add more banks here:
    # elif bank == "ICICI":
    #     parser = ICICIParser()
    #     summary, transactions = parser.parse(text)
    #     result.update(summary)

    else:
        raise Exception(f"Unsupported bank: {bank}. Please add parser for this bank.")

    # Add transaction count
    result['transactions_count'] = len(transactions)

    # Export transactions to CSV if requested
    if export_csv and transactions:
        if not csv_path:
            base = os.path.splitext(os.path.basename(path))[0]
            csv_path = base + "_transactions.csv"

        # Get field names from first transaction
        fieldnames = list(transactions[0].keys()) if transactions else []

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for tx in transactions:
                writer.writerow(tx)

        result['transactions_csv'] = os.path.abspath(csv_path)

    return result, transactions


if __name__ == "__main__":
    import argparse
    import json
    import pprint

    parser = argparse.ArgumentParser(description="Parse bank statements and export CSV")
    parser.add_argument("pdf", help="path to statement pdf")
    parser.add_argument("--csv", help="path to export csv (optional)", default=None)
    args = parser.parse_args()

    res, txs = parse_statement_file(args.pdf, export_csv=True, csv_path=args.csv)
    print(json.dumps(res, indent=4))
    print(f"\nSample transactions (first 10):")
    import itertools

    for tx in itertools.islice(txs, 0, 10):
        pprint.pprint(tx)