import re
from typing import List, Dict, Optional, Tuple


class SBIParser:
    """Parser specifically for SBI bank statements"""

    def __init__(self):
        # Regex patterns for SBI statements
        self.patterns = {
            'account_number': [
                r'Account Number\s*:\s*(\d+)',
                r'A/c\s*No\s*[:\.]?\s*(\d+)',
                r'Account\s*No\s*[:\.]?\s*(\d+)',
            ],
            'account_holder': [
                r'Account Holder\s*:\s*(.+?)(?=\n|Account)',
                r'Account Name\s*:\s*(.+?)(?=\n|Address)',
                r'(?:Mr\.|Mrs\.|Ms\.)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            ],
            'branch': [
                r'Branch\s*:\s*([A-Z][A-Z\s]+?)(?=\s+Drawing|\s+Power|\s+Interest|\s+MOD|\s+Balance)',
                r'Branch\s*:\s*([^:\n]+?)(?=\s+Drawing|\s+Power)',
                r'Branch\s*[:\-]\s*(.+?)(?=\n)',
            ],
            'statement_period': [
                r'Statement Period\s*:\s*(\d+\s+\w+\s+\d+)\s+to\s+(\d+\s+\w+\s+\d+)',
                r'(\d+\s+\w+\s+\d+)\s+to\s+(\d+\s+\w+\s+\d+)',
                r'from\s+(\d{2}\s+\w{3}\s+\d{4})\s+to\s+(\d{2}\s+\w{3}\s+\d{4})',
            ],
            'opening_balance': [
                r'Opening Balance\s*:\s*₹?\s*([\d,]+\.?\d*)',
                r'Balance as on\s+\d+\s+\w+\s+\d+\s*:\s*₹?\s*([\d,]+\.?\d*)',
                r'Balance\s+as\s+on\s+\d+\s+\w+\s+\d+\s*:\s*([\d,]+\.?\d*)',
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

    def extract_account_number(self, text: str) -> Optional[str]:
        """Extract account number"""
        for pattern in self.patterns['account_number']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def extract_account_holder(self, text: str) -> Optional[str]:
        """Extract account holder name"""
        for pattern in self.patterns['account_holder']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Clean up common prefixes
                name = re.sub(r'^(Mr\.?|Mrs\.?|Ms\.?|Dr\.?)\s+', '', name, flags=re.IGNORECASE)
                # Remove extra whitespace
                name = re.sub(r'\s+', ' ', name)
                if len(name) > 3:
                    return name
        return None

    def extract_branch(self, text: str) -> Optional[str]:
        """Extract branch name"""
        for pattern in self.patterns['branch']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                branch = match.group(1).strip()
                # Clean up encoding issues like (cid:9)
                branch = re.sub(r'\(cid:\d+\)', '', branch)
                branch = re.sub(r'\s+', ' ', branch).strip()
                if len(branch) > 2:
                    return branch
        return None

    def extract_statement_period(self, text: str) -> Optional[str]:
        """Extract statement period"""
        for pattern in self.patterns['statement_period']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1).strip()} to {match.group(2).strip()}"
        return None

    def extract_opening_balance(self, text: str) -> Optional[float]:
        """Extract opening balance"""
        for pattern in self.patterns['opening_balance']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                balance_str = match.group(1).replace(',', '').strip()
                try:
                    balance = float(balance_str)
                    return balance
                except ValueError:
                    continue
        return None

    def extract_transactions(self, text: str) -> List[Dict]:
        """Extract transaction details from the statement"""
        transactions = []
        lines = text.split('\n')

        # Month pattern for date matching
        months = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'

        # Look for transaction patterns in each line
        for line in lines:
            line = line.strip()

            # Skip empty lines and headers
            if not line or len(line) < 15:
                continue

            # Skip common headers and footers
            skip_keywords = ['txn date', 'value date', 'particulars', 'description',
                             'withdrawal', 'deposit', 'balance', 'debit', 'credit',
                             'computer generated', 'page ', 'statement', 'branch',
                             'account', 'opening', 'closing', 'total']

            if any(keyword in line.lower() for keyword in skip_keywords):
                continue

            # Pattern 1: DD Mon YYYY format (e.g., "3 May 2018")
            date_pattern1 = rf'^(\d{{1,2}}\s+{months}\s+\d{{4}})'
            match1 = re.match(date_pattern1, line, re.IGNORECASE)

            # Pattern 2: DD/MM/YYYY format
            date_pattern2 = r'^(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
            match2 = re.match(date_pattern2, line)

            date_match = match1 or match2

            if date_match:
                try:
                    date_str = date_match.group(1).strip()
                    remaining = line[len(date_str):].strip()

                    # Try to split by multiple spaces (common in bank statements)
                    parts = re.split(r'\s{2,}', remaining)
                    if len(parts) < 2:
                        parts = remaining.split()

                    # Find numeric values (potential amounts)
                    amounts = []
                    description_parts = []
                    found_first_amount = False

                    for part in parts:
                        # Clean and check if it's a number
                        cleaned = part.replace(',', '').replace('₹', '').replace('Rs.', '').strip()

                        # Check if this looks like an amount
                        if re.match(r'^\d+\.?\d*$', cleaned):
                            try:
                                amount = float(cleaned)
                                if amount > 0:
                                    amounts.append(amount)
                                    found_first_amount = True
                            except:
                                if not found_first_amount:
                                    description_parts.append(part)
                        else:
                            if not found_first_amount:
                                description_parts.append(part)

                    # Need at least one amount (balance)
                    if not amounts:
                        continue

                    # Build description
                    description = ' '.join(description_parts).strip()
                    if not description:
                        description = "Transaction"

                    # Determine transaction type and amounts
                    # Common formats:
                    # 1. Withdrawal | Deposit | Balance (3 amounts)
                    # 2. Amount | Balance (2 amounts)
                    # 3. Just Balance (1 amount - skip these)

                    if len(amounts) >= 3:
                        # Format with 3+ amounts: withdrawal, deposit, balance
                        withdrawal = amounts[0]
                        deposit = amounts[1]
                        balance = amounts[2]

                        if withdrawal > 0 and deposit == 0:
                            txn_type = "Debit"
                            txn_amount = withdrawal
                        elif deposit > 0 and withdrawal == 0:
                            txn_type = "Credit"
                            txn_amount = deposit
                        else:
                            # Use whichever is non-zero
                            txn_type = "Debit" if withdrawal > deposit else "Credit"
                            txn_amount = withdrawal if withdrawal > deposit else deposit

                    elif len(amounts) == 2:
                        # Format with 2 amounts: transaction amount and balance
                        txn_amount = amounts[0]
                        balance = amounts[1]

                        # Determine type from keywords
                        desc_upper = description.upper()
                        if any(kw in desc_upper for kw in ['TO TRANSFER', 'TO', 'WITHDRAWAL',
                                                           'WDL', 'CHARGES', 'PAYMENT',
                                                           'DEBIT', 'ATM', 'POS', 'CHEQUE']):
                            txn_type = "Debit"
                        elif any(kw in desc_upper for kw in ['BY TRANSFER', 'BY', 'DEPOSIT',
                                                             'CREDIT', 'IMPS', 'NEFT',
                                                             'RTGS', 'UPI', 'SALARY']):
                            txn_type = "Credit"
                        else:
                            # Default to debit
                            txn_type = "Debit"
                    else:
                        # Only one amount - likely just balance, skip
                        continue

                    # Add transaction
                    transactions.append({
                        'Date': date_str,
                        'Description': description[:100],
                        'Type': txn_type,
                        'Amount': round(txn_amount, 2),
                        'Balance': round(balance, 2)
                    })

                except Exception as e:
                    # Skip problematic lines
                    continue

        return transactions

    def calculate_summary(self, transactions: List[Dict], opening_balance: Optional[float]) -> Dict:
        """Calculate transaction summary"""
        total_credits = sum(t['Amount'] for t in transactions if t['Type'] == 'Credit')
        total_debits = sum(t['Amount'] for t in transactions if t['Type'] == 'Debit')

        if transactions:
            closing_balance = transactions[-1]['Balance']
        else:
            closing_balance = opening_balance if opening_balance is not None else 0.0

        return {
            'Total Credits': round(total_credits, 2),
            'Total Debits': round(total_debits, 2),
            'Net Change': round(total_credits - total_debits, 2),
            'Closing Balance': round(closing_balance, 2)
        }

    def parse(self, text: str) -> Tuple[Dict, List[Dict]]:
        """
        Main parsing function for SBI statements

        Args:
            text: Extracted text from PDF

        Returns:
            Tuple of (summary_dict, transactions_list)
        """
        data = {}

        # Clean the text first
        text = self.clean_text(text)

        # Extract key data points
        account_number = self.extract_account_number(text)
        account_holder = self.extract_account_holder(text)
        branch = self.extract_branch(text)
        statement_period = self.extract_statement_period(text)
        opening_balance = self.extract_opening_balance(text)

        # Add to data dictionary
        if account_number:
            data['Account Number'] = account_number
        if account_holder:
            data['Account Holder'] = account_holder
        if branch:
            data['Branch'] = branch
        if statement_period:
            data['Statement Period'] = statement_period
        if opening_balance is not None:
            data['Opening Balance'] = opening_balance

        # Extract transactions
        transactions = self.extract_transactions(text)

        # Calculate summary
        if transactions or opening_balance is not None:
            summary = self.calculate_summary(transactions, opening_balance)
            data.update(summary)

        return data, transactions