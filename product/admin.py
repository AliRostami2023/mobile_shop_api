from django.contrib import admin
from .models import Product, CategoryProduct, Brand, ProductFeature, Color


admin.site.register(Product)
admin.site.register(CategoryProduct)
admin.site.register(Brand)
admin.site.register(ProductFeature)
admin.site.register(Color)
