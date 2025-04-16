from django.urls import path
from .views import ProductListView

urlpatterns = [
    # الروابط الجديدة
    path('', views.index, name='index'),  # الصفحة الرئيسية
    path('inventory/', views.inventory, name='inventory'),  # صفحة المخزون

    # الروابط الموجودة بالفعل
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='edit_product'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('products/add_quantity/', views.add_quantity, name='add_quantity'),
    path('products/withdraw_quantity/', views.withdraw_quantity, name='withdraw_quantity'),
    path('products/low_stock/', views.low_stock_products, name='low_stock_products'),
    path('products/clear/', views.clear_products, name='clear_products'),
    path('products/get_info/<int:product_id>/', views.get_product_info, name='get_product_info'),
    path('reports/', views.show_reports, name='show_reports'),
    path('reports/received/', views.received_report_excel, name='received_report'),
    path('reports/withdrawn/', views.withdrawn_report_excel, name='withdrawn_report'),
    path('graph/', views.show_graph, name='graph'),
    path('withdrawn-chart/', views.chart_view, name='withdrawn_chart'),
    path('import_excel/', views.import_excel, name='import_excel'),
    path('export_excel/', views.export_excel, name='export_excel'),
]
