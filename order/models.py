from uuid import uuid4
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from product.models import Product


User = get_user_model()


class Order(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, primary_key=True, verbose_name=_('آیدی'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order', verbose_name=_('کاربر'))

    class StatusOrder(models.TextChoices):
        pending = 'pending', _('در انتظار پرداخت')
        complete = 'complete', _('پرداخت شده')
        failed = 'failed', _('پرداخت ناموفق')

    status = models.CharField(max_length=20, choices=StatusOrder.choices, default=StatusOrder.pending, verbose_name=_('وضعیت سفارش'))
    total_price = models.IntegerField(default=0, verbose_name=_('قیمت کل سفارش'))
    payment_date = models.DateTimeField(_('تاریخ پرداخت'), null=True, blank=True)
    is_paid = models.BooleanField(default=False, verbose_name=_('پرداخت شده؟'))
    first_name = models.CharField(max_length=100, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    email = models.EmailField(max_length=150, null=True, blank=True, verbose_name=_('ایمیل(اختیاری)'))
    phone_number = models.CharField(max_length=11, verbose_name=_('شماره تلفن'))
    state = models.CharField(max_length=100, verbose_name=_('استان'))
    city = models.CharField(max_length=100, verbose_name=_('شهر'))
    zip_code = models.CharField(max_length=20, verbose_name=_('کد پستی'))
    address = models.CharField(max_length=300, verbose_name=_('آدرس'))

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item', verbose_name=_('سفارش'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_item', verbose_name=_('محصول'))
    price = models.IntegerField(_('قیمت محصول'))
    color = models.CharField(max_length=20, verbose_name=_('رنگ محصول'))
    quantity = models.SmallIntegerField()

    def __str__(self):
        return f"{self.order} - {self.product}"