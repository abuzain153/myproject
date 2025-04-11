import os
import django

# إعداد بيئة Django
# يجب أن يشير هذا إلى إعدادات المشروع
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # استبدل myproject باسم مشروعك

django.setup()

# يجب أن يشير هذا إلى نماذج التطبيق
from myapp.models import Product  # استبدل myapp باسم تطبيقك

def correct_product_data():
    products = Product.objects.all()
    for product in products:
        # تبديل اسم المنتج والرمز
        product.product_name, product.product_code = product.product_code, product.product_name
        product.save()
        print(f"تم تصحيح المنتج: {product.product_name} - {product.product_code}")

if __name__ == '__main__':
    correct_product_data()
    print("تم تصحيح جميع المنتجات.")
