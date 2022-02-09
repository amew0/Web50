from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError,connection
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from .models import *
from django.db.models import Max
import sqlite3

def index(request):
	return render(request, "auctions/index.html",{
		"listings":Listing.objects.filter(active = True).order_by('category'),
		"id":request.user.id
		})

def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "auctions/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "auctions/login.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))


def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "auctions/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "auctions/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "auctions/register.html")

class ListingForm(ModelForm):
	class Meta:
		model = Listing
		fields = ['category','title','description','startingBid','imageUrl']
class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['comment' ]


def newListing (request):
	if request.method == "POST":
		category1 = request.POST["category"]
		title1 = request.POST["title"]
		description1 = request.POST["description"]
		startingBid1 = request.POST["startingBid"]
		imageUrl1 = request.POST["imageUrl"]
		userL1 = User.objects.get(pk = request.user.id)

		create = Listing(category=category1, 
						title = title1, 
						description = description1,
						startingBid = startingBid1, 
						imageUrl = imageUrl1, 
						userL = userL1)
		create.save()
		return render(request, "auctions/index.html",{
			"listings":Listing.objects.filter(active = True)
			})
	else:
		return render(request, "auctions/newListing.html",{
			"newListing":ListingForm()
			})
def listing (request,listingId):
	message = ""
	if request.user.id == None:
		UserWatchlist = None
	else:
		UserWatchlist = User.objects.get(pk=request.user.id).listing.all()
	currentPrice = Bid.objects.filter(listingB_id = listingId).aggregate(Max('bid'))["bid__max"] 
	if currentPrice == None:
		currentPrice = Listing.objects.get(id = listingId).startingBid
	if request.method == "POST":
		if 'submitC' in request.POST:
			comment = request.POST["comment"]
			listing = Listing.objects.get(pk = listingId)
			user = User.objects.get(pk = request.user.id)
			if user == None:
				user = -1
			Comment(userC = user, listingC = listing, comment = comment).save()
			
		elif 'submitB' in request.POST:
			try:
				bid = request.POST["bid"]
				listing = Listing.objects.get(pk = listingId)
				user = User.objects.get(pk = request.user.id)
				if user == None:
					user = -1
				Bid(userB = user, listingB = listing, bid = bid).save()
			except:
				message = "Bid can't be empty."


			try: 
				previousBid = Winner.objects.get(winnerL_id = listingId).winnerB	
			except:
				previousBid = 0

			try:
				if (previousBid == 0):
					Winner(winnerU = user, winnerL = listing, winnerB = bid).save()
				else:
					temp = Winner.objects.get(winnerL_id = listingId)
					temp.winnerU = user
					temp.winnerL = listing
					temp.winnerB = bid
					temp.save()
				currentPrice = bid
			except:
				message = message

	try: 
		andegna = Winner.objects.get(winnerL_id = listingId)
	except:
		andegna = Winner(winnerB = -1, winnerU = User.objects.get(id = 1), winnerL = Listing.objects.get(id = listingId))
	return render(request, "auctions/listing.html",{
		"listings":Listing.objects.filter(pk = listingId, active = True),
		"UserWatchlist":UserWatchlist,
		"commentForm":CommentForm(),
		"comments":Comment.objects.filter(listingC_id = listingId),
		"currentPrice": currentPrice,
		"min": float(currentPrice)+0.01,
		"bidsCount": Bid.objects.filter(listingB_id = listingId).count(),
		"isCreator":Listing.objects.get(pk = listingId).userL.id == request.user.id,
		"isActive" : Listing.objects.get(pk = listingId).active,
		"winnerBid" : andegna.winnerB,
		"winner" : andegna.winnerU,
		"winnerId": andegna.winnerU.id,
		"message": message
		})
def watchlist(request):
	
	return render (request,"auctions/watchlist.html",{
		"listings":User.objects.get(pk=request.user.id).listing.all()
		})

def Uwatchlist(request,listingId):
	
	User.objects.get(pk=request.user.id).listing.add(Listing.objects.get(pk=listingId))
	return HttpResponseRedirect (reverse("listing", args=(listingId,)))
	
def Rwatchlist(request,listingId,id):
	User.objects.get(pk=request.user.id).listing.remove(Listing.objects.get(pk=listingId))
	if id == 1:
		return HttpResponseRedirect (reverse("watchlist"))
	else:
		return HttpResponseRedirect (reverse("listing", args=(listingId,)))

def categories (request):
	connection = sqlite3.connect("db.sqlite3") 
  
	cursor = connection.cursor() 
	return render (request, "auctions/categories.html",{
		"listings":Listing.objects.values_list("category", flat=True).distinct()
		})
def category (request,category):
	return render (request, "auctions/category.html",{
		"category":category,
		"listings":Listing.objects.filter(category = category, active = True)
		})

def close (request, listingId):
	listing = Listing.objects.get(pk = listingId)
	listing.active = False
	listing.save()
	message = ""
	try:
		winnerBid = Listing.objects.get(pk = listingId).listingB.all().aggregate(Max('bid'))["bid__max"]
		winner = Bid.objects.get(bid = winnerBid).userB.username
		winnerId = Bid.objects.get(bid = winnerBid).userB.id

		Listing.objects.get(pk = listingId).listingB.all().delete()
		andegna = Winner.objects.get(winnerL_id = listingId)

		return render (request, "auctions/listing.html" ,{
		"winnerBid" : andegna.winnerB,
		"winner" : andegna.winnerU,
		"winnerId": andegna.winnerU.id,
		"isActive": Listing.objects.get(pk = listingId).active
		})

	except:
		message = "No one bid for this listing."
		return render (request, "auctions/listing.html" ,{
			"isActive": Listing.objects.get(pk = listingId).active,
			"Emessage": message
			})