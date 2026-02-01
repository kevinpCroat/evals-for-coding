from datetime import datetime, timedelta
import re

class InvoiceItem:
    def __init__(self, desc, qty, price, tax_code="STD"):
        self.description = desc
        self.quantity = qty
        self.unit_price = price
        self.tax_code = tax_code
        self._discount = 0

    def set_discount(self, pct):
        if pct < 0 or pct > 100:
            raise ValueError("Discount must be 0-100")
        self._discount = pct

    def get_subtotal(self):
        return self.quantity * self.unit_price

    def get_discount_amount(self):
        return self.get_subtotal() * (self._discount / 100.0)

    def get_total(self):
        return self.get_subtotal() - self.get_discount_amount()

class Invoice:
    STATUS_DRAFT = "DRAFT"
    STATUS_PENDING = "PENDING"
    STATUS_APPROVED = "APPROVED"
    STATUS_PAID = "PAID"
    STATUS_CANCELLED = "CANCELLED"

    def __init__(self, invoice_id, customer_id, created_date=None):
        self.id = invoice_id
        self.customer_id = customer_id
        self.items = []
        self.status = self.STATUS_DRAFT
        self.created_date = created_date or datetime.now()
        self.due_date = None
        self.payment_terms = 30
        self._cached_total = None
        self.metadata = {}

    def add_item(self, item):
        if not isinstance(item, InvoiceItem):
            raise TypeError("Must be InvoiceItem")
        self.items.append(item)
        self._cached_total = None

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]
            self._cached_total = None

    def get_subtotal(self):
        total = 0
        for item in self.items:
            total += item.get_total()
        return total

    def calculate_tax(self):
        from tax_calculator import TaxCalculator
        calc = TaxCalculator()
        return calc.calculate_invoice_tax(self)

    def get_total(self):
        if self._cached_total is not None:
            return self._cached_total
        subtotal = self.get_subtotal()
        tax = self.calculate_tax()
        self._cached_total = subtotal + tax
        return self._cached_total

    def set_payment_terms(self, days):
        self.payment_terms = days
        self.due_date = self.created_date + timedelta(days=days)

    def submit(self):
        if self.status != self.STATUS_DRAFT:
            raise ValueError("Can only submit draft invoices")
        if len(self.items) == 0:
            raise ValueError("Cannot submit empty invoice")
        self.status = self.STATUS_PENDING
        if self.due_date is None:
            self.set_payment_terms(self.payment_terms)

    def approve(self, approver_id):
        if self.status != self.STATUS_PENDING:
            raise ValueError("Can only approve pending invoices")
        self.status = self.STATUS_APPROVED
        self.metadata['approver'] = approver_id
        self.metadata['approved_date'] = datetime.now().isoformat()

    def mark_paid(self, payment_id):
        if self.status != self.STATUS_APPROVED:
            raise ValueError("Can only mark approved invoices as paid")
        self.status = self.STATUS_PAID
        self.metadata['payment_id'] = payment_id
        self.metadata['paid_date'] = datetime.now().isoformat()

    def cancel(self):
        if self.status == self.STATUS_PAID:
            raise ValueError("Cannot cancel paid invoices")
        self.status = self.STATUS_CANCELLED

    def is_overdue(self):
        if self.status in [self.STATUS_PAID, self.STATUS_CANCELLED]:
            return False
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'status': self.status,
            'created_date': self.created_date.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'items': len(self.items),
            'total': self.get_total(),
            'metadata': self.metadata
        }
