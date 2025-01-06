from rest_framework import serializers
from .models import Article, CategoryArticle, CommentArticle


class CategoryArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryArticle
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['user']


class CommentArticleSerializer(serializers.ModelSerializer):
    article = serializers.CharField(source='article.title')

    class Meta:
        model = CommentArticle
        fields = '__all__'
        read_only_fields = ['user']


class CreateCommentArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentArticle
		fields = ['body']

	def create(self, validated_data):
		article = Article.objects.get(slug=self.context['article_slug'])
		return CommentArticle.objects.create(article=article, **validated_data)