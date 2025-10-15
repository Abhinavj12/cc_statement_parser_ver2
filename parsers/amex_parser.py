import re
from typing import List, Dict, Optional, Tuple


class AMEXParser:
    """Parser for American Express credit card statements"""

    def __init__(self):
        self.patterns = {
            'member_name': [
                r'Member Name\s*:\s*(.+?)(?=\n|Account)',
            ],
            'account_number': [
                r'Account number ending in\s+(\d{4})',
                r'Account\s*:\s*\*+(\d{4})',
            ],
            'statement_period': [
                r'Period\s*:\s*(\w+\s+\d{1,2},?\s+\d{4})\s*-\s*(\w+\s+\d{1,2},?\s+\d{4})',
            ],
            'due_date': [
                r'Due Date\s*:\s*(\w+\s+\d{1,2},?\s+\d{4})',
            ],
            'amount_due': [
                r'Amount Due\s*:\s*\$?([\d,]+\.?\d*)',
                r'Amount Due\s*:\s*([\d,]+\.?\d*)',
            ],
            'previous_balance': [
                r'Previous Balance\s*:\s*\$?([-\d,]+\.?\d*)',
            ],
            'payments': [
                r'Payments\s*:\s*\$?([-\d,]+\.?\d*)',
            ],
            'new_charges': [
                r'New Charges\s*:\s*\$?([\d,]+\.?\d*)',
            ],
        }

    def clean_text(self, text: str) -> str:
        """Clean text by removing encoding issues"""
        text = re.sub(r'\(cid:\d+\)', '', text)
        lines = text.split('\n')
        cleaned_lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in lines]
        return '\n'.join(cleaned_lines)

    def detect_bank(self, text: str) -> str:
        """Detect if this is an AMEX statement"""
        if 'American Express' in text or 'AMEX' in text:
            return 'AMEX'
        return 'Unknown'

    def extract_field(self, text: str, field_name: str) -> Optional[str]:
        """Extract a field using regex patterns"""
        patterns = self.patterns.get(field_name, [])
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def extract_amount(self, text: str, field_name: str) -> Optional[float]:
        """Extract and convert amount to float"""
        amount_str = self.extract_field(text, field_name)
        if amount_str:
            try:
                amount_str = amount_str.replace(',', '').replace('$', '').strip()
                return float(amount_str)
            except ValueError:
                pass
        return None

    def extract_transactions(self, text: str) -> List[Dict]:
        """Extract transaction details from AMEX statement"""
        transactions = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()

            # Skip empty lines and headers
            if not line or len(line) < 15:
                continue

            # Skip common headers and footers
            skip_keywords = ['Transactions', 'Date', 'Description', 'Amount',
                             'Member Name', 'Account number', 'Period', 'Due Date',
                             'Amount Due', 'Previous Balance', 'Payments', 'New Charges',
                             'American Express', 'AMEX', 'Summary', 'Page']

            if any(keyword in line for keyword in skip_keywords):
                continue

            # Pattern for AMEX: DD-Mon-YYYY DESCRIPTION AMOUNT
            # Example: 15-Aug-2025 STARBUCKS 15.67
            # Also handles: DD/MM/YYYY DESCRIPTION $15.67
            pattern = r'^(\d{1,2}[-/]\w{3}[-/]\d{4})\s+(.+?)\s+(\$?[\d,]+\.?\d+)\s*$'
            match = re.match(pattern, line, re.IGNORECASE)

            if match:
                try:
                    date_str = match.group(1)
                    description = match.group(2).strip()
                    amount_str = match.group(3).replace(',', '').replace('$', '')
                    amount = float(amount_str)

                    transactions.append({
                        'Date': date_str,
                        'Description': description,
                        'Amount': round(amount, 2),
                        'Type': 'DEBIT'  # AMEX typically shows all as debits
                    })

                except (ValueError, IndexError):
                    continue

        return transactions

    def calculate_summary(self, transactions: List[Dict]) -> Dict:
        """Calculate transaction summary"""
        total_amount = sum(t['Amount'] for t in transactions)

        return {
            'Total Transactions': len(transactions),
            'Total Amount': round(total_amount, 2)
        }

    def parse(self, text: str) -> Tuple[Dict, List[Dict]]:
        """
        Main parsing function for AMEX statements

        Args:
            text: Extracted text from PDF

        Returns:
            Tuple of (summary_dict, transactions_list)
        """
        data = {}

        # Clean the text first
        text = self.clean_text(text)

        # Detect bank
        bank = self.detect_bank(text)
        data['Bank'] = bank

        # Extract member information
        member_name = self.extract_field(text, 'member_name')
        if member_name:
            data['Member Name'] = member_name

        account_number = self.extract_field(text, 'account_number')
        if account_number:
            data['Account Number'] = f"****{account_number}"

        # Extract statement period
        statement_period = self.extract_field(text, 'statement_period')
        if statement_period:
            data['Statement Period'] = statement_period

        due_date = self.extract_field(text, 'due_date')
        if due_date:
            data['Due Date'] = due_date

        # Extract amounts
        amount_due = self.extract_amount(text, 'amount_due')
        if amount_due is not None:
            data['Amount Due'] = amount_due

        prev_balance = self.extract_amount(text, 'previous_balance')
        if prev_balance is not None:
            data['Previous Balance'] = prev_balance

        payments = self.extract_amount(text, 'payments')
        if payments is not None:
            data['Payments'] = payments

        new_charges = self.extract_amount(text, 'new_charges')
        if new_charges is not None:
            data['New Charges'] = new_charges

        # Extract transactions
        transactions = self.extract_transactions(text)
        data['Transactions Count'] = len(transactions)

        # Calculate summary
        if transactions:
            summary = self.calculate_summary(transactions)
            data.update(summary)

        return data, transactions