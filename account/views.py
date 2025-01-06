from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .permissions import IsAdminOrSelf

User = get_user_model()


class UserRagistrationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': _('کد تایید ارسال شد'),
                                  'redirect_url': reverse('auth:verify_code-list'),
                                  'user_id': user.id,
                                    }, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class VerifyCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = VerifyCodeSerializers


    def get_serializer_context(self):
        return {'request': self.request}


    def create(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('ثبت نام با موفقیت انجام شد.')}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ResendCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ResendCodeSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': _('کد ارسال شد.')}, status.HTTP_200_OK)


class PasswordResetViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = PasswordResetRequestSerializers


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('یک ایمیل برای تغییر کلمه عبور برایتان ارسال کردیم!')}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class ConfirmResetPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = PasswordResetConfirmSerializers


    def create(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': _('کلمه عبور با موفقیت تغییر کرد.')}, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.UpdateModelMixin,
                                                                        viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrSelf]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.select_related('user')
        return Profile.objects.filter(user=self.request.user).select_related('user')
