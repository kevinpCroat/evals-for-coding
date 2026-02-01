"""
Comprehensive test suite for order processing system.
These tests verify all behavior and MUST continue passing after refactoring.
"""

import pytest
from order_processor import OrderProcessingSystemManager


@pytest.fixture
def processor():
    """Create a fresh order processor for each test."""
    return OrderProcessingSystemManager()


@pytest.fixture
def processor_with_inventory(processor):
    """Create processor with sample inventory."""
    processor.addProductToInventory('WIDGET-001', 'Blue Widget', 25.99, 100)
    processor.addProductToInventory('GADGET-001', 'Red Gadget', 49.99, 50)
    processor.addProductToInventory('TOOL-001', 'Green Tool', 15.99, 75)
    return processor


class TestProductInventoryManagement:
    """Test product and inventory management."""

    def test_add_product_to_inventory(self, processor):
        product = processor.addProductToInventory('PROD-001', 'Test Product', 19.99, 50)

        assert product['product_id'] == 'PROD-001'
        assert product['name'] == 'Test Product'
        assert product['price'] == 19.99
        assert product['stock'] == 50

    def test_add_product_with_zero_stock(self, processor):
        product = processor.addProductToInventory('PROD-002', 'Out of Stock', 9.99, 0)
        assert product['stock'] == 0

    def test_cannot_add_duplicate_product(self, processor):
        processor.addProductToInventory('PROD-001', 'Product 1', 10.00, 10)

        with pytest.raises(ValueError, match="already exists"):
            processor.addProductToInventory('PROD-001', 'Product 2', 20.00, 20)

    def test_cannot_add_product_with_empty_id(self, processor):
        with pytest.raises(ValueError, match="cannot be empty"):
            processor.addProductToInventory('', 'Product', 10.00, 10)

    def test_cannot_add_product_with_empty_name(self, processor):
        with pytest.raises(ValueError, match="cannot be empty"):
            processor.addProductToInventory('PROD-001', '', 10.00, 10)

    def test_cannot_add_product_with_negative_price(self, processor):
        with pytest.raises(ValueError, match="must be positive"):
            processor.addProductToInventory('PROD-001', 'Product', -5.00, 10)

    def test_cannot_add_product_with_zero_price(self, processor):
        with pytest.raises(ValueError, match="must be positive"):
            processor.addProductToInventory('PROD-001', 'Product', 0.00, 10)

    def test_cannot_add_product_with_negative_stock(self, processor):
        with pytest.raises(ValueError, match="cannot be negative"):
            processor.addProductToInventory('PROD-001', 'Product', 10.00, -5)

    def test_update_product_stock(self, processor):
        processor.addProductToInventory('PROD-001', 'Product', 10.00, 50)
        updated = processor.updateProductStock('PROD-001', 75)

        assert updated['stock'] == 75

    def test_cannot_update_stock_of_nonexistent_product(self, processor):
        with pytest.raises(ValueError, match="not found"):
            processor.updateProductStock('INVALID', 10)

    def test_cannot_update_stock_to_negative(self, processor):
        processor.addProductToInventory('PROD-001', 'Product', 10.00, 50)

        with pytest.raises(ValueError, match="cannot be negative"):
            processor.updateProductStock('PROD-001', -10)

    def test_get_inventory_report_empty(self, processor):
        report = processor.getInventoryReport()

        assert report['total_products'] == 0
        assert report['products'] == []

    def test_get_inventory_report_with_products(self, processor_with_inventory):
        report = processor_with_inventory.getInventoryReport()

        assert report['total_products'] == 3
        assert len(report['products']) == 3

        # Check that each product has correct fields
        for product in report['products']:
            assert 'product_id' in product
            assert 'name' in product
            assert 'price' in product
            assert 'stock' in product
            assert 'status' in product

    def test_inventory_report_shows_stock_status(self, processor):
        processor.addProductToInventory('IN-STOCK', 'Available', 10.00, 5)
        processor.addProductToInventory('OUT-STOCK', 'Unavailable', 10.00, 0)

        report = processor.getInventoryReport()

        in_stock = next(p for p in report['products'] if p['product_id'] == 'IN-STOCK')
        out_stock = next(p for p in report['products'] if p['product_id'] == 'OUT-STOCK')

        assert in_stock['status'] == 'in_stock'
        assert out_stock['status'] == 'out_of_stock'


class TestOrderProcessing:
    """Test order creation and processing."""

    def test_process_simple_order(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 2}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        assert order['order_id'] == 1
        assert order['customer_id'] == 'CUST-001'
        assert order['subtotal'] == 51.98  # 25.99 * 2
        assert order['status'] == 'pending'
        assert 'created_at' in order

    def test_process_order_updates_inventory(self, processor_with_inventory):
        initial_stock = processor_with_inventory.inventory['WIDGET-001']['stock']

        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 5}
            ]
        }

        processor_with_inventory.processOrderAndCalculateEverything(order_data)

        assert processor_with_inventory.inventory['WIDGET-001']['stock'] == initial_stock - 5

    def test_process_order_with_multiple_items(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 2},
                {'product_id': 'GADGET-001', 'quantity': 1},
                {'product_id': 'TOOL-001', 'quantity': 3}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        # 25.99*2 + 49.99*1 + 15.99*3 = 51.98 + 49.99 + 47.97 = 149.94
        assert order['subtotal'] == 149.94

    def test_process_order_creates_customer_if_new(self, processor_with_inventory):
        order_data = {
            'customer_id': 'NEW-CUST',
            'customer_name': 'Jane Smith',
            'customer_email': 'jane@example.com',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ]
        }

        processor_with_inventory.processOrderAndCalculateEverything(order_data)

        assert 'NEW-CUST' in processor_with_inventory.customers
        assert processor_with_inventory.customers['NEW-CUST']['name'] == 'Jane Smith'

    def test_cannot_process_order_without_customer_id(self, processor_with_inventory):
        order_data = {
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ]
        }

        with pytest.raises(ValueError, match="Customer ID is required"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_cannot_process_empty_order(self, processor_with_inventory):
        with pytest.raises(ValueError, match="cannot be empty"):
            processor_with_inventory.processOrderAndCalculateEverything(None)

    def test_cannot_process_order_without_items(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001'
        }

        with pytest.raises(ValueError, match="Items list is required"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_cannot_process_order_with_empty_items_list(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': []
        }

        with pytest.raises(ValueError, match="at least one item"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_cannot_process_order_with_invalid_product(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'INVALID', 'quantity': 1}
            ]
        }

        with pytest.raises(ValueError, match="not found in inventory"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_cannot_process_order_with_insufficient_stock(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1000}
            ]
        }

        with pytest.raises(ValueError, match="Insufficient stock"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_cannot_process_order_with_invalid_quantity(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': -5}
            ]
        }

        with pytest.raises(ValueError, match="Invalid quantity"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_cannot_process_order_with_zero_quantity(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 0}
            ]
        }

        with pytest.raises(ValueError, match="Invalid quantity"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_cannot_process_order_missing_product_id(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'quantity': 1}
            ]
        }

        with pytest.raises(ValueError, match="Product ID is required"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_cannot_process_order_missing_quantity(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001'}
            ]
        }

        with pytest.raises(ValueError, match="Quantity is required"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)


class TestDiscounts:
    """Test discount code functionality."""

    def test_apply_discount_code(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 2}
            ],
            'discount_code': 'SAVE10'
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        assert order['discount_code'] == 'SAVE10'
        assert order['discount_amount'] == 5.20  # 51.98 * 0.10

    def test_apply_different_discount_rates(self, processor_with_inventory):
        # Test SAVE20 (20%)
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 4}
            ],
            'discount_code': 'SAVE20'
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        assert order['discount_amount'] == 20.79  # 103.96 * 0.20

    def test_invalid_discount_code(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ],
            'discount_code': 'INVALID'
        }

        with pytest.raises(ValueError, match="Invalid discount code"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_order_without_discount(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        assert order['discount_code'] == ''
        assert order['discount_amount'] == 0


class TestShipping:
    """Test shipping calculations."""

    def test_standard_shipping(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ],
            'shipping_method': 'standard'
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        assert order['shipping_method'] == 'standard'
        assert order['shipping_cost'] == 5.99

    def test_express_shipping(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ],
            'shipping_method': 'express'
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        assert order['shipping_cost'] == 15.99

    def test_overnight_shipping(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ],
            'shipping_method': 'overnight'
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        assert order['shipping_cost'] == 29.99

    def test_default_shipping_method(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        assert order['shipping_method'] == 'standard'

    def test_invalid_shipping_method(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ],
            'shipping_method': 'teleport'
        }

        with pytest.raises(ValueError, match="Invalid shipping method"):
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

    def test_free_shipping_over_100_dollars(self, processor_with_inventory):
        # Order over $100 should get free shipping
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 4}  # 103.96
            ],
            'shipping_method': 'standard'
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        assert order['shipping_cost'] == 0

    def test_free_shipping_after_discount(self, processor_with_inventory):
        # Order that's over $100 after discount
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 5}  # 129.95
            ],
            'discount_code': 'SAVE10',  # -12.995, still over 100
            'shipping_method': 'express'
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        assert order['shipping_cost'] == 0


class TestTaxCalculation:
    """Test tax calculations."""

    def test_tax_calculated_correctly(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}  # 25.99
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        # Tax on 25.99 at 8.5% = 2.209, rounded to 2.21
        assert order['tax_amount'] == 2.21

    def test_tax_on_discounted_amount(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'GADGET-001', 'quantity': 2}  # 99.98
            ],
            'discount_code': 'SAVE20'  # -19.996 = 79.984
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        # Tax on 79.98 at 8.5% = 6.798, rounded to 6.80
        assert order['tax_amount'] == 6.80


class TestOrderTotal:
    """Test final order total calculations."""

    def test_order_total_calculation(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 2}  # 51.98
            ],
            'discount_code': 'SAVE10',  # -5.198 = 46.782
            'shipping_method': 'standard'  # +5.99
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        # Subtotal: 51.98
        # Discount: -5.20
        # Shipping: 5.99
        # Tax: 46.78 * 0.085 = 3.98
        # Total: 51.98 - 5.20 + 5.99 + 3.98 = 56.75
        assert order['total'] == 56.75


class TestOrderRetrieval:
    """Test order retrieval and summary."""

    def test_get_order_summary(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 2}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        summary = processor_with_inventory.getOrderSummaryWithAllDetails(order['order_id'])

        assert summary['order_id'] == order['order_id']
        assert summary['customer']['id'] == 'CUST-001'
        assert summary['customer']['name'] == 'John Doe'
        assert len(summary['items']) == 1
        assert summary['items'][0]['product_id'] == 'WIDGET-001'

    def test_order_summary_includes_product_details(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 2}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        summary = processor_with_inventory.getOrderSummaryWithAllDetails(order['order_id'])

        item = summary['items'][0]
        assert item['name'] == 'Blue Widget'
        assert item['price'] == 25.99
        assert item['quantity'] == 2
        assert item['total'] == 51.98

    def test_cannot_get_summary_for_nonexistent_order(self, processor_with_inventory):
        with pytest.raises(ValueError, match="Order .* not found"):
            processor_with_inventory.getOrderSummaryWithAllDetails(999)


class TestOrderCancellation:
    """Test order cancellation."""

    def test_cancel_order(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 5}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        cancelled = processor_with_inventory.cancelOrderAndRestoreInventory(order['order_id'])

        assert cancelled['status'] == 'cancelled'

    def test_cancel_order_restores_inventory(self, processor_with_inventory):
        initial_stock = processor_with_inventory.inventory['WIDGET-001']['stock']

        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 5}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        processor_with_inventory.cancelOrderAndRestoreInventory(order['order_id'])

        assert processor_with_inventory.inventory['WIDGET-001']['stock'] == initial_stock

    def test_cancel_order_updates_customer_total(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        initial_total = processor_with_inventory.customers['CUST-001']['total_spent']

        processor_with_inventory.cancelOrderAndRestoreInventory(order['order_id'])

        assert processor_with_inventory.customers['CUST-001']['total_spent'] == initial_total - order['total']

    def test_cannot_cancel_nonexistent_order(self, processor_with_inventory):
        with pytest.raises(ValueError, match="not found"):
            processor_with_inventory.cancelOrderAndRestoreInventory(999)

    def test_cannot_cancel_already_cancelled_order(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ]
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        processor_with_inventory.cancelOrderAndRestoreInventory(order['order_id'])

        with pytest.raises(ValueError, match="already cancelled"):
            processor_with_inventory.cancelOrderAndRestoreInventory(order['order_id'])


class TestCustomerManagement:
    """Test customer-related functionality."""

    def test_customer_order_history(self, processor_with_inventory):
        # Place multiple orders
        for i in range(3):
            order_data = {
                'customer_id': 'CUST-001',
                'items': [
                    {'product_id': 'WIDGET-001', 'quantity': 1}
                ]
            }
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

        history = processor_with_inventory.getCustomerOrderHistory('CUST-001')

        assert history['order_count'] == 3
        assert len(history['orders']) == 3

    def test_customer_vip_status_after_spending(self, processor_with_inventory):
        # Place orders totaling over $1000
        for i in range(11):
            order_data = {
                'customer_id': 'CUST-VIP',
                'items': [
                    {'product_id': 'WIDGET-001', 'quantity': 4}  # ~$103 per order
                ]
            }
            processor_with_inventory.processOrderAndCalculateEverything(order_data)

        customer = processor_with_inventory.customers['CUST-VIP']
        assert customer['is_vip'] is True

    def test_customer_loses_vip_after_cancellations(self, processor_with_inventory):
        # Place orders to become VIP
        order_ids = []
        for i in range(11):
            order_data = {
                'customer_id': 'CUST-VIP',
                'items': [
                    {'product_id': 'WIDGET-001', 'quantity': 4}
                ]
            }
            order = processor_with_inventory.processOrderAndCalculateEverything(order_data)
            order_ids.append(order['order_id'])

        # Cancel enough orders to drop below $1000
        for order_id in order_ids[:10]:
            processor_with_inventory.cancelOrderAndRestoreInventory(order_id)

        customer = processor_with_inventory.customers['CUST-VIP']
        assert customer['is_vip'] is False

    def test_cannot_get_history_for_nonexistent_customer(self, processor_with_inventory):
        with pytest.raises(ValueError, match="not found"):
            processor_with_inventory.getCustomerOrderHistory('INVALID')


class TestReporting:
    """Test reporting functionality."""

    def test_revenue_report_empty(self, processor_with_inventory):
        report = processor_with_inventory.calculateRevenueReport()

        assert report['order_count'] == 0
        assert report['total_revenue'] == 0

    def test_revenue_report_with_orders(self, processor_with_inventory):
        # Place several orders
        order_data1 = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 2}
            ]
        }
        processor_with_inventory.processOrderAndCalculateEverything(order_data1)

        order_data2 = {
            'customer_id': 'CUST-002',
            'items': [
                {'product_id': 'GADGET-001', 'quantity': 1}
            ],
            'discount_code': 'SAVE10'
        }
        processor_with_inventory.processOrderAndCalculateEverything(order_data2)

        report = processor_with_inventory.calculateRevenueReport()

        assert report['order_count'] == 2
        assert report['total_revenue'] > 0
        assert report['total_discounts'] >= 0

    def test_revenue_report_excludes_cancelled_orders(self, processor_with_inventory):
        order_data = {
            'customer_id': 'CUST-001',
            'items': [
                {'product_id': 'WIDGET-001', 'quantity': 1}
            ]
        }

        order1 = processor_with_inventory.processOrderAndCalculateEverything(order_data)
        order2 = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        # Cancel one order
        processor_with_inventory.cancelOrderAndRestoreInventory(order1['order_id'])

        report = processor_with_inventory.calculateRevenueReport()
        assert report['order_count'] == 1


class TestComplexScenarios:
    """Test complex multi-step scenarios."""

    def test_complete_order_lifecycle(self, processor_with_inventory):
        # Add product
        processor_with_inventory.addProductToInventory('NEW-PROD', 'New Product', 99.99, 10)

        # Place order
        order_data = {
            'customer_id': 'LIFECYCLE-CUST',
            'customer_name': 'Test User',
            'items': [
                {'product_id': 'NEW-PROD', 'quantity': 2}
            ],
            'discount_code': 'SAVE20',
            'shipping_method': 'express'
        }

        order = processor_with_inventory.processOrderAndCalculateEverything(order_data)

        # Get summary
        summary = processor_with_inventory.getOrderSummaryWithAllDetails(order['order_id'])
        assert summary['order_id'] == order['order_id']

        # Get history
        history = processor_with_inventory.getCustomerOrderHistory('LIFECYCLE-CUST')
        assert history['order_count'] == 1

        # Cancel order
        processor_with_inventory.cancelOrderAndRestoreInventory(order['order_id'])

        # Verify inventory restored
        assert processor_with_inventory.inventory['NEW-PROD']['stock'] == 10

    def test_multiple_customers_multiple_orders(self, processor_with_inventory):
        customers = ['CUST-A', 'CUST-B', 'CUST-C']

        for customer in customers:
            for i in range(2):
                order_data = {
                    'customer_id': customer,
                    'items': [
                        {'product_id': 'WIDGET-001', 'quantity': 1}
                    ]
                }
                processor_with_inventory.processOrderAndCalculateEverything(order_data)

        # Verify all customers have orders
        for customer in customers:
            history = processor_with_inventory.getCustomerOrderHistory(customer)
            assert history['order_count'] == 2

        # Verify revenue report
        report = processor_with_inventory.calculateRevenueReport()
        assert report['order_count'] == 6
