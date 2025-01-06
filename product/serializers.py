from rest_framework import serializers
from .models import CategoryProduct, Product, CommentProduct, ProductFeature, ImagesProduct, FavoriteProduct



class CommentSerializer(serializers.ModelSerializer):
	product = serializers.CharField(source='product.title')
	
	class Meta:
		model = CommentProduct
		fields = '__all__'


class CreateCommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentProduct
		fields = ['body', 'rating']

	def create(self, validated_data):
		product = Product.objects.get(slug=self.context['product_slug'])
		return CommentProduct.objects.create(product=product, **validated_data)


class CategoryProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = CategoryProduct
		fields = '__all__'


class ProductFeatureSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductFeature
		fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ImagesProduct
		fields = '__all__'

		
class ProductSerializer(serializers.ModelSerializer):
	discounted_price = serializers.SerializerMethodField()
	product_comment = CommentSerializer(many=True, read_only=True)
	feature = ProductFeatureSerializer()
	images = ProductImageSerializer(many=True)
	color = serializers.StringRelatedField(
		many = True,
	)

	brand = serializers.StringRelatedField(
	)

	category = serializers.StringRelatedField(
	)

	class Meta:
		model = Product
		fields = ['title', 'category', 'brand', 'image', 'price', 'discount', 'discounted_price', 'color', 'available',
					 'in_stock', 'desc', 'feature', 'published', 'feature', 'product_comment', 'images']
	
	def get_discount_price(self, obj):
		return obj.get_discounted_price()


class ProductFavoriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = FavoriteProduct
		fields = ['id', 'user', 'product']
		read_only_fields = ['user']

		