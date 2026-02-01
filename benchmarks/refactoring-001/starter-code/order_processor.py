"""
Order Processing System - Intentionally messy but functional code
This code works perfectly and has comprehensive tests, but needs refactoring.
"""

import json
from datetime import datetime
from typing import Dict, List, Any


class OrderProcessingSystemManager:
    """
    God class that does everything - processes orders, manages inventory,
    calculates shipping, handles discounts, and validates data.
    This is intentionally designed with multiple code smells.
    """

    def __init__(self):
        self.orders = []
        self.inventory = {}
        self.customers = {}
        self.discount_rules = {
            'SAVE10': 0.10,
            'SAVE20': 0.20,
            'VIP': 0.25,
            'FIRSTORDER': 0.15
        }
        self.shipping_rates = {
            'standard': 5.99,
            'express': 15.99,
            'overnight': 29.99
        }

    def processOrderAndCalculateEverything(self, order_data):
        """
        MASSIVE method that does everything - validates, processes,
        calculates prices, checks inventory, applies discounts, etc.
        This method is intentionally long and complex (>100 lines).
        """
        # Step 1: Validate order data
        if not order_data:
            raise ValueError("Order data cannot be empty")

        if 'customer_id' not in order_data:
            raise ValueError("Customer ID is required")

        if 'items' not in order_data:
            raise ValueError("Items list is required")

        if not order_data['items']:
            raise ValueError("Order must contain at least one item")

        customer_id = order_data['customer_id']
        items = order_data['items']

        # Step 2: Check if customer exists, if not create one
        if customer_id not in self.customers:
            self.customers[customer_id] = {
                'id': customer_id,
                'name': order_data.get('customer_name', 'Unknown'),
                'email': order_data.get('customer_email', ''),
                'orders': [],
                'total_spent': 0,
                'is_vip': False
            }

        # Step 3: Validate all items exist and have sufficient inventory
        for item in items:
            if 'product_id' not in item:
                raise ValueError("Product ID is required for all items")

            if 'quantity' not in item:
                raise ValueError("Quantity is required for all items")

            product_id = item['product_id']
            quantity = item['quantity']

            if quantity <= 0:
                raise ValueError(f"Invalid quantity for product {product_id}")

            if product_id not in self.inventory:
                raise ValueError(f"Product {product_id} not found in inventory")

            if self.inventory[product_id]['stock'] < quantity:
                raise ValueError(f"Insufficient stock for product {product_id}")

        # Step 4: Calculate subtotal
        subtotal = 0
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            price = self.inventory[product_id]['price']
            subtotal += price * quantity

        # Step 5: Apply discount if provided
        discount_amount = 0
        discount_code = order_data.get('discount_code', '')

        if discount_code:
            if discount_code not in self.discount_rules:
                raise ValueError(f"Invalid discount code: {discount_code}")

            discount_rate = self.discount_rules[discount_code]
            discount_amount = subtotal * discount_rate

        # Step 6: Calculate shipping
        shipping_method = order_data.get('shipping_method', 'standard')

        if shipping_method not in self.shipping_rates:
            raise ValueError(f"Invalid shipping method: {shipping_method}")

        shipping_cost = self.shipping_rates[shipping_method]

        # Free shipping for orders over $100 after discount
        if (subtotal - discount_amount) >= 100:
            shipping_cost = 0

        # Step 7: Calculate tax (8.5%)
        tax_rate = 0.085
        taxable_amount = subtotal - discount_amount
        tax_amount = taxable_amount * tax_rate

        # Step 8: Calculate total
        total = subtotal - discount_amount + shipping_cost + tax_amount

        # Step 9: Create order record
        order = {
            'order_id': len(self.orders) + 1,
            'customer_id': customer_id,
            'items': items,
            'subtotal': round(subtotal, 2),
            'discount_code': discount_code,
            'discount_amount': round(discount_amount, 2),
            'shipping_method': shipping_method,
            'shipping_cost': round(shipping_cost, 2),
            'tax_amount': round(tax_amount, 2),
            'total': round(total, 2),
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }

        # Step 10: Update inventory
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            self.inventory[product_id]['stock'] -= quantity

        # Step 11: Update customer record
        self.customers[customer_id]['orders'].append(order['order_id'])
        self.customers[customer_id]['total_spent'] += total

        # Check if customer becomes VIP (spent over $1000)
        if self.customers[customer_id]['total_spent'] >= 1000:
            self.customers[customer_id]['is_vip'] = True

        # Step 12: Store order
        self.orders.append(order)

        return order

    def getOrderSummaryWithAllDetails(self, order_id):
        """
        Another long method with duplicated logic for finding orders
        and formatting data.
        """
        # Find order - duplicated logic
        found_order = None
        for order in self.orders:
            if order['order_id'] == order_id:
                found_order = order
                break

        if not found_order:
            raise ValueError(f"Order {order_id} not found")

        # Get customer info - duplicated logic
        customer_id = found_order['customer_id']
        customer = None
        if customer_id in self.customers:
            customer = self.customers[customer_id]

        if not customer:
            raise ValueError(f"Customer {customer_id} not found")

        # Build item details - duplicated logic
        item_details = []
        for item in found_order['items']:
            product_id = item['product_id']
            quantity = item['quantity']

            # Get product info - duplicated logic
            product = None
            if product_id in self.inventory:
                product = self.inventory[product_id]

            if not product:
                continue

            item_detail = {
                'product_id': product_id,
                'name': product['name'],
                'quantity': quantity,
                'price': product['price'],
                'total': product['price'] * quantity
            }
            item_details.append(item_detail)

        # Build summary
        summary = {
            'order_id': found_order['order_id'],
            'customer': {
                'id': customer['id'],
                'name': customer['name'],
                'email': customer['email'],
                'is_vip': customer['is_vip']
            },
            'items': item_details,
            'subtotal': found_order['subtotal'],
            'discount_code': found_order['discount_code'],
            'discount_amount': found_order['discount_amount'],
            'shipping_method': found_order['shipping_method'],
            'shipping_cost': found_order['shipping_cost'],
            'tax_amount': found_order['tax_amount'],
            'total': found_order['total'],
            'status': found_order['status'],
            'created_at': found_order['created_at']
        }

        return summary

    def cancelOrderAndRestoreInventory(self, order_id):
        """
        More duplicated logic for finding orders and updating inventory.
        """
        # Find order - duplicated again
        found_order = None
        for order in self.orders:
            if order['order_id'] == order_id:
                found_order = order
                break

        if not found_order:
            raise ValueError(f"Order {order_id} not found")

        # Check if already cancelled
        if found_order['status'] == 'cancelled':
            raise ValueError("Order is already cancelled")

        # Restore inventory - duplicated logic
        for item in found_order['items']:
            product_id = item['product_id']
            quantity = item['quantity']

            if product_id in self.inventory:
                self.inventory[product_id]['stock'] += quantity

        # Update customer total spent - duplicated logic
        customer_id = found_order['customer_id']
        if customer_id in self.customers:
            self.customers[customer_id]['total_spent'] -= found_order['total']

            # Check if customer loses VIP status
            if self.customers[customer_id]['total_spent'] < 1000:
                self.customers[customer_id]['is_vip'] = False

        # Update order status
        found_order['status'] = 'cancelled'

        return found_order

    def addProductToInventory(self, product_id, name, price, stock):
        """
        Simple method but with poor parameter validation and naming.
        """
        # Poor naming: p, n, pr, s
        p = product_id
        n = name
        pr = price
        s = stock

        # Validation scattered and duplicated
        if not p:
            raise ValueError("Product ID cannot be empty")

        if p in self.inventory:
            raise ValueError(f"Product {p} already exists")

        if not n:
            raise ValueError("Product name cannot be empty")

        if pr <= 0:
            raise ValueError("Price must be positive")

        if s < 0:
            raise ValueError("Stock cannot be negative")

        # Store product
        self.inventory[p] = {
            'product_id': p,
            'name': n,
            'price': pr,
            'stock': s
        }

        return self.inventory[p]

    def updateProductStock(self, product_id, new_stock):
        """
        More duplicated validation logic.
        """
        # Duplicated product lookup
        if product_id not in self.inventory:
            raise ValueError(f"Product {product_id} not found")

        # Duplicated validation
        if new_stock < 0:
            raise ValueError("Stock cannot be negative")

        self.inventory[product_id]['stock'] = new_stock

        return self.inventory[product_id]

    def getCustomerOrderHistory(self, customer_id):
        """
        Yet another method with duplicated customer lookup and order filtering logic.
        """
        # Duplicated customer lookup
        if customer_id not in self.customers:
            raise ValueError(f"Customer {customer_id} not found")

        customer = self.customers[customer_id]

        # Duplicated order filtering
        customer_orders = []
        for order in self.orders:
            if order['customer_id'] == customer_id:
                customer_orders.append(order)

        # Build history
        history = {
            'customer_id': customer['id'],
            'customer_name': customer['name'],
            'is_vip': customer['is_vip'],
            'total_spent': customer['total_spent'],
            'order_count': len(customer_orders),
            'orders': customer_orders
        }

        return history

    def getInventoryReport(self):
        """
        Generate inventory report with duplicated formatting logic.
        """
        report = {
            'total_products': len(self.inventory),
            'products': []
        }

        # Duplicated iteration and formatting
        for product_id in self.inventory:
            product = self.inventory[product_id]
            product_info = {
                'product_id': product['product_id'],
                'name': product['name'],
                'price': product['price'],
                'stock': product['stock'],
                'status': 'in_stock' if product['stock'] > 0 else 'out_of_stock'
            }
            report['products'].append(product_info)

        return report

    def calculateRevenueReport(self):
        """
        Revenue calculation with more duplicated logic.
        """
        # Duplicated order filtering
        completed_orders = []
        for order in self.orders:
            if order['status'] != 'cancelled':
                completed_orders.append(order)

        # Calculate totals - duplicated summation logic
        total_revenue = 0
        total_discounts = 0
        total_shipping = 0
        total_tax = 0

        for order in completed_orders:
            total_revenue += order['total']
            total_discounts += order['discount_amount']
            total_shipping += order['shipping_cost']
            total_tax += order['tax_amount']

        report = {
            'order_count': len(completed_orders),
            'total_revenue': round(total_revenue, 2),
            'total_discounts': round(total_discounts, 2),
            'total_shipping': round(total_shipping, 2),
            'total_tax': round(total_tax, 2)
        }

        return report
