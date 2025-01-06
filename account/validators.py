import random
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _



def random_code_otp():
    return random.randint(1000, 9999)


class MobileValidator(RegexValidator):
    regex = r"^0[0-9]{10}$"
    message = _(
        'شماره موبایل باید شامل 11 عدد باشد'
        'برای مثال  09171234567'
    )
