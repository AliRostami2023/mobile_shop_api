from rest_framework import viewsets, permissions
from .models import ContactUs, FooterLink, SocialMediaShop, FooterSite
from .serializers import *



class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [permissions.IsAdminUser]


    def get_permissions(self):
        if self.request.user == 'POST':
            return [permissions.AllowAny]
        return super().get_permissions()


class FooterLinkViewSet(viewsets.ModelViewSet):
    queryset = FooterLink.objects.select_related('footer_link_box')
    serializer_class = FooterLinkSerializer
    permission_classes = [permissions.IsAdminUser]


class FooterSiteViewSet(viewsets.ModelViewSet):
    queryset = FooterSite.objects.all()
    serializer_class = FooterSiteSerializer
    permission_classes = [permissions.IsAdminUser]


class SocialMediaShopViewSet(viewsets.ModelViewSet):
    queryset = SocialMediaShop.objects.all()
    serializer_class = SocialMediaShopSerializer
    permission_classes = [permissions.IsAdminUser]
    