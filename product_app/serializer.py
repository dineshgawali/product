from rest_framework import serializers
from django.contrib.auth.models import User
from product_app.models import Product, UserRating

class SignUpSerializer(serializers.Serializer):
	class Meta:
		model = User
		fields = ('username', 'password')


class ProductSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		return Product.objects.create(**validated_data)

	class Meta:
		model = Product
		fields = "__all__"

	def validate(self, data):
		"""
		Check that start is before finish.
		"""
		if data.get('rating'):
			data.pop('rating')
		return data	

class RatingSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		return UserRating.objects.create(**validated_data)

	class Meta:
		model = UserRating
		fields = "__all__"
	def validate(self, data):
		"""
		Check that start is before finish.
		"""
		if UserRating.objects.filter(product=data.get('product'), user=data.get('user')):
			raise serializers.ValidationError("You already rate for this product")

		if data['rating'] > 10:
		   raise serializers.ValidationError("ratings must be less than 10")
		return data	
