from rest_framework import serializers
from .models import Slider, BanerHomeSite


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class BanerSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BanerHomeSite
        fields = '__all__'
        