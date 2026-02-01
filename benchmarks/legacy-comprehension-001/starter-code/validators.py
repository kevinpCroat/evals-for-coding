import re
from datetime import datetime

class InvoiceValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def reset(self):
        self.errors = []
        self.warnings = []

    def validate_invoice(self, invoice):
        self.reset()
        self._validate_basic_fields(invoice)
        self._validate_items(invoice)
        self._validate_amounts(invoice)
        self._validate_dates(invoice)
        self._validate_status_transitions(invoice)

        return len(self.errors) == 0

    def _validate_basic_fields(self, invoice):
        if not invoice.id:
            self.errors.append("Invoice ID is required")

        if not invoice.customer_id:
            self.errors.append("Customer ID is required")

        if not re.match(r'^INV-\d{6}$', invoice.id):
            self.warnings.append("Invoice ID format is non-standard")

    def _validate_items(self, invoice):
        if len(invoice.items) == 0:
            self.warnings.append("Invoice has no items")

        for idx, item in enumerate(invoice.items):
            if item.quantity <= 0:
                self.errors.append(f"Item {idx}: quantity must be positive")

            if item.unit_price < 0:
                self.errors.append(f"Item {idx}: unit price cannot be negative")

            if not item.description or len(item.description.strip()) == 0:
                self.warnings.append(f"Item {idx}: missing description")

    def _validate_amounts(self, invoice):
        subtotal = invoice.get_subtotal()
        if subtotal < 0:
            self.errors.append("Invoice subtotal cannot be negative")

        if subtotal > 1000000:
            self.warnings.append("Invoice amount exceeds $1M - verify accuracy")

        try:
            total = invoice.get_total()
            if total < subtotal:
                self.errors.append("Total is less than subtotal - check tax calculation")
        except Exception as e:
            self.errors.append(f"Error calculating total: {str(e)}")

    def _validate_dates(self, invoice):
        if invoice.created_date > datetime.now():
            self.errors.append("Invoice date cannot be in the future")

        if invoice.due_date:
            if invoice.due_date < invoice.created_date:
                self.errors.append("Due date cannot be before invoice date")

            days_until_due = (invoice.due_date - invoice.created_date).days
            if days_until_due > 365:
                self.warnings.append("Payment terms exceed 1 year")

    def _validate_status_transitions(self, invoice):
        valid_statuses = [
            invoice.STATUS_DRAFT,
            invoice.STATUS_PENDING,
            invoice.STATUS_APPROVED,
            invoice.STATUS_PAID,
            invoice.STATUS_CANCELLED
        ]

        if invoice.status not in valid_statuses:
            self.errors.append(f"Invalid status: {invoice.status}")

    def get_validation_report(self):
        return {
            'valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings)
        }

class PaymentMethodValidator:
    CARD_REGEX = r'^\d{13,19}$'
    CVV_REGEX = r'^\d{3,4}$'
    EXPIRY_REGEX = r'^\d{2}/\d{2}$'

    @staticmethod
    def validate_card_number(card_number):
        card_number = card_number.replace(' ', '').replace('-', '')
        if not re.match(PaymentMethodValidator.CARD_REGEX, card_number):
            return False

        return PaymentMethodValidator._luhn_check(card_number)

    @staticmethod
    def _luhn_check(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0

    @staticmethod
    def validate_cvv(cvv):
        return re.match(PaymentMethodValidator.CVV_REGEX, cvv) is not None

    @staticmethod
    def validate_expiry(expiry):
        if not re.match(PaymentMethodValidator.EXPIRY_REGEX, expiry):
            return False

        month, year = expiry.split('/')
        month = int(month)
        year = int(year) + 2000

        if month < 1 or month > 12:
            return False

        now = datetime.now()
        if year < now.year:
            return False
        if year == now.year and month < now.month:
            return False

        return True

    @staticmethod
    def validate_payment_method(payment_method):
        errors = []

        if 'number' not in payment_method:
            errors.append("Card number is required")
        elif not PaymentMethodValidator.validate_card_number(payment_method['number']):
            errors.append("Invalid card number")

        if 'cvv' not in payment_method:
            errors.append("CVV is required")
        elif not PaymentMethodValidator.validate_cvv(payment_method['cvv']):
            errors.append("Invalid CVV")

        if 'expiry' not in payment_method:
            errors.append("Expiry date is required")
        elif not PaymentMethodValidator.validate_expiry(payment_method['expiry']):
            errors.append("Invalid or expired card")

        return len(errors) == 0, errors
