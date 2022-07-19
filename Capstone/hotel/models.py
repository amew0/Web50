from django.db import models
from django.contrib.auth.models import AbstractUser
# import datetime
import django.utils 
# Create your models here.
class User (AbstractUser):
	pass
CATEGORIES = [
	('Single', 'Single'),
	('Double', 'Double'),
	('Triple', 'Triple'),
	('Quad', 'Quad'),
	('King', 'King'), 	
	('Queen', 'Queen'),
	('Twin', 'Twin')
]
class RoomTypePrice(models.Model):
	roomTypeP = models.TextField(choices = CATEGORIES)
	roomPrice = models.DecimalField(max_digits = 10, decimal_places = 2)

	def serialize(self):
		return {
			"id": self.id,
			"roomType": self.roomTypeP,
			"roomPrice": self.roomPrice
		}
	def __str__(self):
		return f"{self.roomTypeP}"
class Room(models.Model):
	# roomType = models.TextField(choices = CATEGORIES)
	# price = models.DecimalField(max_digits = 10, decimal_places = 2)
	roomType = models.ForeignKey(RoomTypePrice, on_delete=models.CASCADE, related_name="roomType")
	description = models.TextField(blank = True)
	

	def serialize(self):
		return {
			"id": self.id,
			"roomType": self.roomType,
			"reserved": self.reserved,
			"booked": self.booked,
			"description": self.description,
			"price": self.price
		}
	def __str__(self):
		return f"Room {self.id} Type {self.roomType}"

class Reservation(models.Model):
	userR = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, related_name = "userR")
	roomR = models.ForeignKey(Room, on_delete = models.SET_NULL, null=True, related_name = "roomR")
	fromR = models.DateField()
	toR = models.DateField()
	bfIncluded = models.BooleanField(default = False)
	reservedTime = models.DateTimeField(django.utils.timezone.now())
	def serialize(self):
		return {
			"id": self.id,
			"userR": self.userR.id,
			"roomR": self.roomR.id,
			"fromR":self.fromR.strftime("%Y-%m-%d"),
			"toR":self.toR.strftime("%Y-%m-%d"),
			"bfIncluded": self.bfIncluded,
			"reservedTime":self.reservedTime
		}
	def __str__(self):
		return f"Reservation {self.id}: Room {self.roomR.id}: User {self.userR.id}"

METHODS = [
	('Cash', 'Cash'),
	('Master Card', 'Master Card'),
	('Visa', 'Visa'),
	('Bitcoin', 'Bitcoin')
]
class Booking(models.Model):
	userB = models.ForeignKey(User, on_delete = models.SET_NULL, null=True, related_name = "userB")
	roomB = models.ForeignKey(Room, on_delete = models.SET_NULL, null=True, related_name = "roomB")
	fromB = models.DateField()
	toB = models.DateField()
	paidVia = models.TextField(choices = METHODS)
	bfIncluded = models.BooleanField(default = False)
	bookedTime = models.DateTimeField(django.utils.timezone.now())
	def serialize(self):
		return {
			"id": self.id,
			"userB": self.userB.id,
			"roomB": self.roomB.id,
			"fromB":self.fromB.strftime("%Y-%m-%d"),
			"toB":self.toB.strftime("%Y-%m-%d"),
			"paidVia": self.paidVia,
			"bfIncluded": self.bfIncluded,
			"bookedTime": self.bookedTime
		}
	def __str__(self):
		return f"Booking {self.id}: Room {self.roomB.id}: User {self.userB.id}"