from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.db.models import Sum, F, DecimalField
from rest_framework import status
from rest_framework.response import Response
from product.serializers import ProductSerializer
from blog.serializers import ArticleSerializer
from product.models import Product
from blog.models import Article
from .models import Slider, BanerHomeSite
from .serializers import *



class HomePageAPIView(APIView):
    def get(self, request):
        # محصولات جدید
        new_products = Product.objects.select_related('category', 'brand', 'feature') \
                                       .prefetch_related('color') \
                                       .order_by('-create_at')[:10]
        new_products_serializer = ProductSerializer(new_products, many=True)
        
        # پرفروش‌ترین محصولات
        most_selling_products = Product.objects.select_related('category', 'brand', 'feature') \
                                               .prefetch_related('color') \
                                                .annotate(
                                                sale_count=Coalesce(
                                                Sum(F('product_item__quantity') * F('product_item__price')\
                                                , output_field=DecimalField()),
                                                Decimal('0'))) \
                                                .order_by('-sale_count')[:10]
        most_selling_products_serializer = ProductSerializer(most_selling_products, many=True)
        
        # مقالات جدید
        new_articles = Article.objects.select_related('category') \
                                       .order_by('-create_at')[:4]
        new_articles_serializer = ArticleSerializer(new_articles, many=True)
        
        response_data = {
            "new_products": new_products_serializer.data,
            "most_selling_products": most_selling_products_serializer.data,
            "new_articles": new_articles_serializer.data,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)



class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [permissions.IsAdminUser]


class BanerSiteViewSet(viewsets.ModelViewSet):
    queryset = BanerHomeSite.objects.all()
    serializer_class = BanerSiteSerializer
    permission_classes = [permissions.IsAdminUser]

