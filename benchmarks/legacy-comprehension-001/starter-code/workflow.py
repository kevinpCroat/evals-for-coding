from datetime import datetime, timedelta

class InvoiceWorkflow:
    def __init__(self, invoice_db, customer_db):
        self.invoice_db = invoice_db
        self.customer_db = customer_db
        self.approval_rules = []
        self.notification_handlers = []

    def add_approval_rule(self, rule):
        self.approval_rules.append(rule)

    def register_notification_handler(self, handler):
        self.notification_handlers.append(handler)

    def create_invoice(self, customer_id, items, payment_terms=30):
        from invoice import Invoice
        customer = self.customer_db.get_customer(customer_id)
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")

        invoice_id = self.invoice_db.get_next_invoice_id()
        invoice = Invoice(invoice_id, customer_id)
        invoice.set_payment_terms(payment_terms)

        for item in items:
            invoice.add_item(item)

        self.invoice_db.save_invoice(invoice)
        self._notify('invoice_created', invoice)
        return invoice

    def submit_invoice(self, invoice_id, submitted_by):
        invoice = self.invoice_db.get_invoice(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        invoice.submit()
        invoice.metadata['submitted_by'] = submitted_by
        invoice.metadata['submitted_date'] = datetime.now().isoformat()

        self.invoice_db.save_invoice(invoice)
        self._notify('invoice_submitted', invoice)

        if self._should_auto_approve(invoice):
            self.approve_invoice(invoice_id, 'SYSTEM_AUTO')

        return invoice

    def approve_invoice(self, invoice_id, approver_id):
        invoice = self.invoice_db.get_invoice(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        if not self._check_approval_authorization(invoice, approver_id):
            raise PermissionError(f"User {approver_id} not authorized to approve")

        invoice.approve(approver_id)
        self.invoice_db.save_invoice(invoice)
        self._notify('invoice_approved', invoice)
        return invoice

    def reject_invoice(self, invoice_id, rejector_id, reason):
        invoice = self.invoice_db.get_invoice(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice {invoice_id} not found")

        if invoice.status != invoice.STATUS_PENDING:
            raise ValueError("Can only reject pending invoices")

        invoice.status = invoice.STATUS_DRAFT
        invoice.metadata['rejected_by'] = rejector_id
        invoice.metadata['rejected_date'] = datetime.now().isoformat()
        invoice.metadata['rejection_reason'] = reason

        self.invoice_db.save_invoice(invoice)
        self._notify('invoice_rejected', invoice)
        return invoice

    def _should_auto_approve(self, invoice):
        total = invoice.get_total()
        if total < 100:
            return True

        customer = self.customer_db.get_customer(invoice.customer_id)
        if customer and customer.get('trusted', False):
            return True

        return False

    def _check_approval_authorization(self, invoice, approver_id):
        if approver_id == 'SYSTEM_AUTO':
            return True

        total = invoice.get_total()
        if total > 10000 and not approver_id.startswith('MGR-'):
            return False

        return True

    def _notify(self, event_type, invoice):
        for handler in self.notification_handlers:
            try:
                handler(event_type, invoice)
            except Exception:
                pass

    def process_overdue_invoices(self):
        all_invoices = self.invoice_db.list_invoices(status='APPROVED')
        overdue = []

        for invoice in all_invoices:
            if invoice.is_overdue():
                overdue.append(invoice)
                self._notify('invoice_overdue', invoice)

        return overdue

    def bulk_approve(self, invoice_ids, approver_id):
        results = []
        for invoice_id in invoice_ids:
            try:
                invoice = self.approve_invoice(invoice_id, approver_id)
                results.append({'invoice_id': invoice_id, 'success': True})
            except Exception as e:
                results.append({'invoice_id': invoice_id, 'success': False, 'error': str(e)})

        return results

    def generate_invoice_report(self, start_date, end_date, customer_id=None):
        all_invoices = self.invoice_db.list_invoices(customer_id=customer_id)

        filtered = []
        for invoice in all_invoices:
            if start_date <= invoice.created_date <= end_date:
                filtered.append(invoice)

        total_revenue = sum(inv.get_total() for inv in filtered)
        by_status = {}
        for invoice in filtered:
            status = invoice.status
            if status not in by_status:
                by_status[status] = {'count': 0, 'total': 0}
            by_status[status]['count'] += 1
            by_status[status]['total'] += invoice.get_total()

        return {
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'total_invoices': len(filtered),
            'total_revenue': total_revenue,
            'by_status': by_status,
            'invoices': [inv.to_dict() for inv in filtered]
        }
