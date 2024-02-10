from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #  Because it inherits from AbstractUser, it will already have fields for a username, email, password, etc.
    watchlist = models.ManyToManyField('Listing', blank=True, related_name='watchers')  # all the listings the user chose to put on watchlist

class Category(models.Model):
    type = models.CharField(max_length=64) # the name of the category
    description = models.TextField()


    def __str__(self) -> str:
        return f"{self.type}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    categories = models.ManyToManyField(Category, blank=False, related_name='category_listings')
    image = models.URLField(blank=True)
    date_posted = models.DateField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing_owners')
    bidding_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid_winners', null=True, blank=True)
    open_for_bid = models.BooleanField(default=True)


    def __str__(self) -> str:
        return f"{self.title}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField( max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.bidder} bid  ${self.bid} on {self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments", default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    date_posted = models.DateTimeField()

    def __str__(self) -> str:
        return self.content



