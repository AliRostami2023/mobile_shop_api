from django.urls import path
from .views import HomePageAPIView, SliderViewSet, BanerSiteViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('slider', SliderViewSet, basename='slider')
router.register('baner', BanerSiteViewSet, basename='baner')

app_name = 'home'

urlpatterns = [
    path('', HomePageAPIView.as_view(), name='home-page'),
] + router.urls
