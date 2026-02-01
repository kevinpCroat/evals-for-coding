"""
Shopping Cart Module

A realistic e-commerce shopping cart implementation with various edge cases
that require comprehensive testing.
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal, InvalidOperation
from datetime import datetime


class InvalidQuantityError(Exception):
    """Raised when an invalid quantity is provided."""
    pass


class InvalidPriceError(Exception):
    """Raised when an invalid price is provided."""
    pass


class InvalidDiscountError(Exception):
    """Raised when an invalid discount is provided."""
    pass


class Item:
    """Represents a product item in the cart."""

    def __init__(self, item_id: str, name: str, price: float, quantity: int = 1):
        if not item_id or not isinstance(item_id, str):
            raise ValueError("Item ID must be a non-empty string")
        if not name or not isinstance(name, str):
            raise ValueError("Item name must be a non-empty string")
        if price < 0:
            raise InvalidPriceError("Price cannot be negative")
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be positive")

        self.item_id = item_id
        self.name = name
        self.price = Decimal(str(price))
        self.quantity = quantity

    def get_total(self) -> Decimal:
        """Calculate total price for this item."""
        return self.price * self.quantity


class ShoppingCart:
    """Shopping cart with discount and tax calculation capabilities."""

    def __init__(self, tax_rate: float = 0.0):
        if tax_rate < 0 or tax_rate > 1:
            raise ValueError("Tax rate must be between 0 and 1")

        self.items: Dict[str, Item] = {}
        self.tax_rate = Decimal(str(tax_rate))
        self.discounts: List[Tuple[str, Decimal]] = []
        self.loyalty_points = 0

    def add_item(self, item: Item) -> None:
        """Add an item to the cart or update quantity if it exists."""
        if not isinstance(item, Item):
            raise TypeError("Must provide an Item instance")

        if item.item_id in self.items:
            self.items[item.item_id].quantity += item.quantity
        else:
            self.items[item.item_id] = item

    def remove_item(self, item_id: str) -> None:
        """Remove an item from the cart."""
        if item_id not in self.items:
            raise KeyError(f"Item {item_id} not found in cart")
        del self.items[item_id]

    def update_quantity(self, item_id: str, quantity: int) -> None:
        """Update the quantity of an item."""
        if item_id not in self.items:
            raise KeyError(f"Item {item_id} not found in cart")
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be positive")

        self.items[item_id].quantity = quantity

    def get_item_count(self) -> int:
        """Get total number of items (sum of quantities)."""
        return sum(item.quantity for item in self.items.values())

    def get_unique_item_count(self) -> int:
        """Get number of unique items."""
        return len(self.items)

    def is_empty(self) -> bool:
        """Check if cart is empty."""
        return len(self.items) == 0

    def clear(self) -> None:
        """Remove all items from the cart."""
        self.items.clear()
        self.discounts.clear()

    def apply_discount(self, name: str, percentage: float) -> None:
        """Apply a percentage discount."""
        if percentage < 0 or percentage > 100:
            raise InvalidDiscountError("Discount percentage must be between 0 and 100")

        self.discounts.append((name, Decimal(str(percentage))))

    def get_subtotal(self) -> Decimal:
        """Calculate subtotal before discounts and tax."""
        return sum(item.get_total() for item in self.items.values())

    def get_discount_amount(self) -> Decimal:
        """Calculate total discount amount."""
        subtotal = self.get_subtotal()
        total_discount = Decimal('0')

        for name, percentage in self.discounts:
            discount_amount = subtotal * (percentage / Decimal('100'))
            total_discount += discount_amount

        # Ensure discount doesn't exceed subtotal
        return min(total_discount, subtotal)

    def get_tax_amount(self) -> Decimal:
        """Calculate tax on subtotal after discounts."""
        taxable_amount = self.get_subtotal() - self.get_discount_amount()
        return taxable_amount * self.tax_rate

    def get_total(self) -> Decimal:
        """Calculate final total including discounts and tax."""
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        tax = self.get_tax_amount()
        return subtotal - discount + tax

    def apply_loyalty_points(self, points: int) -> None:
        """Add loyalty points (1 point per dollar spent)."""
        if points < 0:
            raise ValueError("Loyalty points cannot be negative")
        self.loyalty_points += points

    def calculate_loyalty_points(self) -> int:
        """Calculate loyalty points earned from current purchase."""
        total = self.get_total()
        return int(total)

    def get_item(self, item_id: str) -> Optional[Item]:
        """Get an item by ID."""
        return self.items.get(item_id)

    def get_items_by_price_range(self, min_price: float, max_price: float) -> List[Item]:
        """Get all items within a price range."""
        if min_price < 0 or max_price < 0:
            raise ValueError("Prices cannot be negative")
        if min_price > max_price:
            raise ValueError("Min price cannot be greater than max price")

        min_decimal = Decimal(str(min_price))
        max_decimal = Decimal(str(max_price))

        return [
            item for item in self.items.values()
            if min_decimal <= item.price <= max_decimal
        ]

    def get_summary(self) -> Dict:
        """Get a summary of the cart."""
        return {
            'item_count': self.get_item_count(),
            'unique_items': self.get_unique_item_count(),
            'subtotal': float(self.get_subtotal()),
            'discount': float(self.get_discount_amount()),
            'tax': float(self.get_tax_amount()),
            'total': float(self.get_total()),
            'loyalty_points': self.loyalty_points
        }
