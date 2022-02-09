from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing",views.newListing,name = "newListing"),
    path("<int:listingId>",views.listing,name = "listing"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("watchlist/<int:listingId>",views.Uwatchlist,name="Uwatchlist"),
    path("<int:listingId>/remove/<int:id>",views.Rwatchlist,name="Rwatchlist"),
    path("categories",views.categories, name="categories"),
    path("categories/<str:category>",views.category, name = "category"),
    path("<int:listingId>/close",views.close, name = "close"),
]
