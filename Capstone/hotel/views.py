from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Imported from current project
from .models import *

# Global variables lands here
allRes = Reservation.objects.all()
allBoo = Booking.objects.all()
sender = "Tsilal Hotel <noreply-booking@tsilal.com>"
admin_id = 1

pMethod = [i[1] for i in METHODS]
room_types = [i[0] for i in CATEGORIES]

@csrf_exempt
def index(request):
	if request.method == "POST":
		if request.POST.get("search"):
			fieldFromB = request.POST["fromB"]
			fieldToB = request.POST["toB"]
			
			availables = spotAvailable(fieldFromB, fieldToB)

			#only one reservation per user is allowed
			
			x = Reservation.objects.filter(userR_id=request.user.id)
			rExist = True if len(x) == 1 else False
			return render(request, "hotel/index.html", {
				"fieldFromB":fieldFromB,
				"fieldToB": fieldToB,
				"today" : datetime.now().strftime("%Y-%m-%d"),
				"typeRoomsAvailable":availables,
				"toDisplay":"inline",
				"searchDisp":"none",
				"display":"inline",
				"rExist":rExist,
				"pMethod":pMethod

				})
		elif request.POST.get("reserve"):
			bfIsIncluded = request.POST.get('bfIsIncluded')
			typeRoom = request.POST["typeRoom"]
			
			hFrom = request.POST["h-from"]
			hTo = request.POST["h-to"]

			bfIsIncluded = False if bfIsIncluded == None else True
			user = User.objects.get(pk=request.user.id)
			roomType_ = RoomTypePrice.objects.get(roomTypeP=typeRoom)
			availableRoom = Room.objects.filter(roomType=roomType_)[0] 
			#selecting the first room that satisfies this requirement
			
			reservation = Reservation(userR=user, 
									  roomR=availableRoom, 
									  fromR=hFrom, 
									  toR=hTo, 
									  bfIncluded=bfIsIncluded,
									  reservedTime=datetime.now())
			reservation.save()
			
			# reservations = Reservation.objects.get(userR_id=request.user.id)
			return HttpResponseRedirect('reservations/'+str(request.user.id))
		elif request.POST.get("pay"):
			book(request)
			return HttpResponseRedirect('bookings/'+str(request.user.id))
	else:
		return render (request, "hotel/index.html", {
			"toDisplay" : "none",
			"searchDisp":"inline",
			"display": "none",
			"today":datetime.now().strftime("%Y-%m-%d")
			})
@login_required
def book(request1):
	bfIsIncluded = request1.POST.get('bfIsIncluded')
	bfIsIncluded = False if bfIsIncluded == None else True
	typeRoom = request1.POST["typeRoom"]
	hFrom = request1.POST["h-from"]
	hTo = request1.POST["h-to"]
	payMethod = request1.POST["payment-method"]
	user = User.objects.get(pk=request1.user.id)
	roomType_ = RoomTypePrice.objects.get(roomTypeP=typeRoom)
	availableRoom = Room.objects.filter(roomType=roomType_)[0] 
	#selecting the first room that satisfies this requirement
	now = datetime.now()
	booking = Booking(userB=user,
						roomB=availableRoom,
						fromB=hFrom,
						toB=hTo,
						bfIncluded=bfIsIncluded,
						paidVia=payMethod,
						bookedTime=now)
	booking.save()

	bfYesNo = "Included" if bfIsIncluded else "Not included"
	receiver = f"{request1.user.username} <{request1.user.email}>"

	subject = "Booking confirmation"
	body = f"""\
	Hello {request1.user.username},

	Your booking has being confirmed.
	Here is the details of the booking.
	Room type: {typeRoom}
	Check in: {hFrom} 12:00
	Check out: {hTo} 14:00
	Breakfast: {bfYesNo}
	Booking time: {now}

	The booking has been paid via: {payMethod}.

	Thank you for choosing Tsilal hotel.
	-------------------------------------
	This is an auto-generated email. Please do not reply.
	"""
	send_mail(
		subject,
		body,
		sender,
		[receiver],
		fail_silently=False,
	)

def spotAvailable(fieldFromB,fieldToB):
	l = []
	temp0 = allRes.filter(fromR__lte = fieldFromB, toR__gte = fieldFromB)
	if (temp0.count() != 0):
		l.append(temp0)

	temp1 = allRes.filter(fromR__lte = fieldToB, toR__gte = fieldToB)
	if (temp1.count() != 0):
		l.append(temp1)

	temp2 = allRes.filter(fromR__gte = fieldFromB, toR__lte = fieldToB)
	if (temp2.count() != 0):
		l.append(temp2)

	temp3 = allBoo.filter(fromB__lte = fieldFromB, toB__gte = fieldFromB)
	if (temp3.count() != 0):
		l.append(temp3)

	temp4 = allBoo.filter(fromB__lte = fieldToB, toB__gte = fieldToB)
	if (temp4.count() != 0):
		l.append(temp4)

	temp5 = allBoo.filter(fromB__gte = fieldFromB, toB__lte = fieldToB)
	if (temp5.count() != 0):
		l.append(temp5)
	
	toBeExcluded = []
	#these are all conflicted entries with the one provided(fieldFromB and fieldToB)

	for i in l:
		for j in i:
			if isinstance(j, Booking):
				toBeExcluded.append(j.roomB.id)
			else:
				toBeExcluded.append(j.roomR.id)

	types = {}
	for room_type in room_types:
		roomType_ = RoomTypePrice.objects.get(roomTypeP=room_type)
		count = Room.objects.filter(roomType = roomType_).exclude(pk__in = toBeExcluded).count()
		types.update({room_type:count})

	availables = []
	for available in types:
		if types[available] != 0:
			availables.append(available)

	return availables

def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "hotel/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "hotel/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "hotel/register.html")

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
			return render(request, "hotel/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "hotel/login.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))

@login_required
def roomPrices(request):
		room_prices = {}
		roomTPs = RoomTypePrice.objects.all()
		for roomTP in roomTPs:
			room_prices.update({roomTP.roomTypeP:roomTP.roomPrice})

		if request.method == "GET":
			return JsonResponse(room_prices, safe=False)
		else:
			pass
@login_required
def bookings(request):
	if request.user.id == admin_id:
		if request.method == "GET":
			return JsonResponse([booking.serialize() for booking in allBoo], safe=False)
		elif request.method == "PUT":
			return render(request, "hotel/doesntexist.html")
	else:
		return render(request, "hotel/doesntexist.html")
@login_required
def reservations(request):
	if request.user.id == admin_id:
		if request.method == "GET":
			return JsonResponse([reservation.serialize() for reservation in allRes], safe=False)
	else:
		return render(request, "hotel/doesntexist.html")
@login_required
@csrf_exempt
def userReservation(request, userId):
	if request.user.id == userId or request.user.id == admin_id:
		if request.method == "GET":
			return JsonResponse([reservation.serialize() for reservation in allRes], safe=False)
		elif request.method == "PUT":
			# deleting
			x=Reservation.objects.get(userR_id = userId)
			x.delete()
			return HttpResponse(status=204)
	else:
		return render(request, "hotel/doesntexist.html")
@login_required
@csrf_exempt	
def showReservations(request, userId):
	if userId==request.user.id:
		if request.method == 'POST':
			if request.POST.get("pay-r"):
				book(request)
				rRemove = request.POST["rID"] 		#remove reservation
				record = Reservation.objects.get(pk = rRemove)
				record.delete()
				bookings = Booking.objects.filter(userB_id=userId).order_by("-fromB")
				return render (request, "hotel/bookings.html", {
					"bookings":bookings
					})
			elif request.POST.get("cancel-r"):
				rRemove = request.POST["rID"] 		#remove reservation
				roomID = request.POST["roomID"]
				record = Reservation.objects.get(pk = rRemove)
				record.delete()

				return render (request, "hotel/reservation.html",{
					"rExist":False,
					"pMethod":pMethod 
					})
		else:
			reservations = [] # there should only be 1
			fromR = None
			toR = None
			try:
				reservations = Reservation.objects.filter(userR_id=userId).order_by("-fromR")[0]
				fromR = str(reservations.fromR)[0:10]
				toR = str(reservations.toR)[0:10]
				rExist = True
			except:
				rExist = False
			return render (request, "hotel/reservation.html", {
				"reservations":reservations,
				"rExist": rExist,
				"pMethod":pMethod,
				"fromRR":fromR,
				"toRR":toR
				})
	else:
		return render(request, "hotel/doesntexist.html")
@login_required
def showBookings (request, userId):
	if userId == request.user.id:
		bExist = True
		bookings = Booking.objects.filter(userB_id=userId).order_by("-fromB")


		if(len(bookings)==0):
			bExist = False

		return render (request, "hotel/bookings.html", {
			"bookings":bookings,
			"bExist": bExist
			})
	else:
		return render(request, "hotel/doesntexist.html")

def errorPage (request, etc):
	from django.contrib import admin
	if (etc == "admin"):
		return admin.site.urls
	return render(request, "hotel/doesntexist.html")