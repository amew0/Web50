from django.contrib import admin

# whenever you add class import it here
from .models import User,Listing,Bid,Comment

# Register your models here.

admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)