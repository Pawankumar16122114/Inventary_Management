import csv
from decimal import Decimal
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.db.models import Sum, F, Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from .decorators import admin_required, manager_required, staff_or_above
from .forms import (
    LoginForm, CategoryForm, SupplierForm, ProductForm,
    StockTransactionForm, PurchaseOrderForm, SalesOrderForm,
    PurchaseOrderItemFormSet, SalesOrderItemFormSet,
)
from .models import (
    CustomUser, Category, Supplier, Product,
    StockTransaction, PurchaseOrder, PurchaseOrderItem,
    SalesOrder, SalesOrderItem,
)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@staff_or_above
def dashboard(request):
    products = Product.objects.select_related('category').all()
    low_stock_products = [p for p in products if p.is_low_stock]

    category_stock = Product.objects.values('category__name').annotate(
        total_qty=Sum('quantity'),
        total_value=Sum(F('quantity') * F('cost')),
    ).order_by('-total_qty')

    recent_transactions = StockTransaction.objects.select_related(
        'product', 'created_by'
    ).all()[:10]

    context = {
        'products': products,
        'low_stock_products': low_stock_products,
        'category_stock': list(category_stock),
        'recent_transactions': recent_transactions,
    }
    return render(request, 'dashboard/index.html', context)


@staff_or_above
def product_list(request):
    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    products = Product.objects.select_related('category', 'supplier').all()
    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(sku__icontains=q)
        )
    if category_id:
        products = products.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'products/list.html', {
        'products': products,
        'categories': categories,
        'q': q,
        'selected_category': category_id,
    })


@manager_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            StockTransaction.objects.create(
                product=product,
                transaction_type='IN',
                quantity=product.quantity,
                notes='Initial stock on product creation',
                created_by=request.user,
            )
            messages.success(request, f'Product "{product.name}" created successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/form.html', {'form': form, 'title': 'Add Product'})


@staff_or_above
def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('category', 'supplier'), pk=pk
    )
    transactions = product.transactions.select_related('created_by').all()[:20]
    return render(request, 'products/detail.html', {
        'product': product,
        'transactions': transactions,
    })


@manager_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated.')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/form.html', {
        'form': form,
        'title': 'Edit Product',
        'product': product,
    })


@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Product "{name}" deleted.')
        return redirect('product_list')
    return render(request, 'products/confirm_delete.html', {
        'object': product,
        'object_type': 'Product',
        'cancel_url': 'product_detail',
    })


@staff_or_above
def category_list(request):
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).all()
    return render(request, 'categories/list.html', {'categories': categories})


@manager_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/form.html', {'form': form, 'title': 'Add Category'})


@manager_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/form.html', {
        'form': form,
        'title': 'Edit Category',
        'category': category,
    })


@admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('category_list')
    return render(request, 'products/confirm_delete.html', {
        'object': category,
        'object_type': 'Category',
        'cancel_url': 'category_list',
    })


@staff_or_above
def supplier_list(request):
    suppliers = Supplier.objects.annotate(
        product_count=Count('products'),
        po_count=Count('purchase_orders'),
    ).all()
    return render(request, 'suppliers/list.html', {'suppliers': suppliers})


@manager_required
def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier created.')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'suppliers/form.html', {'form': form, 'title': 'Add Supplier'})


@manager_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier updated.')
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'suppliers/form.html', {
        'form': form,
        'title': 'Edit Supplier',
        'supplier': supplier,
    })


@admin_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Supplier deleted.')
        return redirect('supplier_list')
    return render(request, 'products/confirm_delete.html', {
        'object': supplier,
        'object_type': 'Supplier',
        'cancel_url': 'supplier_list',
    })


@staff_or_above
def transaction_list(request):
    transaction_type = request.GET.get('type', '')
    transactions = StockTransaction.objects.select_related(
        'product', 'created_by'
    ).all()
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    return render(request, 'transactions/list.html', {
        'transactions': transactions,
        'selected_type': transaction_type,
    })


@manager_required
def transaction_create(request):
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            trans = form.save(commit=False)
            trans.created_by = request.user
            product = trans.product
            if trans.transaction_type == 'IN':
                product.quantity += trans.quantity
            elif trans.transaction_type == 'OUT':
                if product.quantity < trans.quantity:
                    messages.error(
                        request,
                        f'Insufficient stock! Only {product.quantity} units of "{product.name}" available.'
                    )
                    return render(request, 'transactions/form.html', {'form': form})
                product.quantity -= trans.quantity
            else:
                product.quantity = trans.quantity
            product.save()
            trans.save()
            messages.success(
                request,
                f'{trans.get_transaction_type_display()} — {trans.product.name} x{trans.quantity}'
            )
            return redirect('transaction_list')
    else:
        form = StockTransactionForm()
    return render(request, 'transactions/form.html', {'form': form})


@staff_or_above
def po_list(request):
    status = request.GET.get('status', '')
    pos = PurchaseOrder.objects.select_related('supplier', 'created_by').all()
    if status:
        pos = pos.filter(status=status)
    return render(request, 'orders/purchaseorder_list.html', {
        'pos': pos,
        'selected_status': status,
    })


@manager_required
def po_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        formset = PurchaseOrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            po = form.save(commit=False)
            po.created_by = request.user
            with transaction.atomic():
                po.save()
                formset.instance = po
                formset.save()
                total = sum(
                    item.quantity_ordered * item.unit_price
                    for item in po.items.all()
                )
                po.total_amount = total
                po.save()
            messages.success(request, f'Purchase Order {po.po_number} created.')
            return redirect('po_list')
    else:
        form = PurchaseOrderForm()
        formset = PurchaseOrderItemFormSet()
    return render(request, 'orders/purchaseorder_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Purchase Order',
    })


@staff_or_above
def po_detail(request, pk):
    po = get_object_or_404(
        PurchaseOrder.objects.select_related('supplier', 'created_by'),
        pk=pk,
    )
    items = po.items.select_related('product').all()
    return render(request, 'orders/purchaseorder_detail.html', {
        'po': po,
        'items': items,
    })


@manager_required
def po_update_status(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(PurchaseOrder.PO_STATUS_CHOICES):
            old_status = po.status
            if new_status == 'RECEIVED' and old_status != 'RECEIVED':
                if not po.items.exists():
                    messages.error(request, 'Cannot mark as received — no items in PO.')
                    return redirect('po_detail', pk=pk)
                for item in po.items.all():
                    to_receive = item.quantity_ordered - item.quantity_received
                    if to_receive > 0:
                        item.quantity_received = item.quantity_ordered
                        item.save()
                        item.product.quantity += to_receive
                        item.product.save()
                        StockTransaction.objects.create(
                            product=item.product,
                            transaction_type='IN',
                            quantity=to_receive,
                            notes=f'PO {po.po_number} receipt',
                            created_by=request.user,
                        )
                po.status = 'COMPLETED'
            elif new_status == 'CANCELLED':
                po.status = 'CANCELLED'
            else:
                po.status = new_status
            po.save()
            messages.success(request, f'PO {po.po_number} status updated to {po.get_status_display()}.')
        return redirect('po_detail', pk=pk)


@admin_required
def po_delete(request, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)
    if request.method == 'POST':
        po.delete()
        messages.success(request, 'Purchase Order deleted.')
        return redirect('po_list')
    return render(request, 'products/confirm_delete.html', {
        'object': po,
        'object_type': 'Purchase Order',
        'cancel_url': 'po_detail',
    })


@staff_or_above
def so_list(request):
    status = request.GET.get('status', '')
    sos = SalesOrder.objects.select_related('created_by').all()
    if status:
        sos = sos.filter(status=status)
    return render(request, 'orders/salesorder_list.html', {
        'sos': sos,
        'selected_status': status,
    })


@manager_required
def so_create(request):
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        formset = SalesOrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            so = form.save(commit=False)
            so.created_by = request.user
            with transaction.atomic():
                so.save()
                formset.instance = so
                formset.save()
                total = sum(
                    item.quantity * item.unit_price
                    for item in so.items.all()
                )
                so.total_amount = total
                so.save()
            messages.success(request, f'Sales Order {so.so_number} created.')
            return redirect('so_list')
    else:
        form = SalesOrderForm()
        formset = SalesOrderItemFormSet()
    return render(request, 'orders/salesorder_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Sales Order',
    })


@staff_or_above
def so_detail(request, pk):
    so = get_object_or_404(
        SalesOrder.objects.select_related('created_by'),
        pk=pk,
    )
    items = so.items.select_related('product').all()
    return render(request, 'orders/salesorder_detail.html', {
        'so': so,
        'items': items,
    })


@manager_required
def so_update_status(request, pk):
    so = get_object_or_404(SalesOrder, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(SalesOrder.SO_STATUS_CHOICES):
            if new_status in ('SHIPPED', 'DELIVERED') and so.status == 'CONFIRMED':
                for item in so.items.all():
                    if item.product.quantity < item.quantity:
                        messages.error(
                            request,
                            f'Insufficient stock for "{item.product.name}". '
                            f'Need {item.quantity}, have {item.product.quantity}.'
                        )
                        return redirect('so_detail', pk=pk)
                for item in so.items.all():
                    item.product.quantity -= item.quantity
                    item.product.save()
                    StockTransaction.objects.create(
                        product=item.product,
                        transaction_type='OUT',
                        quantity=item.quantity,
                        notes=f'SO {so.so_number} fulfilment',
                        created_by=request.user,
                    )
            elif new_status == 'CANCELLED':
                so.status = 'CANCELLED'
            so.status = new_status
            so.save()
            messages.success(request, f'SO {so.so_number} status updated to {so.get_status_display()}.')
        return redirect('so_detail', pk=pk)


@admin_required
def so_delete(request, pk):
    so = get_object_or_404(SalesOrder, pk=pk)
    if request.method == 'POST':
        so.delete()
        messages.success(request, 'Sales Order deleted.')
        return redirect('so_list')
    return render(request, 'products/confirm_delete.html', {
        'object': so,
        'object_type': 'Sales Order',
        'cancel_url': 'so_detail',
    })


@staff_or_above
def reports(request):
    products = Product.objects.select_related('category').all()
    low_stock = [p for p in products if p.is_low_stock]
    category_data = Product.objects.values('category__name').annotate(
        total_qty=Sum('quantity'),
        total_value=Sum(F('quantity') * F('cost')),
    ).order_by('-total_qty')

    context = {
        'products': products,
        'low_stock': low_stock,
        'category_data': list(category_data),
    }
    return render(request, 'reports/index.html', context)


@staff_or_above
def export_csv(request, report_type):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report_{timezone.now().strftime("%Y%m%d")}.csv"'
    writer = csv.writer(response)

    if report_type == 'products':
        writer.writerow(['SKU', 'Name', 'Category', 'Supplier', 'Price', 'Cost', 'Quantity', 'Value'])
        for p in Product.objects.select_related('category', 'supplier').all():
            writer.writerow([
                p.sku, p.name,
                p.category.name if p.category else '-',
                p.supplier.name if p.supplier else '-',
                p.price, p.cost, p.quantity,
                p.quantity * p.cost,
            ])
    elif report_type == 'low_stock':
        writer.writerow(['SKU', 'Name', 'Quantity', 'Threshold', 'Category'])
        for p in Product.objects.select_related('category').all():
            if p.is_low_stock:
                writer.writerow([
                    p.sku, p.name, p.quantity,
                    p.low_stock_threshold,
                    p.category.name if p.category else '-',
                ])
    elif report_type == 'transactions':
        writer.writerow(['Date', 'Product', 'Type', 'Quantity', 'Notes', 'By'])
        for t in StockTransaction.objects.select_related('product', 'created_by').all():
            writer.writerow([
                t.timestamp.strftime('%Y-%m-%d %H:%M'),
                t.product.name,
                t.get_transaction_type_display(),
                t.quantity,
                t.notes,
                t.created_by.username if t.created_by else '-',
            ])

    return response


@staff_or_above
def export_pdf(request, report_type):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title=f'{report_type.title()} Report')
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f'{report_type.title()} Report', styles['Title']))
    elements.append(Spacer(1, 0.25 * inch))

    if report_type == 'products':
        data = [['SKU', 'Name', 'Category', 'Price', 'Cost', 'Qty', 'Value']]
        for p in Product.objects.select_related('category').all():
            data.append([
                p.sku, p.name,
                p.category.name if p.category else '-',
                f'{p.price:.2f}', f'{p.cost:.2f}',
                str(p.quantity), f'{p.quantity * p.cost:.2f}',
            ])
    elif report_type == 'low_stock':
        data = [['SKU', 'Name', 'Qty', 'Threshold']]
        for p in Product.objects.all():
            if p.is_low_stock:
                data.append([p.sku, p.name, str(p.quantity), str(p.low_stock_threshold)])
    elif report_type == 'transactions':
        data = [['Date', 'Product', 'Type', 'Qty', 'Notes']]
        for t in StockTransaction.objects.select_related('product').all():
            data.append([
                t.timestamp.strftime('%Y-%m-%d'),
                t.product.name,
                t.get_transaction_type_display(),
                str(t.quantity), t.notes,
            ])
    else:
        data = [['No data']]

    if len(data) > 1:
        table = Table(data, repeatRows=1)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f8ef7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')]),
        ])
        table.setStyle(style)
        elements.append(table)
    else:
        elements.append(Paragraph('No data available.', styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report_{timezone.now().strftime("%Y%m%d")}.pdf"'
    return response


@staff_or_above
def chart_data(request):
    category_labels = []
    category_qty = []
    category_value = []
    for item in Product.objects.values('category__name').annotate(
        total_qty=Sum('quantity'),
        total_value=Sum(F('quantity') * F('cost')),
    ).order_by('-total_qty'):
        category_labels.append(item['category__name'] or 'Uncategorised')
        category_qty.append(int(item['total_qty'] or 0))
        category_value.append(float(item['total_value'] or 0))

    transactions = StockTransaction.objects.values('transaction_type').annotate(
        count=Count('id')
    )
    trans_labels = []
    trans_counts = []
    for item in transactions:
        trans_labels.append(dict(StockTransaction.TRANSACTION_TYPES).get(item['transaction_type'], item['transaction_type']))
        trans_counts.append(item['count'])

    return JsonResponse({
        'category_labels': category_labels,
        'category_quantity': category_qty,
        'category_value': category_value,
        'transaction_labels': trans_labels,
        'transaction_counts': trans_counts,
    })
