from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name ="create"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("my_bids/", views.my_bids, name="my_bids"),

    path('categories/' , views.categories_page, name='categories_page'),
    path('category/<str:type>' , views.category_page, name='category_page'),
    path("listing/<str:listing_pk>", views.listing_view, name="listing"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
