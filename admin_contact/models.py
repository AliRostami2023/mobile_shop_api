from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import CreateMixin



class ContactUs(CreateMixin):
    full_name = models.CharField(_('نام و نام خانوادگی'), max_length=300)
    phone_number = models.CharField(_('شماره همراه'), max_length=11)
    email = models.EmailField(_('ایمیل'), max_length=150)
    subject = models.CharField(_('موضوع پیام'), max_length=350)
    content = models.TextField(_('متن پیام'))


    def __str__(self):
        return self.full_name
    

class FooterSite(models.Model):
    shop_name = models.CharField(max_length=250, verbose_name=_('نام فروشگاه'))
    icon_shop = models.ImageField(upload_to='icon_shop/', verbose_name=_('آیکون فروشگاه'))
    about_shop = models.TextField(_('درباره فروشگاه'))
    about_me = models.TextField(_('متن صفحه درباره ما'))
    address = models.CharField(max_length=500, verbose_name=_('آدرس'))
    email = models.EmailField(max_length=400, verbose_name=_('ایمیل'))
    phone = models.CharField(max_length=11, verbose_name=_('شماره تلفن'))
    copy_right = models.CharField(max_length=500, verbose_name=_('متن کپی رایت'))

    def __str__(self):
        return self.shop_name
    


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    url = models.URLField(max_length=500, verbose_name=_('لینک'))
    footer_link_box = models.ForeignKey(to=FooterLinkBox, on_delete=models.CASCADE, verbose_name=_('دسته بندی'))

    def __str__(self):
        return self.title
    

class SocialMediaShop(models.Model):
    facebook = models.URLField(null=True, blank=True, verbose_name=_('فیسبوک'))
    twitter = models.URLField(null=True, blank=True, verbose_name=_('توییتر'))
    linkedin = models.URLField(null=True, blank=True, verbose_name=_('لینکدین'))
    pinterest = models.URLField(null=True, blank=True, verbose_name=_('پینترست'))
    telegram = models.URLField(null=True, blank=True, verbose_name=_('تلگرام'))
    instagram = models.URLField(null=True, blank=True, verbose_name=_('اینستاگرام'))

    def __str__(self):
        return self.instagram
    