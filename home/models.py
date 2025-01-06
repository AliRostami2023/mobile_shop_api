from django.db import models
from django.utils.translation import gettext_lazy as _


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    image = models.ImageField(upload_to='slider/', verbose_name=_('عکس اسلایدر'))
    link = models.URLField(null=True, blank=True, verbose_name=_('لینک'))

    def __str__(self):
        return self.title


class BanerHomeSite(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    image = models.ImageField(upload_to='baner/', verbose_name=_('عکس بنر'))
    link = models.URLField(null=True, blank=True, verbose_name=_('لینک'))
    
    def __str__(self):
        return self.title
    