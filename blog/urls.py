from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from . import views


router = DefaultRouter()
router.register('articles', views.ArticleViewSet, basename='article')
router.register('category', views.CategoryArticleViewSet, basename='category_article')

article_router = NestedDefaultRouter(router, 'articles', lookup='article')
article_router.register('comment', views.CommentArticleViewSet, basename='comment')


app_name = 'article'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(article_router.urls)),
]
