from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('watchlist', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("type",)
    



class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "bid", "bidder")


class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date_posted", "open_for_bid")
    filter_horizontal = ('categories', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'listing', 'date_posted', '__str__')

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)