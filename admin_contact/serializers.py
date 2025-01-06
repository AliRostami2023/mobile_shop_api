from rest_framework import serializers
from .models import ContactUs, FooterLink, FooterLinkBox, FooterSite, SocialMediaShop


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class FooterLinkBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLinkBox
        fields = '__all__'


class FooterLinkSerializer(serializers.ModelSerializer):
    footer_link_box = FooterLinkBoxSerializer()

    class Meta:
        model = FooterLink
        fields = '__all__'


class FooterSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterSite
        fields = '__all__'


class SocialMediaShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaShop
        fields = '__all__'
        