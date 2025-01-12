from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, generics, permissions, status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from .filters import ProductFilter
from .models import CategoryProduct, Product, CommentProduct, FavoriteProduct
from .serializers import CategoryProductSerializer, ProductSerializer, CommentSerializer,\
	 						 CreateCommentSerializer, ProductFavoriteSerializer
from .paginations import ProductPagination


class CategoryProductViewSet(viewsets.ModelViewSet):
    queryset = CategoryProduct.objects.all()
    serializer_class = CategoryProductSerializer
    lookup_field = 'slug'

    

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'brand', 'feature').prefetch_related('color')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'category']
    ordering_fields = ['price', 'create_at']
    lookup_field = 'slug'


    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class CommentViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"product_slug": self.kwargs['product_slug'], "request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return CommentProduct.objects.filter(product__slug=self.kwargs['product_slug']).select_related('user', 'product', 'parent')


class FavoriteProductView(generics.GenericAPIView):
    serializer_class = ProductFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": _("محصول یافت نشد.")}, status=status.HTTP_404_NOT_FOUND)

        if FavoriteProduct.objects.filter(product=product, user=request.user).exists():
            return Response({"detail": _("این محصول قبلاً به علاقه‌مندی‌ها اضافه شده است.")}, status=status.HTTP_400_BAD_REQUEST)

        favorite = FavoriteProduct.objects.create(product=product, user=request.user)
        serializer = self.serializer_class(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": _("محصول یافت نشد.")}, status=status.HTTP_404_NOT_FOUND)

        favorite = FavoriteProduct.objects.filter(product=product, user=request.user)
        if favorite.exists():
            favorite.delete()
            return Response({"detail": _("محصول از علاقه‌مندی‌ها حذف شد.")}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": _("این محصول در لیست علاقه‌مندی‌های شما وجود ندارد.")}, status=status.HTTP_400_BAD_REQUEST)


class ListProductFavoriteAPIView(generics.ListAPIView):
    serializer_class = ProductFavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteProduct.objects.filter(user=self.request.user)