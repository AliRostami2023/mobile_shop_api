from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        ایجاد و ذخیره یک کاربر با شماره تلفن و رمز عبور.
        """
        if not phone_number:
            raise ValueError(_('وارد کردن شماره همراه الزامیست'))

        phone_number = self.normalize_phone_number(phone_number)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        ایجاد و ذخیره یک سوپریوزر با شماره تلفن و رمز عبور.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('سوپریوزر باید is_staff=True باشد.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('سوپریوزر باید is_superuser=True باشد.'))

        return self.create_user(phone_number, password, **extra_fields)

    def normalize_phone_number(self, phone_number):
        return ''.join(filter(str.isdigit, phone_number))
    
