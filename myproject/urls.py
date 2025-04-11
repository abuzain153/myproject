from django.contrib import admin
from django.urls import path, include
from myapp import views #اضافة هذا السطر

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')),
    path('', views.product_list, name='home'), #اضافة هذا السطر
]
