from django.contrib import admin
from .models import Category, Actor, Genre, Raiting, RatingStar, Reviews, Movie, MovieShots

# Register your models here.

admin.site.register(Category)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Raiting)
admin.site.register(RatingStar)
admin.site.register(Reviews)
admin.site.register(MovieShots)
admin.site.register(Movie)
