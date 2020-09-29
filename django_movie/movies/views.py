from django.shortcuts import render
from django.views import View
import os

from .models import Movie

# Create your views here.


class MoviesView(View):
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, 'movies/movie_list.html', context={'movie_list': movies})

