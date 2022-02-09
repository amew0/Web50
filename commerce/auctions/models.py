from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES = [
	('Laptop','laptop'),
	('Mobile','mobile'),
	('Watch','watch'),
	('other','other')
]
	
class Listing (models.Model):
	category = models.CharField(max_length = 64,choices = CATEGORIES)
	title = models.CharField(max_length = 64)
	description = models.CharField(max_length = 255)
	startingBid = models.DecimalField(max_digits = 10,decimal_places = 2)
	# default value of "image not found" if users do not pasted any URL.
	imageUrl = models.URLField(default = "https://www.thermaxglobal.com/wp-content/uploads/2020/05/image-not-found.jpg")
	userL = models.ForeignKey(to='auctions.User', on_delete=models.CASCADE, related_name = "userL" )
	active = models.BooleanField(default = True)
	def __str__(self):
		return f"{self.title}"

class User (AbstractUser):
    listing = models.ManyToManyField(Listing, blank = True, related_name ="listing")

class Bid (models.Model):
	userB = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "userB")
	listingB = models.ForeignKey(Listing, on_delete=models.CASCADE, blank = True ,related_name = "listingB")
	bid = models.DecimalField(max_digits = 10, decimal_places = 2)

class Comment (models.Model):
	userC = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "userC")
	listingC = models.ForeignKey(Listing, on_delete=models.CASCADE, blank = True ,related_name = "listingC")
	comment = models.TextField()
	def __str__(self):
		return f"{self.comment}"

class Winner (models.Model):
	winnerU = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "winnerU")
	winnerL = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name = "winnerL")
	winnerB = models.DecimalField(max_digits = 10,decimal_places = 2)