import re
from typing import List, Dict, Optional, Tuple


class CreditCardParser:
    """Unified parser for ICICI and Axis credit card statements"""

    def __init__(self):
        # Common regex patterns for credit card statements
        self.patterns = {
            'bank_name': [
                r'(ICICI\s+Bank|Axis\s+Bank)',
            ],
            'card_name': [
                r'Card\s+([A-Za-z\s]+?)\s*\(',
                r'Card\s+Name\s*:\s*([A-Za-z\s]+?)(?=\n|Card)',
            ],
            'card_last4': [
                r'XXXX-XXXX-XXXX-(\d{4})',
                r'Card.*?(\d{4})',
            ],
            'statement_date': [
                r'Statement Date\s+(\d{2}\s+\w+\s+\d{4})',
                r'Statement\s+Date\s*:\s*(\d{1,2}\s+\w+\s+\d{4})',
            ],
            'statement_period': [
                r'Statement Period\s+(\d{2}\s+\w+\s+\d{4})\s*-\s*(\d{2}\s+\w+\s+\d{4})',
                r'(\d{1,2}\s+\w+\s+\d{4})\s+to\s+(\d{1,2}\s+\w+\s+\d{4})',
            ],
            'payment_due_date': [
                r'Payment Due Date\s+(\d{2}\s+\w+\s+\d{4})',
                r'Due Date\s*:\s*(\d{1,2}\s+\w+\s+\d{4})',
            ],
            'total_amount_due': [
                r'Total Amount Due\s+INR\s+([\d,]+\.?\d*)',
                r'Total\s+Amount\s+Due\s*:\s*₹?\s*([\d,]+\.?\d*)',
            ],
            'minimum_amount_due': [
                r'Minimum Amount Due\s+INR\s+([\d,]+\.?\d*)',
                r'Minimum\s+Amount\s+Due\s*:\s*₹?\s*([\d,]+\.?\d*)',
            ],
            'previous_balance': [
                r'Previous Balance\s+INR\s+([-\d,]+\.?\d*)',
                r'Previous\s+Balance\s*:\s*₹?\s*([-\d,]+\.?\d*)',
            ],
            'payment_received': [
                r'Payment Received\s+\((\d{2}-\w+-\d{4})\)\s+([-\d,]+\.?\d*)',
            ],
            'new_charges': [
                r'New Charges\s+INR\s+([\d,]+\.?\d*)',
                r'New\s+Charges\s*:\s*₹?\s*([\d,]+\.?\d*)',
            ],
            'statement_balance': [
                r'Statement Balance\s+INR\s+([\d,]+\.?\d*)',
                r'Statement\s+Balance\s*:\s*₹?\s*([\d,]+\.?\d*)',
            ],
        }

    def clean_text(self, text: str) -> str:
        """Clean text by removing encoding issues"""
        # Remove (cid:X) patterns
        text = re.sub(r'\(cid:\d+\)', '', text)
        # Clean up multiple whitespace but preserve newlines
        lines = text.split('\n')
        cleaned_lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in lines]
        return '\n'.join(cleaned_lines)

    def detect_bank(self, text: str) -> str:
        """Detect which bank the statement is from"""
        if 'ICICI Bank' in text:
            return 'ICICI'
        elif 'Axis Bank' in text:
            return 'Axis'
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
                # Remove comma and convert to float
                amount_str = amount_str.replace(',', '').replace('₹', '').strip()
                return float(amount_str)
            except ValueError:
                pass
        return None

    def extract_transactions(self, text: str) -> List[Dict]:
        """Extract transaction details from the statement"""
        transactions = []
        lines = text.split('\n')

        # Transaction line pattern: Date Type Description Debit(INR) Credit(INR)
        # Example: 03-Sep-2025 DEBIT RESTAURANT 124,820.23
        date_pattern = r'^(\d{2}-\w+-\d{4})\s+(DEBIT|CREDIT)\s+([A-Z\s]+?)\s+([\d,]+\.?\d*)\s*$'

        for line in lines:
            line = line.strip()

            # Skip empty lines and headers
            if not line or len(line) < 15:
                continue

            # Skip common headers and footers
            skip_keywords = ['Date', 'Type', 'Description', 'Debit', 'Credit',
                             'EMI', 'interest', 'page', 'statement', 'synthetic',
                             'testing', 'detailed transactions', 'account summary']

            if any(keyword.lower() in line.lower() for keyword in skip_keywords):
                continue

            # Try to match transaction pattern
            match = re.match(date_pattern, line, re.IGNORECASE)

            if match:
                try:
                    date_str = match.group(1)
                    txn_type = match.group(2).upper()
                    description = match.group(3).strip()
                    amount_str = match.group(4).replace(',', '')
                    amount = float(amount_str)

                    transactions.append({
                        'Date': date_str,
                        'Type': txn_type,
                        'Description': description,
                        'Amount': round(amount, 2)
                    })

                except (ValueError, IndexError):
                    continue

        return transactions

    def calculate_summary(self, transactions: List[Dict]) -> Dict:
        """Calculate transaction summary"""
        total_debits = sum(t['Amount'] for t in transactions if t['Type'] == 'DEBIT')
        total_credits = sum(t['Amount'] for t in transactions if t['Type'] == 'CREDIT')

        return {
            'Total Debits': round(total_debits, 2),
            'Total Credits': round(total_credits, 2),
            'Transaction Count': len(transactions)
        }

    def parse(self, text: str) -> Tuple[Dict, List[Dict]]:
        """
        Main parsing function for credit card statements

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

        # Extract key data points
        card_name = self.extract_field(text, 'card_name')
        if card_name:
            data['Card Name'] = card_name.strip()

        card_last4 = self.extract_field(text, 'card_last4')
        if card_last4:
            data['Card Last 4'] = card_last4

        statement_date = self.extract_field(text, 'statement_date')
        if statement_date:
            data['Statement Date'] = statement_date

        statement_period = self.extract_field(text, 'statement_period')
        if statement_period:
            data['Statement Period'] = statement_period

        payment_due_date = self.extract_field(text, 'payment_due_date')
        if payment_due_date:
            data['Payment Due Date'] = payment_due_date

        # Extract amounts
        total_due = self.extract_amount(text, 'total_amount_due')
        if total_due is not None:
            data['Total Amount Due'] = total_due

        min_due = self.extract_amount(text, 'minimum_amount_due')
        if min_due is not None:
            data['Minimum Amount Due'] = min_due

        prev_balance = self.extract_amount(text, 'previous_balance')
        if prev_balance is not None:
            data['Previous Balance'] = prev_balance

        new_charges = self.extract_amount(text, 'new_charges')
        if new_charges is not None:
            data['New Charges'] = new_charges

        stmt_balance = self.extract_amount(text, 'statement_balance')
        if stmt_balance is not None:
            data['Statement Balance'] = stmt_balance

        # Extract transactions
        transactions = self.extract_transactions(text)
        data['Transactions Count'] = len(transactions)

        # Calculate summary
        if transactions:
            summary = self.calculate_summary(transactions)
            data.update(summary)

        return data, transactions