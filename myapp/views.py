from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, F
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Movement
from .forms import ProductForm
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import base64


# Helper function to update product quantity
def update_product_quantity(product, quantity, movement_type):
    if movement_type == 'سحب' and quantity > product.quantity:
        raise ValueError("لا يمكن سحب كمية أكبر من الكمية المتاحة.")
    if movement_type == 'سحب':
        product.quantity -= quantity
    elif movement_type == 'استلام':
        product.quantity += quantity
    product.save()


# List products
class ProductListView(ListView):
    model = Product
    template_name = 'myapp/product_list.html'
    context_object_name = 'products'


# Add a new product
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'myapp/add_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, f'تم إضافة المنتج {form.instance.product_name} بنجاح!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "حدث خطأ في إضافة المنتج. يرجى التحقق من النموذج.")
        return super().form_invalid(form)
def show_reports(request):
    # يمكن إضافة منطق عرض التقارير هنا
    context = {
        'reports': [],  # أضف التقارير هنا
    }
    return render(request, 'myapp/reports.html', context)
def product_list(request):
    # جلب جميع المنتجات من قاعدة البيانات
    products = Product.objects.all()
    # تمرير المنتجات إلى القالب
    return render(request, 'myapp/product_list.html', {'products': products})   
def clear_products(request):
    # حذف جميع المنتجات
    Product.objects.all().delete()
    messages.success(request, "تم حذف جميع المنتجات بنجاح.")
    return redirect('product_list')  # إعادة التوجيه إلى قائمة المنتجات
# Edit an existing product
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'myapp/edit_product.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        messages.success(self.request, f'تم تعديل المنتج {form.instance.product_name} بنجاح!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "حدث خطأ في تعديل المنتج. يرجى التحقق من النموذج.")
        return super().form_invalid(form)


# Delete a product
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'myapp/confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "تم حذف المنتج بنجاح.")
        return super().delete(request, *args, **kwargs)


# Add quantity to a product
def add_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_to_add = request.POST.get('quantity_to_add')
        try:
            quantity_to_add = float(quantity_to_add)
            if quantity_to_add <= 0:
                raise ValueError("الكمية يجب أن تكون أكبر من صفر")

            product = get_object_or_404(Product, pk=product_id)
            update_product_quantity(product, quantity_to_add, 'استلام')

            Movement.objects.create(
                product=product,
                movement_type='استلام',
                quantity=quantity_to_add,
                date=timezone.now()
            )
            messages.success(request, f'تمت إضافة {quantity_to_add} إلى {product.product_name} بنجاح!')
            return redirect('product_list')
        except ValueError as e:
            messages.error(request, f'خطأ: {str(e)}')

    return render(request, 'myapp/add_quantity.html', {'products': Product.objects.all()})
def withdrawn_report_excel(request):
    # جلب جميع الحركات من النوع "سحب"
    withdrawn_movements = Movement.objects.filter(movement_type='سحب')
    data = {
        'اسم المنتج': [movement.product.product_name for movement in withdrawn_movements],
        'الكمية المسحوبة': [movement.quantity for movement in withdrawn_movements],
        'التاريخ': [movement.date.strftime('%Y-%m-%d') for movement in withdrawn_movements],
    }
    df = pd.DataFrame(data)

    # إنشاء ملف Excel للتحميل
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="withdrawn_report.xlsx"'
    df.to_excel(response, index=False)
    return response
def received_report_excel(request):
    # جلب جميع الحركات من النوع "استلام"
    received_movements = Movement.objects.filter(movement_type='استلام')
    data = {
        'اسم المنتج': [movement.product.product_name for movement in received_movements],
        'الكمية المستلمة': [movement.quantity for movement in received_movements],
        'التاريخ': [movement.date.strftime('%Y-%m-%d') for movement in received_movements],
    }
    df = pd.DataFrame(data)

    # إنشاء ملف Excel للتحميل
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="received_report.xlsx"'
    df.to_excel(response, index=False)
    return response
# Withdraw quantity from a product
def withdraw_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_to_withdraw = request.POST.get('quantity_to_withdraw')
        try:
            quantity_to_withdraw = float(quantity_to_withdraw)
            if quantity_to_withdraw <= 0:
                raise ValueError("الكمية يجب أن تكون أكبر من صفر")

            product = get_object_or_404(Product, pk=product_id)
            update_product_quantity(product, quantity_to_withdraw, 'سحب')

            Movement.objects.create(
                product=product,
                movement_type='سحب',
                quantity=quantity_to_withdraw,
                date=timezone.now()
            )
            messages.success(request, f'تم سحب {quantity_to_withdraw} من {product.product_name} بنجاح!')
            return redirect('product_list')
        except ValueError as e:
            messages.error(request, f'خطأ: {str(e)}')

    return render(request, 'myapp/withdraw_quantity.html', {'products': Product.objects.all()})

def chart_view(request):
    # جلب الحركات من النوع "سحب"
    movements = Movement.objects.filter(movement_type='سحب')
    if not movements.exists():
        return render(request, 'myapp/chart.html', {'error': 'لا توجد بيانات لعرض الرسم البياني.'})

    # إعداد البيانات للرسم البياني
    dates = [movement.date.strftime('%Y-%m-%d') for movement in movements]
    quantities = [movement.quantity for movement in movements]

    # إنشاء الرسم البياني
    plt.figure(figsize=(10, 6))
    plt.plot(dates, quantities, marker='o', linestyle='-', color='b')
    plt.title('الرسم البياني للسحب')
    plt.xlabel('التاريخ')
    plt.ylabel('الكمية المسحوبة')
    plt.grid(True)

    # تحويل الرسم البياني إلى صورة
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # تمرير الرسم البياني إلى القالب
    return render(request, 'myapp/chart.html', {'chart': image_data})
# Show graph for withdrawals
def show_graph(request):
    movements = Movement.objects.filter(movement_type='سحب')
    if not movements:
        return render(request, 'myapp/graph.html', {'error': 'لا يوجد مسحوبات'})

    dates = [movement.date.strftime('%Y-%m-%d') for movement in movements]
    quantities = [movement.quantity for movement in movements]

    fig, ax = plt.subplots()
    ax.plot(dates, quantities, marker='o')
    ax.set(xlabel='التاريخ', ylabel='الكمية المسحوبة', title='الكميات المسحوبة عبر الأيام')
    ax.grid()

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_data = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render(request, 'myapp/graph.html', {'graph': image_data})

def get_product_info(request, product_id):
    # جلب المنتج المطلوب أو عرض خطأ 404 إذا لم يكن موجودًا
    product = get_object_or_404(Product, id=product_id)
    # إرجاع المعلومات كـ JSON
    data = {
        'product_name': product.product_name,
        'product_code': product.product_code,
        'quantity': product.quantity,
        'unit': product.unit,
        'min_stock': product.min_stock,
    }
    return JsonResponse(data)
# Export products to Excel
def export_excel(request):
    products = Product.objects.all()
    data = {
        'اسم المنتج': [product.product_name for product in products],
        'رمز المنتج': [product.product_code for product in products],
        'الكمية': [product.quantity for product in products],
        'الوحدة': [product.unit for product in products],
        'الحد الأدنى': [product.min_stock for product in products],
    }
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="inventory.xlsx"'
    df.to_excel(response, index=False)
    return response
def low_stock_products(request):
    # الحد الأدنى للمخزون
    low_stock_threshold = 10  # يمكنك تعديل الرقم حسب الحاجة
    products = Product.objects.filter(quantity__lt=low_stock_threshold)
    return render(request, 'myapp/low_stock.html', {'products': products})
def index(request):
    return render(request, 'myapp/index.html')

def inventory(request):
    products = Product.objects.all()
    return render(request, 'myapp/inventory.html', {'products': products})
# Import products from Excel
def import_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file)
            required_columns = ['product_name', 'product_code', 'quantity', 'unit', 'min_stock']
            if not all(col in df.columns for col in required_columns):
                messages.error(request, 'خطأ: ملف Excel لا يحتوي على جميع الأعمدة المطلوبة.')
                return redirect('import_excel')

            products = []
            for _, row in df.iterrows():
                if all(pd.notnull(row)):
                    products.append(Product(
                        product_name=row['product_name'].strip(),
                        product_code=row['product_code'].strip(),
                        quantity=float(row['quantity']),
                        unit=row['unit'].strip(),
                        min_stock=float(row['min_stock'])
                    ))
            Product.objects.bulk_create(products)
            messages.success(request, 'تم استيراد البيانات بنجاح.')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'خطأ: حدث خطأ أثناء قراءة ملف Excel: {e}')
            return redirect('import_excel')

    return render(request, 'myapp/import_excel.html')
