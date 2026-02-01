from datetime import datetime
import hashlib
import random

class PaymentGateway:
    def __init__(self, api_key):
        self.api_key = api_key
        self.test_mode = api_key.startswith("test_")
        self._transaction_log = []

    def charge(self, amount, payment_method, metadata=None):
        if amount <= 0:
            raise ValueError("Amount must be positive")

        transaction_id = self._generate_transaction_id()

        if self.test_mode:
            if payment_method.get('number', '').endswith('0000'):
                return {'success': False, 'error': 'CARD_DECLINED', 'transaction_id': transaction_id}
            success = True
        else:
            success = self._process_real_charge(amount, payment_method)

        result = {
            'success': success,
            'transaction_id': transaction_id,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }

        if metadata:
            result['metadata'] = metadata

        self._transaction_log.append(result)
        return result

    def _generate_transaction_id(self):
        timestamp = str(datetime.now().timestamp())
        random_str = str(random.randint(10000, 99999))
        hash_input = f"{self.api_key}{timestamp}{random_str}"
        return "TXN_" + hashlib.md5(hash_input.encode()).hexdigest()[:12].upper()

    def _process_real_charge(self, amount, payment_method):
        return True

    def refund(self, transaction_id, amount=None):
        original = None
        for txn in self._transaction_log:
            if txn.get('transaction_id') == transaction_id:
                original = txn
                break

        if not original:
            return {'success': False, 'error': 'TRANSACTION_NOT_FOUND'}

        if not original.get('success'):
            return {'success': False, 'error': 'CANNOT_REFUND_FAILED_TRANSACTION'}

        refund_amount = amount if amount else original['amount']
        if refund_amount > original['amount']:
            return {'success': False, 'error': 'REFUND_EXCEEDS_ORIGINAL'}

        refund_id = self._generate_transaction_id()
        result = {
            'success': True,
            'refund_id': refund_id,
            'transaction_id': transaction_id,
            'amount': refund_amount,
            'timestamp': datetime.now().isoformat()
        }

        self._transaction_log.append(result)
        return result

class PaymentProcessor:
    def __init__(self, gateway, invoice_db):
        self.gateway = gateway
        self.invoice_db = invoice_db
        self.retry_attempts = 3
        self.retry_delay = 5

    def process_invoice_payment(self, invoice_id, payment_method):
        invoice = self.invoice_db.get_invoice(invoice_id)
        if not invoice:
            return {'success': False, 'error': 'INVOICE_NOT_FOUND'}

        if invoice.status != invoice.STATUS_APPROVED:
            return {'success': False, 'error': 'INVOICE_NOT_APPROVED'}

        amount = invoice.get_total()

        metadata = {
            'invoice_id': invoice_id,
            'customer_id': invoice.customer_id
        }

        for attempt in range(self.retry_attempts):
            result = self.gateway.charge(amount, payment_method, metadata)

            if result['success']:
                invoice.mark_paid(result['transaction_id'])
                self.invoice_db.save_invoice(invoice)
                return {
                    'success': True,
                    'transaction_id': result['transaction_id'],
                    'amount': amount,
                    'invoice_id': invoice_id
                }

            if result.get('error') == 'CARD_DECLINED':
                break

        return {'success': False, 'error': result.get('error', 'PAYMENT_FAILED')}

    def process_refund(self, invoice_id, amount=None):
        invoice = self.invoice_db.get_invoice(invoice_id)
        if not invoice:
            return {'success': False, 'error': 'INVOICE_NOT_FOUND'}

        if invoice.status != invoice.STATUS_PAID:
            return {'success': False, 'error': 'INVOICE_NOT_PAID'}

        payment_id = invoice.metadata.get('payment_id')
        if not payment_id:
            return {'success': False, 'error': 'NO_PAYMENT_RECORD'}

        refund_result = self.gateway.refund(payment_id, amount)

        if refund_result['success']:
            invoice.metadata['refund_id'] = refund_result['refund_id']
            invoice.metadata['refund_amount'] = refund_result['amount']
            invoice.metadata['refund_date'] = refund_result['timestamp']
            self.invoice_db.save_invoice(invoice)

        return refund_result

    def process_batch_payments(self, payment_batch):
        results = []
        for batch_item in payment_batch:
            invoice_id = batch_item['invoice_id']
            payment_method = batch_item['payment_method']
            result = self.process_invoice_payment(invoice_id, payment_method)
            results.append({
                'invoice_id': invoice_id,
                'result': result
            })

        successful = sum(1 for r in results if r['result']['success'])
        return {
            'total': len(results),
            'successful': successful,
            'failed': len(results) - successful,
            'details': results
        }
