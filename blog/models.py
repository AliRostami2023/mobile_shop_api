from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from slugify import slugify
from core.models import CreateMixin, UpdateMixin


User = get_user_model()


class CategoryArticle(CreateMixin, UpdateMixin):
	title = models.CharField(max_length=300, verbose_name=_('عنوان دسته بندی'))
	slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name=_('اسلاگ'))


	def __str__(self):
		return self.title
	

	def save(self, *args, **kwargs):
		if not self.slug or (self.pk and CategoryArticle.objects.get(pk=self.pk).title != self.title):
			self.slug = slugify(self.title, allow_unicode=True)
		return super().save(*args, **kwargs)



class Article(CreateMixin, UpdateMixin):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_article', verbose_name=_('نویسنده'))
	title = models.CharField(max_length=300, verbose_name=_('عنوان مقاله'))
	slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name=_('اسلاگ'))
	category = models.ForeignKey(CategoryArticle, on_delete=models.CASCADE, related_name='category_article', verbose_name=_('دسته بندی'))
	image = models.ImageField(upload_to='article_image', verbose_name=_('تصویر مقاله'))
	content = models.TextField(_('متن مقاله'))
	time_study = models.CharField(max_length=25, verbose_name=_('زمان مطالعه'))

	def __str__(self):
		return self.title
	

	def save(self, *args, **kwargs):
		if not self.slug or (self.pk and Article.objects.get(pk=self.pk).title != self.title):
			self.slug = slugify(self.title, allow_unicode=True)
		return super().save(*args, **kwargs)


class CommentArticle(CreateMixin):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment', verbose_name=_('کاربر'))
	article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comment', verbose_name=_('مقاله'))
	body = models.TextField(_('دیدگاه'))
	reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent', null=True, blank=True, verbose_name=_('پاسخ به دیدگاه'))


	def __str__(self):
		return f"{self.user.get_full_name()} - {self.body[:20]}"
	
	