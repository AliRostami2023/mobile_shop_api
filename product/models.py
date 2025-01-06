from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from slugify import slugify
from core.models import CreateMixin, UpdateMixin


User = get_user_model()


class CategoryProduct(CreateMixin, UpdateMixin):
    title = models.CharField(max_length=350, verbose_name=_('عنوان'))
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name=_('اسلاگ'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='parent_category', verbose_name=_('زیرمجموعه'))

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and CategoryProduct.objects.get(pk=self.pk).title != self.title):
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(CreateMixin, UpdateMixin):
    title = models.CharField(max_length=500, verbose_name=_('نام محصول'))
    slug = models.SlugField(max_length=65, unique=True, allow_unicode=True, verbose_name=_('اسلاگ'))
    category = models.ForeignKey('CategoryProduct', related_name='category_product', on_delete=models.CASCADE, verbose_name=_('دسته بندی'))
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='brand', verbose_name=_('برند'))
    image = models.ImageField(upload_to='product_images', verbose_name=_('تصویر محصول'))
    price = models.IntegerField(_('قیمت محصول'))
    discount = models.SmallIntegerField(null=True, blank=True, verbose_name=_('تخفیف محصول(بر حسب درصد)'))
    color = models.ManyToManyField('Color', related_name='colors', verbose_name=_('رنگ های محصول'))
    available = models.BooleanField(default=True, verbose_name=_('موجود'))
    in_stock = models.SmallIntegerField(default=0, verbose_name=_('تعداد موجود در انبار'))
    desc = models.TextField(_('توضیحات'))
    feature = models.ForeignKey('ProductFeature', on_delete=models.CASCADE, related_name='feature_product', verbose_name=_('مشخصات محصول'))
    published = models.BooleanField(default=True, verbose_name=_('نمایش بده'))

    def __str__(self):
        return f"{self.title}, {self.category}"
    

    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Product.objects.get(pk=self.pk).title != self.title):
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


    def get_discounted_price(self):
        if self.discount:
            return self.price - (self.price * self.discount // 100)
        return self.price


class ProductFeature(models.Model):
    os = models.CharField(max_length=300, verbose_name=_('سیستم عامل'))
    model = models.CharField(max_length=350, verbose_name=_('مدل گوشی'))
    size = models.CharField(max_length=350, verbose_name=_('سایز صفحه نمایش(اینچ)'))
    weight = models.CharField(max_length=150, verbose_name=_('وزن'))
    number_sim = models.SmallIntegerField(default=2, verbose_name=_('تعداد سیم کارت'))
    internal_memory = models.CharField(max_length=30, verbose_name=_('حافظه داخلی'))
    ram = models.CharField(max_length=20, verbose_name=_('مقدار RAM'))
    camera = models.CharField(max_length=50, verbose_name=_('کیفیت دوربین(مگاپیکسل)'))

    def __str__(self):
        return self.model


class ImagesProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('محصول'))
    image = models.ImageField(upload_to='uploads/images_products', verbose_name=_('عکس'))

    def __str__(self):
        return self.product.title


class Brand(CreateMixin, UpdateMixin):
    title = models.CharField(max_length=300, verbose_name=_('نام برند'))
    slug = models.SlugField(max_length=350, unique=True, blank=True, verbose_name=_('اسلاگ'))

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug or (self.pk and Brand.objects.get(pk=self.pk).title != self.title):
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('نام رنگ'))

    def __str__(self):
        return self.name


class CommentProduct(CreateMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comment', verbose_name=_('محصول'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_product', verbose_name=_('کاربر'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name=_('پاسخ'))
    rating = models.PositiveSmallIntegerField(_('امتیاز به محصول'), validators=[MinValueValidator(1),
                                              MaxValueValidator(5)], null=True, blank=True)
    body = models.TextField(_('متن دیدگاه'))

    def __str__(self):
        return f"{self.product} - {self.user} - {self.body[:20]}"


class FavoriteProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='fproduct', verbose_name=_('محصول'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fuser', verbose_name=_('کاربر'))

    def __str__(self):
        return f"{self.product.title[:7]} - {self.user.get_full_name}"
    