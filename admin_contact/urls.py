from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('contact_us', views.ContactUsViewSet, basename='contact_us')
router.register('footer_link', views.FooterLinkViewSet, basename='footer_link')
router.register('footer_site', views.FooterSiteViewSet, basename='footer_site')
router.register('social_media_shop', views.SocialMediaShopViewSet, basename='social_media_shop')

app_name = 'contact'

urlpatterns = router.urls