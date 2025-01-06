from rest_framework import viewsets, permissions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Article, CategoryArticle, CommentArticle
from .serializers import ArticleSerializer, CommentArticleSerializer, CategoryArticleSerializer,\
                            CreateCommentArticleSerializer



class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author', 'category')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]


    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    

class CategoryArticleViewSet(viewsets.ModelViewSet):
    queryset = CategoryArticle.objects.all()
    serializer_class = CategoryArticleSerializer
    permission_classes = [permissions.AllowAny]


    @method_decorator(cache_page(60 * 20))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    

class CommentArticleViewSet(viewsets.ModelViewSet):
    queryset = CommentArticle.objects.select_related('user', 'article', 'reply')
    serializer_class = CommentArticleSerializer


    @method_decorator(cache_page(60 * 30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {"article_slug": self.kwargs['article_slug'], "request": self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCommentArticleSerializer
        return CommentArticleSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return CommentArticle.objects.filter(article__slug=self.kwargs['article_slug']).select_related('user', 'article', 'reply')
