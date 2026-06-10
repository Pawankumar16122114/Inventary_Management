from django import template
from django.db.models import Sum, F
from ..models import Product, StockTransaction, PurchaseOrder, SalesOrder
from decimal import Decimal

register = template.Library()


@register.simple_tag
def total_products():
    return Product.objects.count()


@register.simple_tag
def total_categories():
    from ..models import Category
    return Category.objects.count()


@register.simple_tag
def total_suppliers():
    from ..models import Supplier
    return Supplier.objects.count()


@register.simple_tag
def low_stock_count():
    return Product.objects.filter(quantity__lte=F('low_stock_threshold')).count()


@register.simple_tag
def stock_value():
    result = Product.objects.aggregate(
        total=Sum(F('quantity') * F('cost'))
    )['total']
    return result or Decimal('0.00')


@register.simple_tag
def potential_revenue():
    result = Product.objects.aggregate(
        total=Sum(F('quantity') * F('price'))
    )['total']
    return result or Decimal('0.00')


@register.simple_tag
def total_in_transactions():
    return StockTransaction.objects.filter(transaction_type='IN').count()


@register.simple_tag
def total_out_transactions():
    return StockTransaction.objects.filter(transaction_type='OUT').count()


@register.simple_tag
def pending_po_count():
    return PurchaseOrder.objects.exclude(status__in=['COMPLETED', 'CANCELLED']).count()


@register.simple_tag
def pending_so_count():
    return SalesOrder.objects.exclude(status__in=['DELIVERED', 'CANCELLED']).count()


@register.filter
def currency(value):
    try:
        return f'\u20b9{float(value):,.2f}'
    except (ValueError, TypeError):
        return value


@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0
