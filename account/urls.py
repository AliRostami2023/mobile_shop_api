from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


router = DefaultRouter()
router.register('register', views.UserRagistrationViewSet, basename='register')
router.register('verify', views.VerifyCodeViewSet, basename='verify_code')
router.register('resend-code', views.ResendCodeViewSet, basename='resend_code')
router.register('password-reset', views.PasswordResetViewSet, basename='reset-password')
router.register('confirm-password-reset', views.ConfirmResetPasswordViewSet, basename='confirm-reset-password')
router.register('profile', views.ProfileViewSet, basename='profile')


app_name = 'auth'

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
