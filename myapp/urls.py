from django.urls import path
from . import views

urlpatterns = [
    # روابط المنتجات
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='add_product'),  # تعديل باستخدام Class-Based View
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='edit_product'),  # تعديل باستخدام Class-Based View
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),  # تعديل باستخدام Class-Based View
    path('products/add_quantity/', views.add_quantity, name='add_quantity'),
    path('products/withdraw_quantity/', views.withdraw_quantity, name='withdraw_quantity'),
    path('products/low_stock/', views.low_stock_products, name='low_stock_products'),
    path('products/clear/', views.clear_products, name='clear_products'),
    path('products/get_info/<int:product_id>/', views.get_product_info, name='get_product_info'),  # تحسين اسم الرابط

    # روابط التقارير
    path('reports/', views.show_reports, name='show_reports'),
    path('reports/received/', views.received_report_excel, name='received_report'),
    path('reports/withdrawn/', views.withdrawn_report_excel, name='withdrawn_report'),

    # روابط الرسوم البيانية
    path('graph/', views.show_graph, name='show_graph'),
    path('withdrawn-chart/', views.chart_view, name='withdrawn_chart'),

    # استيراد وتصدير Excel
    path('import_excel/', views.import_excel, name='import_excel'),
    path('export_excel/', views.export_excel, name='export_excel'),
]
