from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
	name = models.CharField(max_length=255)
	price = models.FloatField(null=True, blank=True)
	rating = models.FloatField(null=True, blank=True)

	def __str__(self):
		return "%s" % (self.name)

class UserRating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	rating = models.FloatField(null=True, blank=True)
	
	def __str__(self):		
		return "%s" % (self.user.username)

	def save(self, *args, **kwargs):
		if self.rating:
			product_rating = Product.objects.get(id=self.product.id)
			user_rating = UserRating.objects.filter(product_id=self.product.id).values_list('rating')
			rating_list = [rating[0] for rating in user_rating]
			total_rating = (sum(rating_list) + self.rating) / (len(user_rating) + 1)
			product_rating.rating = total_rating 
			product_rating.save()
		super(UserRating, self).save(*args, **kwargs)