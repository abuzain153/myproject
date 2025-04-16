from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="اسم المنتج")
    product_code = models.CharField(max_length=50, unique=True, verbose_name="رمز المنتج")
    quantity = models.FloatField(default=0, verbose_name="الكمية")
    unit = models.CharField(max_length=50, verbose_name="الوحدة")
    min_stock = models.FloatField(verbose_name="الحد الأدنى للمخزون")

    def __str__(self):
        return f"{self.product_name} (رمز: {self.product_code})"

    def save(self, *args, **kwargs):
        if self.quantity < 0:
            raise ValueError("لا يمكن أن تكون الكمية سالبة.")
        super().save(*args, **kwargs)

class Movement(models.Model):
    MOVEMENT_TYPES = (
        ('استلام', 'استلام'),
        ('سحب', 'سحب'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="المنتج")
    movement_type = models.CharField(max_length=50, choices=MOVEMENT_TYPES, verbose_name="نوع الحركة")
    quantity = models.FloatField(verbose_name="الكمية")
    date = models.DateTimeField(auto_now_add=True, verbose_name="التاريخ")

    def __str__(self):
        return f"{self.product.product_name} - {self.movement_type} - {self.quantity}"

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            raise ValueError("الكمية يجب أن تكون أكبر من الصفر.")
        if self.movement_type == "سحب" and self.quantity > self.product.quantity:
            raise ValueError("الكمية المسحوبة أكبر من المخزون المتوفر.")
        super().save(*args, **kwargs)

@receiver(post_save, sender=Movement)
def update_product_quantity(sender, instance, created, **kwargs):
    """
    تحديث كمية المنتج بعد حفظ الحركة.
    """
    product = instance.product
    if instance.movement_type == 'استلام':
        product.quantity += instance.quantity
    elif instance.movement_type == 'سحب':
        product.quantity -= instance.quantity
    product.save()
