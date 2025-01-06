from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import datetime
import uuid
from .validators import MobileValidator
from core.models import CreateMixin, UpdateMixin
from .managers import UserManager


class Customer(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, validators=[MobileValidator()],
                                     verbose_name=_('شماره تلفن'))    
    
    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number
    

class OtpCode(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='otpuser', verbose_name=_('user'))
    code = models.PositiveIntegerField(_('code'))
    expired_date = models.DateTimeField(_('expired date'))


    def __str__(self) -> str:
        return f"{self.user.username} +' '+ {self.code}"
    
    
    @property
    def expired_date_over(self):
        return datetime.now() > self.expired_date
    

    def delete_otp(self):
        if self.expired_date_over():
            self.delete()
            return True
        return False
    

class PasswordResetToken(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='password_reset')
    token = models.UUIDField(unique=True, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


    def is_valid(self):
        return datetime.now() > self.created + timedelta(days=2) and not self.is_used
    


class Profile(CreateMixin, UpdateMixin):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='profile_customer', verbose_name=_('مشتری'))
    avatar = models.ImageField(upload_to='avatar_profile/', null=True, blank=True, verbose_name=_('تصویر پروفایل'))
    about_me = models.TextField(_('درباره من'), null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('آدرس'))


    def __str__(self):
        return self.user.phone_number
    