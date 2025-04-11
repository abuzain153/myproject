from django.urls import path
from . import views

urlpatterns = [
    path('get_product_info/<int:product_id>/', views.get_product_info, name='get_product_info'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('products/add_quantity/', views.add_quantity, name='add_quantity'),
    path('products/withdraw_quantity/', views.withdraw_quantity, name='withdraw_quantity'),
    path('reports/', views.show_reports, name='show_reports'),
    path('reports/received/', views.received_report_excel, name='received_report'),  # تم التعديل هنا
    path('reports/withdrawn/', views.withdrawn_report_excel, name='withdrawn_report'),  # تم التعديل هنا
    path('graph/', views.show_graph, name='show_graph'),
    path('low_stock/', views.low_stock_products, name='low_stock_products'),
    path('import_excel/', views.import_excel, name='import_excel'),
    path('export_excel/', views.export_excel, name='export_excel'),
    path('withdrawn-chart/', views.chart_view, name='withdrawn_chart'),
    path('products/', views.product_list, name='product_list'),
    path('clear_products/', views.clear_products, name='clear_products'),
    # هذا هو المسار الجديد
]
