from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=50, unique=True)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=50)
    min_stock = models.FloatField()

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        # إزالة التحقق من الكمية السالبة
        super().save(*args, **kwargs)

class Movement(models.Model):
    MOVEMENT_TYPES = (
        ('استلام', 'استلام'),
        ('سحب', 'سحب'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=50, choices=MOVEMENT_TYPES)
    quantity = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.movement_type} - {self.quantity}"

    def save(self, *args, **kwargs):
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
