from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),
    path('suppliers/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),

    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_create, name='transaction_create'),

    path('purchase-orders/', views.po_list, name='po_list'),
    path('purchase-orders/add/', views.po_create, name='po_create'),
    path('purchase-orders/<int:pk>/', views.po_detail, name='po_detail'),
    path('purchase-orders/<int:pk>/status/', views.po_update_status, name='po_update_status'),
    path('purchase-orders/<int:pk>/delete/', views.po_delete, name='po_delete'),

    path('sales-orders/', views.so_list, name='so_list'),
    path('sales-orders/add/', views.so_create, name='so_create'),
    path('sales-orders/<int:pk>/', views.so_detail, name='so_detail'),
    path('sales-orders/<int:pk>/status/', views.so_update_status, name='so_update_status'),
    path('sales-orders/<int:pk>/delete/', views.so_delete, name='so_delete'),

    path('reports/', views.reports, name='reports'),
    path('reports/export/csv/<str:report_type>/', views.export_csv, name='export_csv'),
    path('reports/export/pdf/<str:report_type>/', views.export_pdf, name='export_pdf'),

    path('chart-data/', views.chart_data, name='chart_data'),
]
