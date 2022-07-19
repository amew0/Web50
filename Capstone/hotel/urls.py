from django.urls import path
from . import views

urlpatterns = [
     path("", views.index, name="index"),
     path("register", views.register, name="register"),
     path("login", views.login_view, name="login"),
     path("logout", views.logout_view, name="logout"),
     path("reservations/<int:userId>", views.showReservations, name="showReservations"),
     path("bookings/<int:userId>", views.showBookings, name="showBookings"),

     #API Routes
     path("roomprices", views.roomPrices, name="rooms"),
     path("bookings", views.bookings, name="bookings"),
     path("reservations", views.reservations, name="reservations"),
     path("reservationFor/<int:userId>", views.userReservation, name="userReservations"),
     path("<str:etc>", views.errorPage, name="errorPage")
 ]