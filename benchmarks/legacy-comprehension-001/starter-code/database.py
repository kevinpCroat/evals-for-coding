import json
import os
from datetime import datetime

class InvoiceDatabase:
    def __init__(self, data_dir="./data"):
        self.data_dir = data_dir
        self._cache = {}
        self._cache_enabled = True
        self.auto_increment_id = 1000

    def _get_filepath(self, invoice_id):
        return os.path.join(self.data_dir, f"invoice_{invoice_id}.json")

    def _serialize_invoice(self, invoice):
        data = invoice.to_dict()
        items_data = []
        for item in invoice.items:
            items_data.append({
                'description': item.description,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'tax_code': item.tax_code,
                'discount': item._discount
            })
        data['items_detail'] = items_data
        data['payment_terms'] = invoice.payment_terms
        return data

    def _deserialize_invoice(self, data):
        from invoice import Invoice, InvoiceItem
        inv = Invoice(
            data['id'],
            data['customer_id'],
            datetime.fromisoformat(data['created_date'])
        )
        inv.status = data['status']
        inv.payment_terms = data.get('payment_terms', 30)
        if data.get('due_date'):
            inv.due_date = datetime.fromisoformat(data['due_date'])
        inv.metadata = data.get('metadata', {})

        for item_data in data.get('items_detail', []):
            item = InvoiceItem(
                item_data['description'],
                item_data['quantity'],
                item_data['unit_price'],
                item_data.get('tax_code', 'STD')
            )
            if 'discount' in item_data:
                item._discount = item_data['discount']
            inv.add_item(item)

        return inv

    def save_invoice(self, invoice):
        if self._cache_enabled:
            self._cache[invoice.id] = invoice

        data = self._serialize_invoice(invoice)
        filepath = self._get_filepath(invoice.id)

        os.makedirs(self.data_dir, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return True

    def get_invoice(self, invoice_id):
        if self._cache_enabled and invoice_id in self._cache:
            return self._cache[invoice_id]

        filepath = self._get_filepath(invoice_id)
        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r') as f:
            data = json.load(f)

        invoice = self._deserialize_invoice(data)

        if self._cache_enabled:
            self._cache[invoice_id] = invoice

        return invoice

    def delete_invoice(self, invoice_id):
        if invoice_id in self._cache:
            del self._cache[invoice_id]

        filepath = self._get_filepath(invoice_id)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def list_invoices(self, customer_id=None, status=None):
        if not os.path.exists(self.data_dir):
            return []

        invoices = []
        for filename in os.listdir(self.data_dir):
            if filename.startswith("invoice_") and filename.endswith(".json"):
                invoice_id = filename.replace("invoice_", "").replace(".json", "")
                invoice = self.get_invoice(invoice_id)
                if invoice:
                    if customer_id and invoice.customer_id != customer_id:
                        continue
                    if status and invoice.status != status:
                        continue
                    invoices.append(invoice)

        return invoices

    def get_next_invoice_id(self):
        invoice_id = f"INV-{self.auto_increment_id:06d}"
        self.auto_increment_id += 1
        return invoice_id

    def clear_cache(self):
        self._cache = {}

class CustomerDatabase:
    def __init__(self):
        self._customers = {}

    def add_customer(self, customer_id, customer_data):
        self._customers[customer_id] = customer_data

    def get_customer(self, customer_id):
        return self._customers.get(customer_id)

    def update_customer(self, customer_id, updates):
        if customer_id in self._customers:
            self._customers[customer_id].update(updates)
            return True
        return False

    def delete_customer(self, customer_id):
        if customer_id in self._customers:
            del self._customers[customer_id]
            return True
        return False

    def search_customers(self, **criteria):
        results = []
        for customer_id, customer_data in self._customers.items():
            match = True
            for key, value in criteria.items():
                if customer_data.get(key) != value:
                    match = False
                    break
            if match:
                results.append({'id': customer_id, **customer_data})
        return results

    def get_all_customers(self):
        return [{'id': cid, **cdata} for cid, cdata in self._customers.items()]
