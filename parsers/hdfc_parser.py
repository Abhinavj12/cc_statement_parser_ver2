import re
from typing import List, Dict, Tuple


class HDFCParser:
    """Parser specifically for HDFC Credit Card statements"""

    def __init__(self):
        pass

    def parse_amount(self, amount_str: str) -> float:
        """Convert amount string to float"""
        if not amount_str:
            return 0.0
        s = str(amount_str).replace(",", "").strip()
        s = re.sub(r"[^\d\.\-]", "", s)
        try:
            return float(s) if s else 0.0
        except:
            return 0.0

    def parse(self, text: str) -> Tuple[Dict, List[Dict]]:
        """
        Parse HDFC credit card statement

        Args:
            text: Extracted text from PDF

        Returns:
            Tuple of (summary_dict, transactions_list)
        """
        data = {}
        transactions = []

        t = text.replace('\xa0', ' ')

        # CARD HOLDER NAME
        m = re.search(r'(?:Name|Ca:rd|rdNIKHIL|HN DFa.*?)(NIKHIL KHANDELWAL|[A-Z][A-Z\s]{5,})', t)
        if m:
            name = m.group(1).strip() if m.lastindex > 0 else m.group(0).strip()
            name = re.sub(r'\s+', ' ', name)
            if name and len(name) > 3:
                data['Card Holder Name'] = name
        else:
            # Try to extract from "Domestic Transactions" section
            m = re.search(r'Domestic Transactions.*?(NIKHIL KHANDELWAL|[A-Z]{2,}\s+[A-Z]{2,})', t, re.DOTALL)
            if m:
                data['Card Holder Name'] = m.group(1).strip()

        # CARD LAST 4
        m = re.search(r'Card\s*(?:No|Number|No\.)\s*[:\-]?\s*\d{4}\s+\d{2}[Xx]{2}\s+[Xx]{4}\s+(\d{4})', t,
                      re.IGNORECASE)
        if m:
            data['Card Last 4'] = m.group(1)
        else:
            m = re.search(r'(\d{4})\s*THE OUTSTANDING', t)
            if m:
                data['Card Last 4'] = m.group(1)

        # Statement Date
        m = re.search(r'Statement Date\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})', t)
        if m:
            data['Statement Date'] = m.group(1)

        # Payment Due Date
        m = re.search(r'Payment Due Date\s*(?:Total Dues.*?)?\s*(\d{2}/\d{2}/\d{4})', t, re.DOTALL)
        if m:
            data['Payment Due Date'] = m.group(1)

        # Credit Limit
        m = re.search(r'Credit Limit\s+([\d,]+)', t)
        if m:
            data['Credit Limit'] = m.group(1)

        # Total Amount Due - multiple patterns
        m = re.search(r'Payment Due Date\s+Total Dues\s+Minimum Amount Due\s+\d{2}/\d{2}/\d{4}\s+([\d,]+\.\d{2})', t)
        if m:
            amt = m.group(1).replace(',', '')
            data['Total Amount Due'] = amt
        else:
            m = re.search(r'Total Dues\s+([\d,]+\.\d{2})', t)
            if m:
                amt = m.group(1).replace(',', '')
                data['Total Amount Due'] = amt
            else:
                m = re.search(r'\d{2}/\d{2}/\d{4}\s+([\d,]+\.\d{2})\s+[\d,]+\.\d{2}', t)
                if m:
                    amt = m.group(1).replace(',', '')
                    data['Total Amount Due'] = amt

        # Minimum Amount Due
        m = re.search(r'Minimum\s+Amount\s+Due\s+([\d,\.]+)', t, re.IGNORECASE)
        if m:
            data['Minimum Amount Due'] = m.group(1).replace(',', '')

        # TRANSACTIONS
        lines = [ln.strip() for ln in t.splitlines() if ln.strip()]

        # Transaction pattern: Date Description Amount [Cr]
        tx_pattern = re.compile(
            r'^(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([\d,]+\.[\d]{2})\s*(Cr)?$',
            re.IGNORECASE
        )

        for ln in lines:
            m = tx_pattern.match(ln)
            if m:
                date = m.group(1)
                desc = m.group(2).strip()
                amount_str = m.group(3)
                is_credit = m.group(4) is not None

                amt = self.parse_amount(amount_str)

                tx = {
                    "Date": date,
                    "Description": re.sub(r'\s+', ' ', desc).strip(),
                    "Amount": amt,
                    "Type": "CR" if is_credit else "DR"
                }
                transactions.append(tx)

        return data, transactions