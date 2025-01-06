from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from rest_framework import serializers
from datetime import timedelta, datetime
from .models import *
from .validators import random_code_otp
from .send_sms import send_otp_code

User = get_user_model()


class CreateUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password']


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        expired_date = datetime.now() + timedelta(minutes=2)
        OtpCode.objects.create(user=user, code=random_code_otp(), expired_date=expired_date)
        send_otp_code(phone_number=user.phone_number, code=random_code_otp())
        print(f"otp code for {user.username}: {random_code_otp()}")
        return user



class VerifyCodeSerializers(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ['code']
        read_only_fields = ['user', 'expired_date']
    

    def validate(self, attrs):
        phone_number = self.context['request'].user
        code = attrs.get('code')

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('کاربری با این مشخصات وجود ندارد'))
        
        otp = OtpCode.objects.filter(user=user, code=code).first()

        if not otp:
            raise serializers.ValidationError(_('کد اشتباه است!'))
                
        if otp.expired_date_over:
            otp.delete_otp()
            raise serializers.ValidationError(_('کد منقضی شده است!'))
        
        user.is_active = True
        user.save()

        otp.delete()
        return attrs


class PasswordResetRequestSerializers(serializers.Serializer):
    email = serializers.EmailField()


    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_('کاربری با این ایمیل وجود ندارد !!!'))
        return value
    

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        reset_token = PasswordResetToken.objects.create(user=user)

        reset_link = f"{self.context['request'].build_absolute_uri(reverse_lazy('password-reset', kwargs={'token':str(reset_token.token)}))}"

        send_mail(
            subject= _('درخواست تغییر کلمه عبور'),
            message= _(f"برای تغییر کلمه عبور روی لینک کلیک کنید {reset_link}"),
            from_email= 'example@gmail.com',
            recipient_list= [user.email],
            fail_silently= False
        )

        print(reset_link)
        return reset_token



class PasswordResetConfirmSerializers(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password1 = attrs['new_password']
        password2 = attrs['confirm_new_password']

        if password1 and password1 != password2:
            raise serializers.ValidationError(_('کلمه عبور باید یکسان باشد !!!'))
        elif len(password1) < 8:
            raise serializers.ValidationError(_('کلمه عبور باید شامل 8 کاراکتر یا عدد باشد !!!'))
        return attrs


    def validate_token(self, value):
        try:
            reset_token = PasswordResetToken.objects.get(is_used=False, token=value)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError(_('توکن معتبر نیست'))

        if not reset_token.is_valid():
            raise serializers.ValidationError(_('توکن منقضی شده است'))
        return value


    def save(self, **kwargs):
        reset_token = PasswordResetToken.objects.get(token=self.validated_data['token'])
        user = reset_token.user
        user.set_password(self.validated_data['new_password'])
        user.save()
        reset_token.is_used = True
        reset_token.save()


class ResendCodeSerializers(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=11)


    def validate_phone_number(self, value):
        try:
            User.objects.get(phone_number=value)
        except User.DoesNotExist:
            raise  serializers.ValidationError(_("کاربری با این شماره تلفن یافت نشد !"))
        return value


    def create(self, validated_data):
        user = User.objects.get(phone_number=validated_data['phone_number'])

        otp_code = random_code_otp()
        expire_date = datetime.now() + timedelta(minutes=2)

        OtpCode.objects.update_or_create(user=user, defaults={'code': otp_code, 'expired_date': expire_date})
        send_otp_code(phone_number=user.phone_number, code=random_code_otp())
        print(f"Resend code for {user.phone_number} : {otp_code}")
        return user
    

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class ProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
        