class TaxCalculator:
    TAX_RATES = {
        'STD': 0.20,
        'REDUCED': 0.05,
        'ZERO': 0.00,
        'EXEMPT': 0.00
    }

    SPECIAL_REGIONS = {
        'EU': {'STD': 0.21, 'REDUCED': 0.06},
        'CA': {'STD': 0.13, 'REDUCED': 0.05},
        'UK': {'STD': 0.20, 'REDUCED': 0.05}
    }

    def __init__(self):
        self.region = None
        self._tax_overrides = {}

    def set_region(self, region_code):
        if region_code in self.SPECIAL_REGIONS:
            self.region = region_code
        else:
            self.region = None

    def add_tax_override(self, customer_id, tax_code, rate):
        if customer_id not in self._tax_overrides:
            self._tax_overrides[customer_id] = {}
        self._tax_overrides[customer_id][tax_code] = rate

    def get_tax_rate(self, tax_code, customer_id=None):
        if customer_id and customer_id in self._tax_overrides:
            if tax_code in self._tax_overrides[customer_id]:
                return self._tax_overrides[customer_id][tax_code]

        if self.region and self.region in self.SPECIAL_REGIONS:
            regional_rates = self.SPECIAL_REGIONS[self.region]
            if tax_code in regional_rates:
                return regional_rates[tax_code]

        if tax_code in self.TAX_RATES:
            return self.TAX_RATES[tax_code]

        return self.TAX_RATES['STD']

    def calculate_item_tax(self, item, customer_id=None):
        rate = self.get_tax_rate(item.tax_code, customer_id)
        return item.get_total() * rate

    def calculate_invoice_tax(self, invoice):
        total_tax = 0
        for item in invoice.items:
            total_tax += self.calculate_item_tax(item, invoice.customer_id)
        return total_tax

    def apply_compound_tax(self, amount, tax_code1, tax_code2, customer_id=None):
        rate1 = self.get_tax_rate(tax_code1, customer_id)
        rate2 = self.get_tax_rate(tax_code2, customer_id)
        tax1 = amount * rate1
        tax2 = (amount + tax1) * rate2
        return tax1 + tax2

class TaxExemptionChecker:
    def __init__(self, customer_db):
        self.customer_db = customer_db

    def is_tax_exempt(self, customer_id):
        customer = self.customer_db.get_customer(customer_id)
        if not customer:
            return False
        return customer.get('tax_exempt', False) or customer.get('tax_id', '').startswith('EX-')

    def get_exemption_reason(self, customer_id):
        customer = self.customer_db.get_customer(customer_id)
        if not customer:
            return None
        if customer.get('tax_exempt'):
            return customer.get('exemption_reason', 'UNKNOWN')
        if customer.get('tax_id', '').startswith('EX-'):
            return 'EXEMPT_TAX_ID'
        return None

    def validate_exemption(self, customer_id, exemption_cert):
        import re
        if not re.match(r'^EXC-\d{6}-[A-Z]{2}$', exemption_cert):
            return False
        customer = self.customer_db.get_customer(customer_id)
        if not customer:
            return False
        stored_cert = customer.get('exemption_cert')
        return stored_cert == exemption_cert
