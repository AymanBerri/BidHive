from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from datetime import datetime

from .models import User, Category, Listing, Comment, Bid


def index(request):
    # Or the listing page view

    listings = Listing.objects.filter(open_for_bid=True)


    return render(request, "auctions/index.html", {
        'page_title': "Active Listings",
        'listings': listings,
    })


def categories_page(request):
    # Retrieve all categories that have at least one associated listing
    categories = Category.objects.filter(category_listings__isnull=False).distinct()

    return render(request, 'auctions/categories.html', {
        'categories': categories,
    })


def category_page(request, type):
    # after user chooses the category he wants, he is brought here
    # we just use the index page, but we filter what we show

    listing_of_type = Category.objects.get(type=type)
    listings_related = listing_of_type.category_listings.all()

    return render(request, 'auctions/index.html', {
        'page_title': type,
        'listings': listings_related,
    })


@login_required
def create(request):
    if request.method == "POST":
        print(request.POST)

        # Creating a Listing method with the info we get fomr the form
        title = request.POST['title']
        description = request.POST['description']
        start_price = (float)(request.POST['price'])
        categories = request.POST.getlist('categories')
        image = request.POST['image']
        date_posted = datetime.now()
        owner = request.user

        print(f">>>>>>>>>>>>>>>> {categories}")

        # creating the new listing
        new_listing = Listing(title=title, description=description, image=image, start_price=start_price, date_posted=date_posted, owner=owner)
        new_listing.save()
        new_listing.categories.set(categories)


        print(f"---------------- {new_listing.categories}")

        # # creating the starting bid
        # new_bid = Bid(listing=new_listing, bidder=request.user, bid=starting_bid)
        # new_bid.save()

        new_listing.categories.set(categories)

        # Redirect to the listing's page by passing the listing_pk as a parameter
        return redirect('listing', listing_pk=new_listing.pk)

    all_categories = Category.objects.all()
    return render(request, "auctions/create.html",{
        "all_categories": all_categories,
    })


@login_required
def watchlist(request):
    # Retrieve the current user's watchlist
    watchlist_listings = request.user.watchlist.all()

    # the same thing ive done for "Active listings" and "Category page"
    return render(request, 'auctions/index.html', {
        'page_title': "Watchlist",
        'listings': watchlist_listings,
    })

@login_required
def my_bids(request):
    # retrieve all the listings where the user bid on
    my_bids = Bid.objects.filter(bidder=request.user)

    # getting unique listings using set comprehension
    listings = {bid.listing for bid in my_bids}

    return render(request, 'auctions/index.html', {
        'page_title': "My Bids",
        'listings': listings,
    })


def listing_view(request, listing_pk):

    # Check if listing exists
    try:
        listing = Listing.objects.get(pk=listing_pk)

        # error variables
        new_bid_error = ''  # Initialize the variable
    except Listing.DoesNotExist:
        return HttpResponse("<h1>Listing not found</h1>", status=404)


    if request.user.is_authenticated:
        # Get bool for if the User has this specific listing in his watchlist
        is_watchlisted = request.user.watchlist.filter(pk=listing_pk).exists()

        if request.method == "POST":

            # handle the WATCHLIST FORM
            if 'watchlist_btn' in request.POST:
                print(">>>>>>>>>>>>> WHATCHLIST")
                if is_watchlisted:
                    request.user.watchlist.remove(listing)
                    # must update the variable before rendering the page, otherwise it wont work.
                    is_watchlisted = False
                else:
                    request.user.watchlist.add(listing)
                    is_watchlisted = True

                # If the user chooses to add/remove the listing from the watchlist.
                return render(request, "auctions/listing.html", {
                    'listing': listing,
                    'bid_price': listing.bids.all().last().bid if listing.bids.all().last() else listing.start_price,
                    'is_watchlisted': 'Add to watchlist' if not is_watchlisted else 'Remove from watchlist',
                    
                })
            
            # OWNER CLOSE BID BUTTON
            elif 'close_bid' in request.POST:
                # close bidding
                listing.open_for_bid = False
                # get the winner
                listing.bidding_winner = listing.bids.all().last().bidder
                listing.save()



            
            elif 'new_bid' in request.POST:
                # getting the last bid if exists else the start price (the current price)
                bid_price = listing.bids.all().last().bid if listing.bids.all().last() else listing.start_price

                # how much the user bids on it
                new_bid = float(request.POST['new_bid'])

                # check if the bid is acceptable.
                if new_bid <= bid_price:
                    # handle with error to user
                    new_bid_error = f"Invalid bid amount. Please enter a bid higher than ${bid_price}"
                else:
                    # create new bid
                    create_bid = Bid(listing=listing, bidder=request.user, bid=new_bid)
                    create_bid.save()

            
            # handle the COMMENT FORM
            elif 'comment_content' in request.POST:
                comment_content = request.POST['comment_content']

                if comment_content.strip():
                    print(comment_content)
                    # creating a new object Comment
                    new_comment = Comment(listing=listing, author=request.user, content=comment_content, date_posted=timezone.now())
                    new_comment.save()

                # Redirect to the same page with an anchor link to the comments section
                listing_url = reverse('listing', kwargs={'listing_pk': listing_pk})
                return redirect(f'{listing_url}#comments-section')

        
        
        # If user is authenticated but visiting the page for the FIRST time
        return render(request, "auctions/listing.html", {
        'listing': listing,
        # if there is a bid, get the last one and print the bid amount, else print the start price
        'bid_price': listing.bids.all().last().bid if listing.bids.all().last() else listing.start_price,
        'new_bid_error': new_bid_error,
        'is_watchlisted': 'Add to watchlist' if not is_watchlisted else 'Remove from watchlist',
        })


    # If user is not authenticated, he can't use the watchlist feature
    return render(request, "auctions/listing.html", {
        'listing': listing,
        'bid_price': listing.bids.all().last().bid,
        'is_watchlisted': '',
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
    return redirect('index')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"] # Second try for the new password
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
        # If the uername is unique, the new user is created (above) and logged in (below).
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
